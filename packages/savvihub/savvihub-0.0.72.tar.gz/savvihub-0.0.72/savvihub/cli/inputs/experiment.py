import os
import tempfile
from typing import Optional, List

import inquirer
import requests
import typer

from openapi_client import (
    ProtoVolumeMountRequest,
    ProtoVolumeMountRequestSourceDataset,
    ProtoVolumeMountRequestSourceVolume,
)
from savvihub.api.exceptions import NotFoundAPIException
from savvihub.api.file_object import DownloadableFileObject
from savvihub.api.uploader import Uploader
from savvihub.cli.exceptions import ExitException
from savvihub.cli.typer import Context
from savvihub.cli.utils import find_from_inquirer, parse_dataset


def start_command_callback(start_command: str) -> str:
    if start_command:
        return start_command

    return inquirer.prompt([inquirer.Text(
        'start_command',
        message="Start command",
        default="python main.py",
    )]).get('start_command')


def cluster_name_callback(ctx: Context, cluster_name: str) -> str:
    assert ctx.params['workspace_name']

    clusters = [c for c in ctx.authenticated_client.cluster_list(ctx.params['workspace_name']).clusters
                if c.status == 'connected']
    if cluster_name:
        for cluster in clusters:
            if cluster.name == cluster_name.strip():
                ctx.store['cluster'] = cluster
                return cluster.name
        else:
            raise ExitException(f'Cluster not found: {cluster_name.strip()}')

    elif len(clusters) == 1:
        typer.echo(f'The cluster is automatically set to `{clusters[0].name}{" (SavviHub)" if clusters[0].is_savvihub_managed else f" ({clusters[0].kubernetes_master_endpoint})"}`.')
        ctx.store['cluster'] = clusters[0]
        return clusters[0].name

    else:
        selected_cluster = find_from_inquirer(
            clusters,
            lambda x: f'{x.name}{" (SavviHub)" if x.is_savvihub_managed else f" ({x.kubernetes_master_endpoint})"}',
            "Please choose a cluster"
        )
        ctx.store['cluster'] = selected_cluster

    return selected_cluster.name


def image_url_callback(ctx: Context, image_url: str) -> str:
    assert ctx.params['workspace_name'] and ctx.params['processor_type']

    images = ctx.authenticated_client.kernel_image_list(ctx.params['workspace_name']).results
    images = [i for i in images if i.processor_type == ctx.params['processor_type']]
    if image_url:
        for image in images:
            if image.image_url == image_url:
                return image_url
        else:
            raise ExitException(f'Image not found: {image_url}')

    return find_from_inquirer(
        images,
        lambda x: f'{x.image_url} ({x.name})',
        "Please choose a kernel image"
    ).image_url


def resource_name_callback(ctx: Context, resource_name: str) -> Optional[str]:
    assert ctx.params['workspace_name'] and ctx.store['cluster']

    if ctx.store['cluster'].is_savvihub_managed:
        resources = ctx.authenticated_client.kernel_resource_list(ctx.params['workspace_name']).results
        if resource_name:
            for resource in resources:
                if resource.name == resource_name.strip():
                    ctx.store['processor_type'] = resource.processor_type
                    ctx.store['resource_spec_id'] = resource.id
                    return resource.name
            else:
                raise ExitException(f'Resource not found: {resource_name.strip()}')
        else:
            selected_resource = find_from_inquirer(
                resources,
                lambda x: f'{x.name} ({x.description})',
                "Please choose a resource"
            )
            ctx.store['processor_type'] = selected_resource.processor_type
            ctx.store['resource_spec_id'] = selected_resource.id
            return selected_resource.name

    elif resource_name:
        raise ExitException('--resource option can be set only with a savvihub-managed cluster')

    return None


def processor_type_callback(ctx: Context, processor_type: str) -> str:
    assert ctx.store['cluster']

    if ctx.store['cluster'].is_savvihub_managed:
        return ctx.store['processor_type']

    if processor_type not in ['cpu', 'gpu']:
        processor_type = find_from_inquirer(
            ['cpu', 'gpu'],
            lambda x: x,
            "Please choose a processor type",
        )

    return processor_type


