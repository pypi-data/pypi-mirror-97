import typer

from savvihub.api.exceptions import NotFoundAPIException
from savvihub.cli.commands.volume import volume_file_list, volume_file_remove, volume_file_copy
from savvihub.cli.exceptions import ExitException
from savvihub.cli.inputs.workspace import workspace_name_option
from savvihub.cli.typer import Typer, Context
from savvihub.cli.utils import parse_dataset

dataset_files_app = Typer()


@dataset_files_app.callback()
def main():
    """
    Manage files in the dataset
    """
    return


@dataset_files_app.command(user_required=True)
def ls(
    ctx: Context,
    dataset_full_name: str = typer.Argument(..., metavar='DATASET',
                                            help='{workspace}/{dataset}@{snapshot} format '
                                                 'where workspace and snapshot are optional.'),
    path: str = typer.Argument('/'),
    workspace_name: str = workspace_name_option,
    recursive: bool = typer.Option(False, '-r', '--recursive', help='recursive flag'),
    directory: bool = typer.Option(False, '-d', '--directory', help='list the directory itself, not its contents')
):
    """
    List files in the dataset with prefix
    """
    workspace_name_override, dataset_name, snapshot_name = parse_dataset(dataset_full_name)
    if workspace_name_override:
        workspace_name = workspace_name_override

    dataset = ctx.authenticated_client.dataset_read(workspace_name, dataset_name)
    volume_file_list(ctx, dataset.volume_id, snapshot_name, path, recursive, directory)


@dataset_files_app.command(user_required=True)
def rm(
    ctx: Context,
    dataset_full_name: str = typer.Argument(..., metavar='DATASET_NAME'),
    path: str = typer.Argument(...),
    workspace_name: str = workspace_name_option,
    recursive: bool = typer.Option(False, '-r', '-R', '--recursive',
                                   help='Remove directories and their contents recursively'),
):
    """
    Remove files in a dataset (SavviHub dataset files only)
    """
    workspace_name_override, dataset_name, snapshot_name = parse_dataset(dataset_full_name)
    if workspace_name_override:
        workspace_name = workspace_name_override

    if snapshot_name != 'latest':
        raise ExitException('Files in a snapshot cannot be removed.')

    dataset = ctx.authenticated_client.dataset_read(workspace_name, dataset_name)
    volume_file_remove(ctx, dataset.volume_id, path, recursive)


@dataset_files_app.command(user_required=True)
def upload(
    ctx: Context,
    dataset_full_name: str = typer.Argument(..., metavar='DATASET_NAME'),
    source_path: str = typer.Argument(...),
    dest_path: str = typer.Argument(...),
    workspace_name: str = workspace_name_option,
    recursive: bool = typer.Option(False, '-r', '--recursive'),
    watch: bool = typer.Option(False, '-w', '--watch'),
):
    """
    Upload files to a dataset (SavviHub dataset only)
    """
    workspace_name_override, dataset_name, snapshot_name = parse_dataset(dataset_full_name)
    if workspace_name_override:
        workspace_name = workspace_name_override

    if snapshot_name != 'latest':
        raise ExitException('Files in a snapshot cannot be removed.')

    dataset = ctx.authenticated_client.dataset_read(workspace_name, dataset_name)
    volume_file_copy(
        ctx,
        source_volume_id=None,
        source_snapshot=None,
        source_path=source_path,
        dest_volume_id=dataset.volume_id,
        dest_snapshot='latest',
        dest_path=dest_path,
        recursive=recursive,
        watch=watch,
    )


@dataset_files_app.command(user_required=True)
def download(
    ctx: Context,
    dataset_full_name: str = typer.Argument(..., metavar='DATASET',
                                            help='{workspace}/{dataset}@{snapshot} format '
                                                 'where workspace and snapshot are optional.'),
    source_path: str = typer.Argument(...),
    dest_path: str = typer.Argument('.'),
    workspace_name: str = workspace_name_option,
    recursive: bool = typer.Option(False, '-r', '--recursive'),
    watch: bool = typer.Option(False, '-w', '--watch'),
):
    """
    Download files from a dataset
    """
    workspace_name_override, dataset_name, snapshot_name = parse_dataset(dataset_full_name)
    if workspace_name_override:
        workspace_name = workspace_name_override

    dataset = ctx.authenticated_client.dataset_read(workspace_name, dataset_name)
    if snapshot_name != 'latest':
        try:
            ctx.authenticated_client.snapshot_read(dataset.volume_id, snapshot_name)
        except NotFoundAPIException:
            raise ExitException(f'Invalid dataset snapshot: {dataset_full_name}\n'
                                f'Please check your dataset and snapshot exist in workspace `{workspace_name}`.')
    volume_file_copy(
        ctx,
        source_volume_id=dataset.volume_id,
        source_snapshot=snapshot_name,
        source_path=source_path,
        dest_volume_id=None,
        dest_snapshot=None,
        dest_path=dest_path,
        recursive=recursive,
        watch=watch,
    )


@dataset_files_app.command(user_required=True)
def cp(
    ctx: Context,
    dataset_full_name: str = typer.Argument(..., metavar='DATASET',
                                            help='{workspace}/{dataset}@{snapshot} format '
                                                 'where workspace and snapshot are optional. '
                                                 'If a snapshot is specified, '
                                                 'copies the files from the snapshot to the current dataset.'),
    source_path: str = typer.Argument(...),
    dest_path: str = typer.Argument(...),
    workspace_name: str = workspace_name_option,
    recursive: bool = typer.Option(False, '-r', '--recursive'),
    watch: bool = typer.Option(False, '-w', '--watch'),
):
    """
    Copy files within a dataset (SavviHub dataset files only)
    """
    workspace_name_override, dataset_name, src_snapshot_name = parse_dataset(dataset_full_name)
    if workspace_name_override:
        workspace_name = workspace_name_override

    dataset = ctx.authenticated_client.dataset_read(workspace_name, dataset_name)
    if src_snapshot_name != 'latest':
        try:
            ctx.authenticated_client.snapshot_read(dataset.volume_id, src_snapshot_name)
        except NotFoundAPIException:
            raise ExitException(f'Invalid dataset snapshot: {dataset_full_name}\n'
                                f'Please check your dataset and snapshot exist in workspace `{workspace_name}`.')
    volume_file_copy(
        ctx,
        source_volume_id=dataset.volume_id,
        source_snapshot=src_snapshot_name,
        source_path=source_path,
        dest_volume_id=dataset.volume_id,
        dest_snapshot='latest',
        dest_path=dest_path,
        recursive=recursive,
        watch=watch,
    )
