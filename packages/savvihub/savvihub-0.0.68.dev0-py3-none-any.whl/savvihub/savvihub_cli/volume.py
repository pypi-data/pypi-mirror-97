import os
import sys
import time
from collections import defaultdict
from urllib.parse import urlparse

import typer
from terminaltables import AsciiTable

from savvihub import Context
from savvihub.api.savvihub import SavviHubClient
from savvihub.api.types import SavviHubVolume
from savvihub.api.uploader import Downloader, Uploader
from savvihub.common.utils import sizeof_fmt, remove_suffix

volume_app = typer.Typer()


class PathException(Exception):
    pass


def refine_volume_path(
    path_arg,
    raise_if_not_empty=False,
    raise_if_not_dir=False,
    raise_if_not_exist=False,
    remote_only=False,
):
    if path_arg.startswith('svds://'):
        typer.echo('[Error] Use \'sv://\' for volumes.')
        sys.exit(1)

    if path_arg.startswith('sv://'):
        return path_arg, True
    elif remote_only:
        return 'sv://' + path_arg, True

    path = os.path.abspath(path_arg)
    if os.path.exists(path):
        if not os.path.isdir(path) and raise_if_not_dir:
            raise PathException(f'Must specify directory: {path_arg}')
        if raise_if_not_empty and len(os.listdir(path)) > 0:
            raise PathException(f'Must specify empty directory: {path_arg}')
    else:
        if raise_if_not_exist:
            raise PathException(f'Must specify directory: {path_arg}')

    return path, False


def parse_remote_volume_path(remote_path: str) -> (SavviHubVolume, str, str):
    # sv://1:snapshot/path/to/files
    u = urlparse(remote_path)
    volume_snapshot = u.netloc
    split_snapshot = volume_snapshot.split(':', 1)
    volume_id = int(split_snapshot[0])
    file_path = u.path.lstrip('/')

    snapshot = split_snapshot[1] if len(split_snapshot) == 2 else 'latest'

    return volume_id, snapshot, file_path


@volume_app.callback()
def main():
    """
    Manage files in the volume
    """
    return


@volume_app.command()
def ls(
    source_path_arg: str = typer.Argument(...),
    recursive: bool = typer.Option(False, '-r', '--recursive', help='recursive flag'),
    directory: bool = typer.Option(False, '-d', '--directory', help='list the directory itself, not its contents')
):
    """
    List files in the dataset with prefix
    """
    try:
        source_path, is_source_remote = refine_volume_path(source_path_arg, raise_if_not_exist=True, remote_only=True)
    except PathException as e:
        typer.echo(str(e))
        return

    volume_id, snapshot, path = parse_remote_volume_path(source_path)
    volume_file_list(volume_id, snapshot, path, recursive, directory)
    return


@volume_app.command()
def rm(
    source_path_arg: str = typer.Argument(...),
    recursive: bool = typer.Option(False, '-r', '-R', '--recursive',
                                   help='Remove directories and their contents recursively'),
):
    """
    Remove files in the volume with path
    """
    try:
        source_path, is_source_remote = refine_volume_path(source_path_arg, raise_if_not_exist=True, remote_only=True)
    except PathException as e:
        typer.echo(str(e))
        return

    volume_id, snapshot, path = parse_remote_volume_path(source_path)
    volume_file_remove(volume_id, snapshot, path, recursive)


@volume_app.command()
def cp(
    source_path_arg: str = typer.Argument(...),
    dest_path_arg: str = typer.Argument(...),
    recursive: bool = typer.Option(False, '-r', '--recursive'),
    watch: bool = typer.Option(False, '-w', '--watch'),
):
    try:
        source_path, is_source_remote = refine_volume_path(source_path_arg, raise_if_not_exist=True)
        dest_path, is_dest_remote = refine_volume_path(dest_path_arg)
    except PathException as e:
        typer.echo(str(e))
        return

    source_volume_id = dest_volume_id = None
    source_snapshot = dest_snapshot = None
    if is_source_remote:
        source_volume_id, source_snapshot, source_path = parse_remote_volume_path(source_path)
    if is_dest_remote:
        dest_volume_id, dest_snapshot, dest_path = parse_remote_volume_path(dest_path)

    volume_file_copy(source_volume_id, source_snapshot, source_path,
                     dest_volume_id, dest_snapshot, dest_path,
                     recursive, watch)


