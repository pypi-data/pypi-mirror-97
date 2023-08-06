import re

import typer
from terminaltables import AsciiTable

from savvihub.cli import kubectl
from savvihub.cli.constants import WEB_HOST
from savvihub.cli.exceptions import ExitException
from savvihub.cli.inputs.workspace import workspace_name_option
from savvihub.cli.typer import Typer, Context

cluster_app = Typer()


@cluster_app.callback()
def main():
    """
    Manage clusters
    """


@cluster_app.command(user_required=True)
def add(
    ctx: Context,
    workspace_name: str = workspace_name_option,
):
    """
    Add a new Kubernetes cluster to SavviHub
    """
    client = ctx.authenticated_client

    # kubectl context
    kubectl_context_name = kubectl.get_current_context()
    kubectl_context_confirm = typer.confirm(f'Current kubectl context is `{kubectl_context_name}`.\n'
                                            f'Do you want to add this Kubernetes cluster to SavviHub?', default=True)
    if not kubectl_context_confirm:
        raise ExitException('Run `kubectl config use-context` to switch the context.')

    default_master_endpoint, default_ssl_ca_cert_base64_encoded = kubectl.get_cluster_info(kubectl_context_name)

    # master endpoint
    master_endpoint = typer.prompt('Master endpoint', default=default_master_endpoint)

    # ssl ca cert
    ssl_ca_cert_base64_encoded = typer.prompt('CA cert (base64-encoded)', default=default_ssl_ca_cert_base64_encoded)

    # namespace
    namespace = typer.prompt('Kubernetes namespace')
    sa_token = kubectl.get_service_account_token(namespace)
    agent_access_token = kubectl.get_agent_access_token(namespace)

    # cluster name
    default_cluster_name = re.sub('[^0-9a-zA-Z]', '-', kubectl_context_name).strip('-')
    cluster_name = typer.prompt('Cluster name', default=default_cluster_name)

    # add cluster
    cluster = client.cluster_add(workspace_name, cluster_name, agent_access_token,
                                 master_endpoint, namespace, sa_token, ssl_ca_cert_base64_encoded)
    typer.echo(f'\n'
               f'Custom cluster `{cluster.name}` is successfully added to workspace `{workspace_name}`.\n'
               f'{WEB_HOST}/{workspace_name}/settings/clusters')


@cluster_app.command(user_required=True)
def list(
    ctx: Context,
    workspace_name: str = workspace_name_option,
):
    """
    List custom clusters added to SavviHub
    """
    client = ctx.authenticated_client
    clusters = client.cluster_list(workspace_name).clusters
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


@cluster_app.command(user_required=True)
def rename(
    ctx: Context,
    cluster_name: str = typer.Argument(..., help='Custom cluster name'),
    new_name: str = typer.Argument(..., help='A new name for the cluster'),
    workspace_name: str = workspace_name_option,
):
    """
    Rename a custom cluster
    """
    client = ctx.authenticated_client
    client.cluster_rename(workspace_name, cluster_name, new_name)
    typer.echo(f'Successfully renamed `{cluster_name}` to `{new_name}`')


@cluster_app.command(user_required=True)
def delete(
    ctx: Context,
    cluster_name: str = typer.Argument(..., help='Custom cluster name'),
    workspace_name: str = workspace_name_option,
):
    """
    Delete a custom cluster
    """
    client = ctx.authenticated_client
    client.cluster_delete(workspace_name, cluster_name)
    typer.echo(f'Successfully deleted `{cluster_name}`.')