def cpu_limit_callback(ctx: Context, cpu_limit: float) -> Optional[float]:
    assert ctx.store['cluster']
    if ctx.store['cluster'].is_savvihub_managed:
        return 0

    if cpu_limit <= 0:
        cpu_limit = float(inquirer.prompt([inquirer.Text(
            'question',
            message="CPU limit (the number of vCPUs)",
            default=1.0,
        )]).get('question'))
        if cpu_limit <= 0:
            raise ExitException('Must be greater than 0')

    return cpu_limit


def memory_limit_callback(ctx: Context, memory_limit: float) -> Optional[float]:
    assert ctx.store['cluster']
    if ctx.store['cluster'].is_savvihub_managed:
        return None

    if memory_limit <= 0:
        memory_limit = float(inquirer.prompt([inquirer.Text(
            'question',
            message="Memory limit in GiB",
            default=4.0,
        )]).get('question'))
        if memory_limit <= 0:
            raise ExitException('Must be greater than 0')

    return memory_limit


def gpu_type_callback(ctx: Context, gpu_type: str) -> str:
    assert ctx.store['cluster'] and ctx.params['processor_type']
    if ctx.store['cluster'].is_savvihub_managed or ctx.params['processor_type'] != 'gpu':
        return 'Empty'

    if gpu_type:
        return gpu_type

    return inquirer.prompt([inquirer.Text(  # TODO: use find_from_inquirer
        'question',
        message="GPU type",
        default="Tesla-K80",
    )]).get('question')


def gpu_limit_callback(ctx: Context, gpu_limit: int) -> int:
    assert ctx.store['cluster'] and ctx.params['gpu_type']
    if ctx.store['cluster'].is_savvihub_managed or ctx.params['gpu_type'] == 'Empty':
        return 0

    if gpu_limit <= 0:
        gpu_limit = int(inquirer.prompt([inquirer.Text(
            'question',
            message="GPU limit (the number of GPUs)",
            default=1,
        )]).get('question'))
        if gpu_limit <= 0:
            raise ExitException('Must be greater than 0')

    return gpu_limit


def dataset_mount_callback(ctx: Context, dataset_mounts: List[str]) -> List[str]:
    client = ctx.authenticated_client
    workspace_name = ctx.params['workspace_name']
    ctx.store['dataset_mounts'] = []
    for dataset_mount in dataset_mounts:
        splitted = dataset_mount.split(':')
        if len(splitted) != 2:
            raise ExitException(f'Invalid dataset mount format: {dataset_mount}. '
                                f'You should specify both mount path and dataset name.\n'
                                f'ex) /input/dataset1:mnist@snapshot-3d1e0f91c')

        mount_path, dataset_full_name = splitted
        workspace_name_override, dataset_name, snapshot_name = parse_dataset(dataset_full_name)
        if workspace_name_override:
            workspace_name = workspace_name_override

        dataset = client.dataset_read(workspace_name, dataset_name)
        if snapshot_name != 'latest':
            try:
                client.snapshot_read(dataset.volume_id, snapshot_name)
            except NotFoundAPIException:
                raise ExitException(f'Invalid dataset snapshot: {dataset_full_name}\n'
                                    f'Please check your dataset and snapshot exist in workspace `{workspace_name}`.')

        ctx.store['dataset_mounts'].append(ProtoVolumeMountRequest(
            mount_type='dataset',
            mount_path=mount_path,
            dataset=ProtoVolumeMountRequestSourceDataset(
                dataset_id=dataset.id,
                snapshot_name=snapshot_name,
            ),
        ))

    return dataset_mounts


def volume_file_mount_callback(ctx: Context, volume_file_mounts: List[str]) -> List[str]:
    ctx.store['volume_file_mounts'] = []
    for volume_file_mount in volume_file_mounts:
        splitted = volume_file_mount.split(':')
        if len(splitted) != 2:
            raise ExitException(f'Invalid volume file mount format: {volume_file_mount}. '
                                f'You should specify both mount path and volume file.\n'
                                f'Volume file can be notated with volume id and subpath.'
                                f'ex) /input/model.pt:1#subPath=f72fca375e812/model.pt')

        mount_path, volume_id = splitted
        if '#subPath=' in volume_id:
            volume_id, sub_path = volume_id.split('#subPath=')
        else:
            sub_path = ''

        try:
            volume_id = int(volume_id)
        except ValueError:
            raise ExitException(f'Volume id should be an integer.')

        try:
            ctx.authenticated_client.volume_read(volume_id)
        except NotFoundAPIException:
            raise ExitException(f'Volume not found: {volume_id}')

        ctx.store['volume_file_mounts'].append(ProtoVolumeMountRequest(
            mount_type='volume',
            mount_path=mount_path,
            volume=ProtoVolumeMountRequestSourceVolume(
                volume_id=volume_id,
                sub_path=sub_path,
            )
        ))

    return volume_file_mounts