def volume_file_list(volume_id: int, snapshot: str, path: str, recursive: bool, directory: bool):
    context = Context(auth_required=True)
    client = SavviHubClient(token=context.token)

    if recursive and directory:
        typer.echo('[Error] -r and -d options cannot be used in one command')
        return
    elif recursive:
        files = client.volume_file_list(volume_id, snapshot=snapshot, path=path, recursive=True)
    elif directory:
        if not path:
            typer.echo('[Error] path must be specified to run -d option')
            return
        file = client.volume_file_read(volume_id, path, snapshot)
        files = [file] if file is not None else None
    else:
        files = client.volume_file_list(volume_id, snapshot=snapshot, path=path, recursive=False)

    if files is None:
        typer.echo('No such file or directory.')
        return

    if len(files) == 0:
        typer.echo('This directory is empty.')
        return

    print_file_list(files, recursive)


def volume_file_remove(volume_id: int, snapshot: str, path: str, recursive: bool):
    context = Context(auth_required=True)
    client = SavviHubClient(token=context.token)

    file = client.volume_file_read(volume_id, path, snapshot)
    if file is None:
        typer.echo('[Error] Request entity not found')
        return

    if file.is_dir:
        if not recursive:
            typer.echo('[Error] Remove directory should use -r option')
            return
        deleted_files = client.volume_file_delete(volume_id, path, True)
    else:
        deleted_files = client.volume_file_delete(volume_id, path, False)

    if not deleted_files:
        typer.echo('[Error] Server error')
        return

    typer.echo('Successfully deleted files:')
    print_file_list(deleted_files, True)


def print_file_list(files, recursive):
    files = sorted(files, key=lambda f: f.path if recursive else (not f.is_dir, f.path))

    table_content = []
    for file in files:
        row = [file.path if recursive else file.path.rsplit('/', 1)[-1],
               '' if file.is_dir else sizeof_fmt(file.size)]
        if file.is_dir:
            row[0] += '/'
        table_content.append(row)

    table = AsciiTable(table_content)
    table.inner_column_border = False
    table.inner_heading_row_border = False
    table.inner_footing_row_border = False
    table.outer_border = False

    typer.echo(table.table)


