import inquirer
import typer

from openapi_client import ResponseWorkspace
from savvihub import SavviHubClient


def get_default_workspace(client: SavviHubClient) -> ResponseWorkspace:
    workspaces = client.workspace_list().workspaces
    if len(workspaces) == 1:
        default_workspace = workspaces[0]
        typer.echo(f'Default workspace is automatically set to `{default_workspace.name}`.')
    else:
        default_workspace = inquirer.prompt([inquirer.List(
            'default_workspace',
            message='Select default workspace',
            choices=[(ws.name, ws) for ws in workspaces],
        )]).get('default_workspace')

        typer.echo(f'Default workspace is set to `{default_workspace.name}`.')

    return default_workspace


def find_from_inquirer(options, display, message):
    return inquirer.prompt([inquirer.List(
        "question",
        message=message,
        choices=[(f'[{i+1}] {display(option)}', option) for i, option in enumerate(options)],
    )]).get("question")
