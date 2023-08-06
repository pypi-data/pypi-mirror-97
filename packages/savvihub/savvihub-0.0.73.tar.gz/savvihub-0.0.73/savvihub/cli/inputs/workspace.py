import typer

from savvihub.api.exceptions import NotFoundAPIException
from savvihub.cli.exceptions import ExitException
from savvihub.cli.typer import Context
from savvihub.cli.utils import get_default_workspace


def workspace_name_callback(ctx: Context, workspace_name: str) -> str:
    if workspace_name:
        try:
            ctx.authenticated_client.workspace_read(workspace_name)
        except NotFoundAPIException:
            raise ExitException('Workspace not found.')
        return workspace_name

    return (ctx.workspace.name if ctx.workspace
            else get_default_workspace(ctx.authenticated_client).name)


workspace_name_option = typer.Option(None, '--workspace', callback=workspace_name_callback,
                                     help='Override the default workspace.')
