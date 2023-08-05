import os
import sys

import typer

from savvihub import Context
from savvihub.api.savvihub import SavviHubClient
from savvihub.common.config_loader import ProjectConfigLoader
from savvihub.common.constants import WEB_HOST, API_HOST
from savvihub.common.git import GitRepository, InvalidGitRepository
from savvihub.common.utils import remove_file

project_app = typer.Typer()


@project_app.callback()
def main():
    """
    Create the basic element of workspace
    """
    return


@project_app.command()
def init(
    name: str = typer.Argument(None, help="Type workspace/project as an argument"),
):
    """
    Initialize a new experiment configuration file with workspace/project
    """
    context = Context(user_required=True)
    if not context.user.github_authorized:
        typer.echo(f'You should authorize github first.\n{WEB_HOST}/cli/github-authorize/')
        return

    try:
        git_repo = GitRepository()
    except InvalidGitRepository as e:
        typer.echo(str(e))
        sys.exit(1)

    if not name:
        workspaces = context.authorized_client.workspace_list(raise_error=True)
        default_workspace_name = None
        if len(workspaces) == 1:
            default_workspace_name = workspaces[0].name

        workspace_name = typer.prompt("SavviHub workspace name", default=default_workspace_name)
        project_name = typer.prompt("SavviHub project name", default=git_repo.get_github_repo()[1])
    else:
        workspace_name, project_name = name.split("/")

    config_file_path = git_repo.get_savvihub_config_file_path()
    if os.path.exists(config_file_path):
        if typer.confirm(f'SavviHub config file already exists in {config_file_path}. Overwrite file?', abort=True):
            remove_file(config_file_path)
        else:
            return

    client = SavviHubClient(token=context.token)

    workspace = client.workspace_read(workspace_name)
    if workspace is None:
        typer.echo(f'Cannot find workspace {workspace_name}.')
        return

    project = client.project_read(workspace_name, project_name)
    if project is None:
        owner, repo = git_repo.get_github_repo()
        if typer.confirm(f'Project not found. Create new project in SavviHub?', abort=True):
            typer.echo(f'Workspace: {workspace_name}\nProject: {project_name}\nGit: github.com/{owner}/{repo}')
            client.project_github_create(workspace_name, project_name, owner, repo, raise_error=True)
            typer.echo(f'Project created successfully.\n{WEB_HOST}/{workspace_name}/{project_name}')

    project_config = ProjectConfigLoader(config_file_path)
    project_config.set_savvihub(url=API_HOST, workspace=workspace_name, project=project_name)
    project_config.save()

    typer.echo(f"Experiment config successfully made in {config_file_path}")


@project_app.command()
def status():
    """
    Print the current project configuration
    """
    context = Context(user_required=True, project_required=True)
    typer.echo(f'Workspace: {context.project.workspace.name}\nProject: {context.project.name}')
