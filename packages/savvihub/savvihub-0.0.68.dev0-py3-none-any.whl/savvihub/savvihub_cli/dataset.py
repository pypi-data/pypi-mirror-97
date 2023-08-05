import sys
from urllib.parse import urlparse

import typer
from terminaltables import AsciiTable

from savvihub import Context
from savvihub.api.savvihub import SavviHubClient
from savvihub.common.constants import DATASET_SOURCE_TYPE_SAVVIHUB, DATASET_PATH_PARSE_SCHEME_GS, \
    DATASET_PATH_PARSE_SCHEME_S3
from savvihub.savvihub_cli.dataset_files import dataset_files_app

dataset_app = typer.Typer()
dataset_app.add_typer(dataset_files_app, name='files')


def parse_dataset_arg(dataset_arg):
    dataset_arg = dataset_arg.replace('svds://', '').strip('/')
    if '/' not in dataset_arg:
        typer.echo("You should specify dataset with workspace. ex) savvihub/mnist")
        sys.exit(1)

    if dataset_arg.count('/') > 1:
        typer.echo('Invalid dataset name format.')
        sys.exit(1)

    workspace, rest = dataset_arg.split("/")
    if ":" in rest:
        dataset, ref = rest.split(":")
    else:
        dataset = rest
        ref = "latest"
    return workspace, dataset, ref


@dataset_app.callback()
def main():
    """
    Manage the collection of data
    """
    return


@dataset_app.command()
def list():
    """
    Show my SavviHub dataset list
    """
    context = Context(user_required=True, project_required=True)
    client = context.authorized_client
    dataset_list = client.dataset_list(context.project.workspace.name)
    if len(dataset_list) == 0:
        typer.echo(f'No datasets found in \'{context.project.workspace.name}\' workspace.')
    else:
        table = AsciiTable([
            ['WORKSPACE/NAME', 'SOURCE TYPE'],
            *[[f'{d.workspace.name}/{d.name}', d.source.type] for d in dataset_list],
        ])
        table.inner_column_border = False
        table.inner_heading_row_border = False
        table.inner_footing_row_border = False
        table.outer_border = False

        typer.echo(table.table)


@dataset_app.command()
def create(
    dataset_arg: str = typer.Argument(...),
    path_arg: str = typer.Option(None, "-u", "--url", help="Dataset source path"),
    description: str = typer.Option(None, "-m", help="Dataset description"),
    aws_role_arn: str = typer.Option(None, "--aws-role-arn", help="AWS Role ARN")
):
    """
    Create a SavviHub dataset
    """
    workspace, dataset, _ = parse_dataset_arg(dataset_arg)

    context = Context(user_required=True)
    client = SavviHubClient(token=context.token)

    if path_arg:
        if not (path_arg.startswith("gs://") or path_arg.startswith("s3://")):
            typer.echo(f"path should start with \"gs://\" or \"s3://\"")
            return

        r = urlparse(path_arg)
        if r.scheme == DATASET_PATH_PARSE_SCHEME_GS:
            dataset_obj = client.dataset_gs_create(workspace, dataset, False, description, path_arg)
        elif r.scheme == DATASET_PATH_PARSE_SCHEME_S3:
            if not aws_role_arn:
                typer.echo("AWS Role ARN is required for S3 users")
                return
            dataset_obj = client.dataset_s3_create(workspace, dataset, False, description, path_arg, aws_role_arn)
        else:
            raise Exception("Only Google Cloud Storage and Amazon S3 are supported at the moment.")
    else:
        dataset_obj = client.dataset_create(workspace, dataset, False, description)

    if not dataset_obj:
        return

    dataset_name = dataset_obj.name
    typer.echo(f"Dataset {dataset_name} is created.")
    typer.echo(client.get_full_info_dataset(workspace, dataset_name))


@dataset_app.command()
def describe(
    dataset_arg: str = typer.Argument(...),
):
    """
    Describe the dataset information in detail
    """
    workspace, dataset, _ = parse_dataset_arg(dataset_arg)

    context = Context(user_required=True)
    client = SavviHubClient(token=context.token)

    dataset = client.dataset_read(workspace, dataset)
    if not dataset:
        typer.echo('[Error]Dataset not found!\n You should specify dataset with workspace. ex) savvihub/mnist')
        sys.exit(1)

    typer.echo(
        f'Name: {dataset.name}\n'
        f'Volume ID: {dataset.volume_id}\n'
        f'Workspace:\n'
        f'\tName: {dataset.workspace.name}'
    )

    source = dataset.source
    if source.type != DATASET_SOURCE_TYPE_SAVVIHUB:
        typer.echo(
            f'Source:\n'
            f'\tType: {source.type}\n'
            f'\tPath: {source.bucket_name}/{source.path}'
        )
        typer.echo(f'{client.get_full_info_dataset(dataset.workspace.name, dataset.name)}')