def volume_file_copy(source_volume_id, source_snapshot, source_path, dest_volume_id, dest_snapshot, dest_path, recursive, watch):
    context = Context(auth_required=True)
    hashmap = defaultdict(lambda: '')
    client = context.authorized_client

    while True:
        if source_volume_id is not None and dest_volume_id is not None:
            # remote -> remote
            if source_volume_id != dest_volume_id:
                typer.echo('Currently files can be copied only within the same volume.')
                sys.exit(1)

            if dest_snapshot != 'latest':
                typer.echo(f'Cannot write to snapshots: {dest_path}')
                sys.exit(1)

            source_file = client.volume_file_read(source_volume_id, source_path, source_snapshot)
            if source_file is None:
                typer.echo(f'No such file or directory: {source_path}')
                sys.exit(1)

            if source_file.is_dir and not recursive:
                typer.echo(f'Source path is a directory, you should call with --recursive option.')
                sys.exit(1)

            dest_file = client.volume_file_read(dest_volume_id, dest_path, 'latest')
            if source_file.is_dir and dest_file is not None and not dest_file.is_dir:
                typer.echo(f'Source path is a directory, but destination path is a file.')
                sys.exit(1)

            client.volume_file_copy(
                source_volume_id, source_path, source_snapshot,
                dest_path, recursive=recursive,
            )

        elif source_volume_id is not None and dest_volume_id is None:
            # remote -> local
            source_file = client.volume_file_read(source_volume_id, source_path, source_snapshot)

            if source_file is None:
                typer.echo(f'Source file does not exist: {source_path}')
                sys.exit(1)

            if source_file.is_dir:
                if not recursive:
                    typer.echo(f'Source path is a directory, you should call with --recursive option.')
                    sys.exit(1)

                if os.path.exists(dest_path) and not os.path.isdir(dest_path):
                    typer.echo(f'Destination path is not a directory: {dest_path}')
                    sys.exit(1)

                # download directory
                typer.echo('Fetching file metadata...')
                files = client.volume_file_list(source_volume_id, path=source_path, snapshot=source_snapshot, recursive=True, need_download_url=True)
                files = [file for file in files if hashmap[file.path] != file.hash]

                if source_path.endswith('/'):
                    for file in files:
                        file.path = file.path.replace(source_path, '', 1)
                else:
                    dir_name = os.path.dirname(source_path)
                    for file in files:
                        if dir_name:
                            file.path = file.path.replace(dir_name + '/', '', 1)

                typer.echo(f'Found {len(files)} files to download.')
                if len(files) > 0:
                    typer.echo('Downloading...')
                    Downloader.bulk_download(context, dest_path, files, progressable=typer.progressbar)
                    for file in files:
                        hashmap[file.path] = file.hash
                    typer.echo('Successfully downloaded.')
            else:
                # download file
                dest_file_path = dest_path
                if os.path.isdir(dest_path):
                    dest_file_path = os.path.join(dest_path, os.path.basename(source_file.path))

                Downloader.download(dest_file_path, source_file, progressable=typer.progressbar)
                hashmap[source_file.path] = source_file.hash

        elif source_volume_id is None and dest_volume_id is not None:
            # local -> remote
            if not os.path.exists(source_path):
                typer.echo(f'No such file or directory: {source_path}')
                sys.exit(1)

            if dest_snapshot != 'latest':
                typer.echo(f'Cannot write to snapshots: {dest_path}')
                sys.exit(1)

            dest_file = client.volume_file_read(dest_volume_id, dest_path, dest_snapshot)
            if os.path.isdir(source_path):
                if not recursive:
                    typer.echo(f'Source path is a directory, you should call with --recursive option.')
                    sys.exit(1)

                files = Uploader.get_files_to_upload(source_path, hashmap)
                if dest_file is None:
                    # x/y/dir1/ -> c/ (not exist)
                    # x/y/dir1/file1/ -> c/file1
                    dest_base_path = dest_path
                elif dest_file.is_dir:
                    # x/y/dir1/ -> c/ (exist path)
                    # x/y/dir1/file1/ -> c/dir1/file1
                    if source_path.endswith('/'):
                        dest_base_path = dest_path
                    else:
                        dest_base_path = os.path.join(dest_path, os.path.basename(remove_suffix(source_path, "/")))
                else:
                    typer.echo(f'Destination path is not a directory: {dest_path}')
                    sys.exit(1)

                typer.echo(f'Found {len(files)} files to upload.')
                if len(files) > 0:
                    typer.echo('Uploading...')
                    Uploader.bulk_upload(context, source_path, files, dest_volume_id, dest_base_path, progressable=typer.progressbar)
                    hashmap = Uploader.get_hashmap(source_path)
                    typer.echo('Successfully uploaded.')
            else:
                # x/y/dir1/file1 ->
                if dest_file is None:
                    if dest_path.endswith('/'):
                        Uploader.upload(context, source_path, dest_volume_id, os.path.join(dest_path, os.path.basename(source_path)))
                    else:
                        Uploader.upload(context, source_path, dest_volume_id, dest_path)
                elif dest_file.is_dir:
                    Uploader.upload(context, source_path, dest_volume_id, os.path.join(dest_path, os.path.basename(source_path)))
                else:
                    Uploader.upload(context, source_path, dest_volume_id, dest_path)

        else:
            typer.echo('Use \'svds://\' scheme for remote files')
            return

        if not watch:
            return

        time.sleep(10)
