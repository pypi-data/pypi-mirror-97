import os
import sys
from urllib.parse import urlparse

import typer

from savvihub import Context
from savvihub.api.savvihub import SavviHubClient
from savvihub.api.types import SavviHubDataset
from savvihub.savvihub_cli.volume import volume_file_list, volume_file_remove, volume_file_copy

dataset_files_app = typer.Typer()


class PathException(Exception):
    pass


def refine_dataset_path(
    path_arg,
    raise_if_not_empty=False,
    raise_if_not_dir=False,
    raise_if_not_exist=False,
    remote_only=False,
):
    if path_arg.startswith('sv://'):
        typer.echo('[Error] Use \'svds://\' for datasets.')
        sys.exit(1)

    if path_arg.startswith('svds://') or remote_only:
        path_arg = path_arg.replace('svds://', '')
        if path_arg.strip('/').count('/') == 0:
            typer.echo('[Error] Dataset not found!\n You should specify dataset with workspace. ex) savvihub/mnist')
            sys.exit(1)
        return 'svds://' + path_arg, True

    path = os.path.abspath(path_arg)
    if path_arg.endswith('/'):
        path += '/'

    if os.path.exists(path):
        if not os.path.isdir(path) and raise_if_not_dir:
            raise PathException(f'Must specify directory: {path_arg}')
        if raise_if_not_empty and len(os.listdir(path)) > 0:
            raise PathException(f'Must specify empty directory: {path_arg}')
    else:
        if raise_if_not_exist:
            raise PathException(f'Must specify directory: {path_arg}')

    return path, False


def parse_remote_dataset_path(remote_path: str) -> (SavviHubDataset, str, str):
    u = urlparse(remote_path)
    workspace = u.netloc
    path = u.path.lstrip('/')
    split_path = path.split('/', 1)
    split_snapshot = split_path[0].split(':', 1)

    file_path = split_path[1] if len(split_path) == 2 else ''
    snapshot = split_snapshot[1] if len(split_snapshot) == 2 else 'latest'

    return get_dataset(workspace, split_snapshot[0]), snapshot, file_path


def get_dataset(workspace: str, dataset: str) -> SavviHubDataset:
    context = Context(user_required=True)
    client = context.authorized_client

    r = client.dataset_read(workspace, dataset)
    if not r:
        typer.echo('[Error] Dataset not found!\n You should specify dataset with workspace. ex) savvihub/mnist')
        sys.exit(1)
    return r


@dataset_files_app.callback()
def main():
    """
    Manage files in the dataset
    """
    return


@dataset_files_app.command()
def ls(
    source_path_arg: str = typer.Argument(...),
    recursive: bool = typer.Option(False, '-r', '--recursive', help='recursive flag'),
    directory: bool = typer.Option(False, '-d', '--directory', help='list the directory itself, not its contents')
):
    """
    List files in the dataset with prefix
    """
    try:
        source_path, is_source_remote = refine_dataset_path(source_path_arg, raise_if_not_exist=True, remote_only=True)
    except PathException as e:
        typer.echo(str(e))
        return

    dataset, snapshot, path = parse_remote_dataset_path(source_path)
    volume_file_list(dataset.volume_id, snapshot, path, recursive, directory)


@dataset_files_app.command()
def rm(
    source_path_arg: str = typer.Argument(...),
    recursive: bool = typer.Option(False, '-r', '-R', '--recursive',
                                   help='Remove directories and their contents recursively'),
):
    """
    Remove files in the volume with path
    """
    try:
        source_path, is_source_remote = refine_dataset_path(source_path_arg, raise_if_not_exist=True, remote_only=True)
    except PathException as e:
        typer.echo(str(e))
        return

    dataset, snapshot, path = parse_remote_dataset_path(source_path)
    volume_file_remove(dataset.volume_id, snapshot, path, recursive)


@dataset_files_app.command()
def cp(
    source_path_arg: str = typer.Argument(...),
    dest_path_arg: str = typer.Argument(...),
    recursive: bool = typer.Option(False, '-r', '--recursive'),
    watch: bool = typer.Option(False, '-w', '--watch'),
):
    try:
        source_path, is_source_remote = refine_dataset_path(source_path_arg, raise_if_not_exist=True)
        dest_path, is_dest_remote = refine_dataset_path(dest_path_arg)
    except PathException as e:
        typer.echo(str(e))
        return

    source_volume_id = dest_volume_id = None
    source_snapshot = dest_snapshot = None
    if is_source_remote:
        source_dataset, source_snapshot, source_path = parse_remote_dataset_path(source_path)
        source_volume_id = source_dataset.volume_id
    if is_dest_remote:
        dest_dataset, dest_snapshot, dest_path = parse_remote_dataset_path(dest_path)
        dest_volume_id = dest_dataset.volume_id

    volume_file_copy(source_volume_id, source_snapshot, source_path,
                     dest_volume_id, dest_snapshot, dest_path,
                     recursive, watch)
