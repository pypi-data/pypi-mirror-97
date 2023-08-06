import sys

import inquirer
import typer

from savvihub import SavviHubClient
from savvihub.cli.constants import WEB_HOST
from savvihub_client import ResponseWorkspace


def get_full_info(workspace, project, experiment, form):
    return \
        f'Full {form} info at:\n' \
        f'    {WEB_HOST}/{workspace}/{project}/experiments/{experiment}/{form}\n'


def get_full_info_dataset(workspace, dataset):
    return \
        f'\n\tFull dataset info at:\n' \
        f'\t\t{WEB_HOST}/{workspace}/datasets/{dataset}\n'


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


def find_from_args(options, selector, error_message=''):
    for option in options:
        if selector(option):
            return option

    if error_message:
        typer.echo(error_message)
        sys.exit(1)


def find_from_inquirer(options, display, message):
    return inquirer.prompt([inquirer.List(
        "question",
        message=message,
        choices=[(f'[{i+1}] {display(option)}', option) for i, option in enumerate(options)],
    )]).get("question")