def env_vars_callback(ctx: Context, env_vars: List[str]) -> List[str]:
    ctx.store['env_vars'] = []
    for env_var in env_vars:
        try:
            env_key, env_value = env_var.split("=", 1)
            ctx.store['env_vars'].append({
                'key': env_key,
                'value': env_value,
            })
        except ValueError:
            raise ExitException(f'Cannot parse environment variable: {env_var}')

    return env_vars


def git_ref_callback(ctx: Context, git_ref: str) -> str:
    if git_ref:
        git_ref = git_ref.strip()
        if ctx.git_repo and not ctx.git_repo.check_revision_in_remote(git_ref):
            raise ExitException(f'Git commit {git_ref} does not exist in a remote repository.')
        return git_ref

    if ctx.git_repo is None:
        raise ExitException('Run it inside a git-initialized directory or set --git-ref option.')

    return ctx.git_repo.commit_ref


def git_diff_callback(ctx: Context, git_diff_url: str) -> Optional[str]:
    assert ctx.params['git_ref']
    if ctx.params['ignore_git_diff']:
        return None

    diff_file = None
    if git_diff_url:
        if git_diff_url.startswith('https://') or git_diff_url.startswith('http://'):
            diff_file = tempfile.NamedTemporaryFile(suffix='.patch')
            d = DownloadableFileObject(git_diff_url, os.path.dirname(diff_file.name), os.path.basename(diff_file.name))
            session = requests.Session()
            session.headers = ctx.authenticated_client.auth_header
            d.download(session=session)
            diff_file.seek(0)
    else:
        if ctx.git_repo is None:
            return None

        typer.echo(f'Run experiment with revision {ctx.git_repo.commit_ref[:7]} ({ctx.git_repo.branch})')
        typer.echo(f'Commit: {ctx.git_repo.get_commit_message(ctx.git_repo.commit_ref)}')
        if not ctx.git_repo.is_head:
            typer.echo('Your current revision does not exist in remote repository. '
                       'SavviHub will use latest remote branch revision hash and uncommitted diff.')
        typer.echo('')

        has_diff, diff_status = ctx.git_repo.get_current_diff_status(ctx.git_repo.commit_ref)
        if has_diff:
            typer.echo('Diff to be uploaded: ')

            uncommitted_files = diff_status.get('uncommitted')
            untracked_files = diff_status.get('untracked')

            if uncommitted_files:
                typer.echo('  Changes not committed')
                typer.echo('\n'.join([f'    {x}' for x in uncommitted_files]))
                typer.echo('')
            if untracked_files:
                typer.echo(f'  Untracked files:')
                typer.echo('\n'.join([f'    {x}' for x in untracked_files]))
                typer.echo('')

            answer = inquirer.prompt([inquirer.List(
                'question',
                message='Run experiment with diff?',
                choices=[
                    ('[1] Run experiment with uncommitted and untracked changes.', 1),
                    ('[2] Run experiment with uncommitted changes.', 2),
                    ('[3] Run experiment without any changes.', 3),
                    ('[4] Abort.', 4),
                ],
            )])['question']

            if answer == 1:
                diff_file = ctx.git_repo.get_current_diff_file(ctx.git_repo.commit_ref, with_untracked=True)
            elif answer == 2:
                diff_file = ctx.git_repo.get_current_diff_file(ctx.git_repo.commit_ref, with_untracked=False)
            elif answer == 3:
                pass
            else:
                raise ExitException('Aborted.')

    if diff_file:
        typer.echo('Generating diff patch file...')
        uploaded = Uploader.upload(
            ctx,
            local_path=diff_file.name,
            volume_id=ctx.project.volume_id,
            remote_path=os.path.basename(diff_file.name),
            progressable=typer.progressbar,
        )
        diff_file_path = uploaded.path
        diff_file.close()

        ctx.store['git_diff_uploaded_path'] = diff_file_path

    return git_diff_url
