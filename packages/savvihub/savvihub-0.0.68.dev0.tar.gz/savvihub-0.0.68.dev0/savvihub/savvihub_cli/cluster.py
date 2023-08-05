import re
import sys

import typer
from terminaltables import AsciiTable

from savvihub import Context
from savvihub.common import kubectl
from savvihub.common.constants import WEB_HOST
from savvihub.common.git import GitRepository, InvalidGitRepository

cluster_app = typer.Typer()


@cluster_app.callback()
def main():
    """
    Manage custom clusters
    """


@cluster_app.command()
def add():
    """
    Add a new Kubernetes cluster to SavviHub
    """
    context = Context(user_required=True)
    client = context.authorized_client

    # kubectl context
    kubectl_context_name = kubectl.get_current_context()
    kubectl_context_confirm = typer.confirm(f'Current kubectl context is `{kubectl_context_name}`.\n'
                                            f'Do you want to add this Kubernetes cluster to SavviHub?', default=True)
    if not kubectl_context_confirm:
        typer.echo('Run `kubectl config use-context` to switch the context.')
        sys.exit(1)

    # namespace
    namespace = typer.prompt('Kubernetes namespace')
    master_endpoint, ssl_ca_cert_base64_encoded = kubectl.get_cluster_info(kubectl_context_name)
    sa_token = kubectl.get_service_account_token(namespace)
    agent_access_token = kubectl.get_agent_access_token(namespace)

    # workspace
    default_workspace_name = get_default_workspace_name(context, prompt=False)
    workspace_name = typer.prompt('SavviHub workspace name', default=default_workspace_name)
    workspace = client.workspace_read(workspace_name)
    if workspace is None:
        typer.echo(f'Workspace `{workspace_name}` does not exist or is not accessible.')
        sys.exit(1)

    # cluster name
    default_cluster_name = re.sub('[^0-9a-zA-Z]', '-', kubectl_context_name).strip('-')
    cluster_name = typer.prompt('Cluster name', default=default_cluster_name)

    # add cluster
    cluster = client.cluster_add(workspace_name, cluster_name, agent_access_token,
                                 master_endpoint, namespace, sa_token, ssl_ca_cert_base64_encoded)
    typer.echo(f'\n'
               f'Custom cluster `{cluster.name}` is successfully added to workspace `{workspace_name}`.\n'
               f'{WEB_HOST}/{workspace_name}/settings/clusters')


@cluster_app.command()
def list():
    """
    List custom clusters added to SavviHub
    """
    context = Context(user_required=True)
    client = context.authorized_client
    workspace_name = get_default_workspace_name(context)
    clusters = client.cluster_list(workspace_name)
    rows = []
    for cluster in clusters:
        rows.append([
            cluster.name,
            'O' if cluster.is_savvihub_managed else 'X',
            cluster.kubernetes_master_endpoint or '-',
            cluster.kubernetes_namespace or '-',
            cluster.status.replace('-', ' ').upper(),
        ])

    table = AsciiTable([['NAME', 'SAVVIHUB-MANAGED', 'K8S MASTER ENDPOINT', 'K8S NAMESPACE', 'STATUS'], *rows])
    table.inner_column_border = False
    table.inner_heading_row_border = False
    table.inner_footing_row_border = False
    table.outer_border = False

    typer.echo(table.table)


@cluster_app.command()
def rename(
    cluster_name: str = typer.Argument(..., help='Custom cluster name'),
    new_name: str = typer.Argument(..., help='A new name for the cluster'),
):
    """
    Rename a custom cluster
    """
    context = Context(user_required=True)
    client = context.authorized_client
    workspace_name = get_default_workspace_name(context)
    client.cluster_rename(workspace_name, cluster_name, new_name)
    typer.echo(f'Successfully renamed `{cluster_name}` to `{new_name}`')


@cluster_app.command()
def delete(
    cluster_name: str = typer.Argument(..., help='Custom cluster name'),
):
    """
    Delete a custom cluster
    """
    context = Context(user_required=True)
    client = context.authorized_client
    workspace_name = get_default_workspace_name(context)
    client.cluster_delete(workspace_name, cluster_name)
    typer.echo(f'Successfully deleted `{cluster_name}`.')


def get_default_workspace_name(context, *, prompt=True):
    if len(context.user.workspaces) == 1:
        return context.user.workspaces[0].name

    try:
        context.git_repo = GitRepository()
        context.project_config = context.load_project_config(context.git_repo.get_savvihub_config_file_path())
        project = context.get_project()
        if project is not None:
            return project.workspace.name

    except InvalidGitRepository:
        pass

    if prompt:
        typer.echo('Run \'sv project init\' to set the default workspace name.')
        return typer.prompt('SavviHub workspace name')

    return None
