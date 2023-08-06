import inquirer
import typer

from savvihub.api.exceptions import NotFoundAPIException
from savvihub.cli.exceptions import ExitException, InvalidGitRepository
from savvihub.cli.git import GitRepository
from savvihub.cli.typer import Context


def project_name_callback(ctx: Context, project_name: str) -> str:
    workspace_name = ctx.params['workspace_name']
    try:
        git_repo = GitRepository()
    except InvalidGitRepository:
        if not project_name:
            projects = ctx.authenticated_client.project_list(workspace_name).results
            if len(projects) == 1:
                ctx.project = projects[0]
            else:
                ctx.project = inquirer.prompt([inquirer.List(
                    'project',
                    message='Select project',
                    choices=[(p.name, p) for p in projects],
                )]).get('project')

            return ctx.project.name

    if not project_name:
        project_name = git_repo._get_github_repo()[1]
        ctx.git_repo = git_repo
    elif project_name == git_repo._get_github_repo()[1]:
        ctx.git_repo = git_repo

    try:
        ctx.project = ctx.authenticated_client.project_read(workspace_name, project_name)
    except NotFoundAPIException:
        raise ExitException(f'Project `{project_name}` does not exist in the workspace `{workspace_name}`.')

    return project_name


project_name_option = typer.Option(None, '--project', callback=project_name_callback,
                                   help='If not present, uses git repository name of the current directory.')
