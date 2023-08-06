from urllib.parse import urlparse

import typer
from terminaltables import AsciiTable

from savvihub.cli.commands.dataset_files import dataset_files_app
from savvihub.cli.constants import (
    DATASET_PATH_PARSE_SCHEME_GS,
    DATASET_PATH_PARSE_SCHEME_S3,
    DATASET_SOURCE_TYPE_AWS_S3,
    DATASET_SOURCE_TYPE_GCP_GS,
    WEB_HOST,
)
from savvihub.cli.exceptions import ExitException
from savvihub.cli.inputs.workspace import workspace_name_option
from savvihub.cli.typer import Typer, Context
from savvihub.cli.utils import parse_dataset

dataset_app = Typer()
dataset_app.add_typer(dataset_files_app, name='files')


@dataset_app.callback()
def main():
    """
    Manage the collection of data
    """
    return


@dataset_app.command(user_required=True)
def list(
    ctx: Context,
    workspace_name: str = workspace_name_option,
):
    """
    Show datasets
    """
    client = ctx.authenticated_client
    dataset_list = client.dataset_list(workspace_name).results
    if len(dataset_list) == 0:
        typer.echo(f'No datasets found in `{workspace_name}` workspace.')
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


@dataset_app.command(user_required=True)
def create(
    ctx: Context,
    workspace_name: str = workspace_name_option,
    dataset_name: str = typer.Argument(...),
    path_arg: str = typer.Option(None, "-u", "--url", help="S3 or GoogleStorage url starting with s3:// or gs://."),
    aws_role_arn: str = typer.Option(None, "--aws-role-arn", help="Required to create S3 dataset."),
    description: str = typer.Option(None, "-m", help="Dataset description."),
):
    """
    Create a dataset
    """
    client = ctx.authenticated_client

    if path_arg:
        if not (path_arg.startswith("gs://") or path_arg.startswith("s3://")):
            raise ExitException(f"path should start with \"gs://\" or \"s3://\"")

        r = urlparse(path_arg)
        if r.scheme == DATASET_PATH_PARSE_SCHEME_GS:
            dataset = client.dataset_gs_create(workspace_name, dataset_name, False, description, path_arg)
        elif r.scheme == DATASET_PATH_PARSE_SCHEME_S3:
            if not aws_role_arn:
                raise ExitException("AWS Role ARN is required for S3 users")
            dataset = client.dataset_s3_create(workspace_name, dataset_name, False, description, path_arg, aws_role_arn)
        else:
            raise ExitException("Only Google Cloud Storage and Amazon S3 are supported at the moment.")
    else:
        dataset = client.dataset_create(workspace_name, dataset_name, False, description)

    if not dataset:
        return

    if dataset_name != dataset.name:
        typer.echo(f'Duplicate dataset name: {dataset_name}')

    typer.echo(
        f'Dataset {dataset.name} is created.\n'
        f'Full dataset info at:\n'
        f'    {WEB_HOST}/{dataset.workspace.name}/datasets/{dataset.name}\n'
    )


@dataset_app.command(user_required=True)
def describe(
    ctx: Context,
    workspace_name: str = workspace_name_option,
    dataset_name: str = typer.Argument(...),
):
    """
    Describe the dataset information in detail
    """
    workspace_name_override, dataset_name, _ = parse_dataset(dataset_name)
    if workspace_name_override:
        workspace_name = workspace_name_override

    dataset = ctx.authenticated_client.dataset_read(workspace_name, dataset_name)
    typer.echo(
        f'Name: {dataset.name}\n'
        f'Volume ID: {dataset.volume_id}\n'
        f'Workspace: {dataset.workspace.name}'
    )

    source = dataset.source
    if source.type == DATASET_SOURCE_TYPE_AWS_S3:
        typer.echo(f'Source: s3://{source.bucket_name}/{source.path}')
    elif source.type == DATASET_SOURCE_TYPE_GCP_GS:
        typer.echo(f'Source: gs://{source.bucket_name}/{source.path}')

    typer.echo(
        '\n'
        f'Full dataset info at:\n'
        f'    {WEB_HOST}/{dataset.workspace.name}/datasets/{dataset.name}\n'
    )
