from datetime import datetime
from typing import List

import typer
from terminaltables import AsciiTable

from openapi_client import (
    ProtoVolumeMountRequest,
    ProtoVolumeMountRequestSourceProject,
    ProtoVolumeMountRequests,
)
from savvihub.cli.commands.volume import volume_file_list, volume_file_copy
from savvihub.cli.constants import WEB_HOST
from savvihub.cli.exceptions import ExitException
from savvihub.cli.formatter import TreeFormatter
from savvihub.cli.inputs.experiment import (
    cluster_name_callback,
    cpu_limit_callback,
    dataset_mount_callback,
    env_vars_callback,
    git_diff_callback,
    git_ref_callback,
    gpu_limit_callback,
    gpu_type_callback,
    image_url_callback,
    memory_limit_callback,
    processor_type_callback,
    resource_name_callback,
    start_command_callback,
    volume_file_mount_callback,
)
from savvihub.cli.inputs.project import project_name_option
from savvihub.cli.inputs.workspace import workspace_name_option
from savvihub.cli.typer import Typer, Context
from savvihub.common.utils import (
    parse_time_to_ago,
    short_string,
)

experiment_output_app = Typer()
experiment_app = Typer()
experiment_app.add_typer(experiment_output_app, name='output')


@experiment_app.callback()
def main():
    """
    Run the machine learning experiment
    """
    return


@experiment_app.command(user_required=True)
def list(
    ctx: Context,
    workspace_name: str = workspace_name_option,
    project_name: str = project_name_option,
):
    """
    Display a list of experiments
    """
    experiments = ctx.authenticated_client.experiment_list(workspace_name, project_name).results
    if not experiments:
        raise ExitException(f'There is no experiment in `{project_name}` project.')

    table = AsciiTable([
        ['NUMBER', 'NAME', 'STATUS', 'CREATED', 'IMAGE', 'RESOURCE', 'START COMMAND'],
        *[[e.number, e.name, e.status, parse_time_to_ago(e.created_dt),  short_string(e.kernel_image.name, 25),
           e.kernel_resource_spec.name, f'"{short_string(e.start_command, 25)}"']
          for e in experiments],
    ])
    table.inner_column_border = False
    table.inner_heading_row_border = False
    table.inner_footing_row_border = False
    table.outer_border = False

    typer.echo(table.table)


@experiment_app.command(user_required=True)
def describe(
    ctx: Context,
    workspace_name: str = workspace_name_option,
    project_name: str = project_name_option,
    experiment_number_or_name: str = typer.Argument(..., help="The unique experiment number or name"),
):
    """
    Describe the experiment in details
    """
    experiment = ctx.authenticated_client.experiment_read(workspace_name, project_name, experiment_number_or_name)
    timezone = datetime.now().astimezone().tzinfo

    root = TreeFormatter()
    root.add_child(f'Number: {experiment.number}',
                   f'Name: {experiment.name}',
                   f'Created: {experiment.created_dt.astimezone(timezone)}',
                   f'Updated: {experiment.updated_dt.astimezone(timezone)}',
                   f'Git Commit: ({experiment.git_ref[:7]}) {experiment.message}')

    if experiment.source_code_link:
        root.add_child(f'Source code link: {experiment.source_code_link[0].url}')

    if experiment.git_diff_file:
        git_diff_file_desc = TreeFormatter('Git Diff File:')
        git_diff_file_desc.add_child(f'URL: {experiment.git_diff_file.download_url["url"]}')
        root.add_child(git_diff_file_desc)

    root.add_child(f'Status: {experiment.status}',
                   f'Tensorboard: {experiment.tensorboard or "N/A"}')

    # Kernel Image Description
    kernel_image_desc = TreeFormatter('Kernel Image:')
    kernel_image_desc.add_child(f'Name: {experiment.kernel_image.name}',
                                f'URL: {experiment.kernel_image.image_url}',
                                f'Language: {experiment.kernel_image.language or "N/A"}')
    root.add_child(kernel_image_desc)

    # Resource Spec Description
    resource_spec_desc = TreeFormatter('Resource Spec:')
    resource_spec_desc.add_child(f'Name: {experiment.kernel_resource_spec.name}',
                                 f'CPU Type: {experiment.kernel_resource_spec.name}',
                                 f'CPU Limit: {experiment.kernel_resource_spec.cpu_limit}',
                                 f'Memory Limit: {experiment.kernel_resource_spec.memory_limit}',
                                 f'GPU Type: {experiment.kernel_resource_spec.gpu_type}',
                                 f'GPU Limit: {experiment.kernel_resource_spec.gpu_limit}')
    root.add_child(resource_spec_desc)

    # Datasets Description
    datasets_desc = TreeFormatter('Datasets:')
    found = False
    for volume_mount in experiment.volume_mounts.mounts:
        if volume_mount.source_type == 'dataset':
            dataset_desc = TreeFormatter(volume_mount.dataset.dataset.name)
            dataset_desc.add_child(f'Mount Path: {volume_mount.path}')
            datasets_desc.add_child(dataset_desc)
            found = True
    if not found:
        datasets_desc.add_child('Dataset Not Found')
    root.add_child(datasets_desc)

    # Histories Description
    histories_desc = TreeFormatter('Histories:')
    if not experiment.histories:
        histories_desc.add_child('History Not Found')
    else:
        for history in experiment.histories:
            history_desc = TreeFormatter(history.status)
            history_desc.add_child(f'Started: {datetime.fromtimestamp(history.started_timestamp, tz=timezone).strftime("%Y-%m-%d %H:%M:%S.%f%z")}',
                                   f'Ended: {datetime.fromtimestamp(history.ended_timestamp, tz=timezone).strftime("%Y-%m-%d %H:%M:%S.%f%z") if history.ended_timestamp else "N/A"}')
            histories_desc.add_child(history_desc)
    root.add_child(histories_desc)

    # Metrics Description
    metrics_desc = TreeFormatter('Metrics:')
    if not experiment.metrics_summary.latest:
        metrics_desc.add_child('Metrics Not Found')
    else:
        # TODO
        # for history in experiment.metrics_summary.latest:
        #     metrics_desc.add_child(history)

        full_metrics_info_desc = TreeFormatter('Full metrics at:')
        full_metrics_info_desc.add_child(f'{WEB_HOST}/{workspace_name}/{project_name}/experiments/{experiment.number}/metrics')
        metrics_desc.add_child(full_metrics_info_desc)
    root.add_child(metrics_desc)

    # System Metrics Description
    system_metrics_desc = TreeFormatter('System Metrics:')
    full_system_metrics_info_desc = TreeFormatter('Full system metrics at:')
    full_system_metrics_info_desc.add_child(f'{WEB_HOST}/{workspace_name}/{project_name}/experiments/{experiment.number}/system-metrics')
    system_metrics_desc.add_child(full_system_metrics_info_desc)
    root.add_child(system_metrics_desc)
    root.add_child(f'Start Command: {experiment.start_command}')

    typer.echo(root.format())


@experiment_app.command(user_required=True)
def logs(
    ctx: Context,
    workspace_name: str = workspace_name_option,
    project_name: str = project_name_option,
    experiment_number_or_name: str = typer.Argument(..., help="The unique experiment number or name"),
    tail: int = typer.Option(200, "--tail"),
    detail: bool = typer.Option(False, "--detail", hidden=True),
    all: bool = typer.Option(False, "--all", hidden=True),
):
    """
    Display the last fifty lines of the experiment logs
    """
    client = ctx.authenticated_client

    kwargs = {}
    if not all:
        kwargs = {'limit': tail}
    if detail:
        kwargs = {'with_event_log': 'true'}

    experiment_logs = client.experiment_log(
        workspace_name, project_name, experiment_number_or_name, **kwargs).logs

    all_logs = []
    for _, logs in experiment_logs.items():
        all_logs.extend(logs)

    timezone = datetime.now().astimezone().tzinfo
    log_str = ''
    for log in sorted(all_logs, key=lambda x: x.timestamp):
        log_str += f'[{datetime.fromtimestamp(log.timestamp, tz=timezone).strftime("%H:%M:%S.%f")}] {log.message}\n'

    typer.echo(log_str)
    typer.echo(
        f'Full logs at:\n'
        f'    {WEB_HOST}/{workspace_name}/{project_name}/experiments/{experiment_number_or_name}/logs\n'
    )


@experiment_app.command(user_required=True)
def run(
    ctx: Context,
    workspace_name: str = workspace_name_option,
    project_name: str = project_name_option,
    start_command: str = typer.Option(None, "--start-command", callback=start_command_callback,
                                      help="Start command"),
    cluster_name: str = typer.Option(None, "--cluster", "-c", callback=cluster_name_callback,
                                     help="Cluster name"),
    resource_name: str = typer.Option(None, "--resource", "-r", callback=resource_name_callback,
                                      help="Resource name (for savvihub-managed cluster)"),
    processor_type: str = typer.Option(None, "--processor-type", callback=processor_type_callback,
                                       help="cpu or gpu (for custom cluster)"),
    image_url: str = typer.Option(None, "--image", "-i", callback=image_url_callback,
                                  help="Kernel docker image URL"),
    cpu_limit: float = typer.Option(0, "--cpu-limit", callback=cpu_limit_callback,
                                    help="Number of vCPUs (for custom cluster)"),
    memory_limit: str = typer.Option(None, "--memory-limit", callback=memory_limit_callback,
                                     help="Memory capacity (ex: 4Gi, 500Mi)"),
    gpu_type: str = typer.Option(None, "--gpu-type", callback=gpu_type_callback,
                                 help="GPU product name such as Tesla-K80 (for custom cluster)"),
    gpu_limit: int = typer.Option(0, "--gpu-limit", callback=gpu_limit_callback,
                                  help="Number of GPU cores (for custom cluster)"),
    dataset_mounts: List[str] = typer.Option([], "--dataset", "-d", callback=dataset_mount_callback,
                                             help="Dataset mounted path"),
    volume_file_mounts: List[str] = typer.Option([], "--volume-file", callback=volume_file_mount_callback, hidden=True),
    env_vars: List[str] = typer.Option([], "-e", callback=env_vars_callback, help="Environment variables"),
    ignore_git_diff: bool = typer.Option(False, "--ignore-git-diff", help="Ignore git diff flag"),
    git_branch: str = typer.Option(None, "--git-branch", help="Git branch name"),
    git_ref: str = typer.Option(None, "--git-ref", callback=git_ref_callback, help="Git commit SHA"),
    git_diff_arg: str = typer.Option(None, "--git-diff", callback=git_diff_callback, help="Git diff file URL"),
    output_dir: str = typer.Option("/output/", "--output-dir",
                                   help="A directory to which the experiment result output files to be stored."),
    working_dir: str = typer.Option(None, "--working-dir", help="If not present, use `/work/{project_name}`."),
    root_volume_size: str = typer.Option(None, "--root-volume-size", help="Root volume size"),
):
    """
    Run an experiment in SavviHub
    """
    resource_spec = resource_spec_id = None
    if ctx.store['cluster'].is_savvihub_managed:
        resource_spec_id = ctx.store['resource_spec_id']
    else:
        resource_spec = {
            'processor_type': processor_type,
            'cpu_type': 'Any',
            'cpu_limit': cpu_limit,
            'memory_limit': memory_limit,
            'gpu_type': gpu_type,
            'gpu_limit': gpu_limit,
        }

    experiment = ctx.authenticated_client.experiment_create(
        workspace=workspace_name,
        project=project_name,
        cluster_name=ctx.store['cluster'].name,
        image_url=image_url,
        resource_spec_id=resource_spec_id,
        resource_spec=resource_spec,
        start_command=start_command,
        env_vars=ctx.store['env_vars'],
        volume_mounts=ProtoVolumeMountRequests(
            root_volume_size=root_volume_size,
            working_dir=working_dir,
            requests=ctx.store['dataset_mounts'] + ctx.store['volume_file_mounts'] + [
                ProtoVolumeMountRequest(
                    mount_type='empty-dir',
                    mount_path='/work/'
                ),
                ProtoVolumeMountRequest(
                    mount_type='output',
                    mount_path=output_dir,
                ),
                ProtoVolumeMountRequest(
                    mount_type='project',
                    mount_path=f'/work/{project_name}/',
                    project=ProtoVolumeMountRequestSourceProject(
                        project_id=ctx.project.id,
                        project_branch=git_branch or ctx.git_repo.branch,
                        project_git_ref=git_ref,
                        project_git_diff=ctx.store.get('git_diff_uploaded_path'),
                    ),
                ),
            ],
        ),
    )

    typer.echo(
        f'Experiment {experiment.number} is running. Check the experiment status at below link\n'
        f'{WEB_HOST}/{workspace_name}/{project_name}/experiments/{experiment.number}'
    )


@experiment_output_app.callback()
def output_main():
    """
    Manage experiment output files
    """


@experiment_output_app.command(user_required=True)
def ls(
    ctx: Context,
    workspace_name: str = workspace_name_option,
    project_name: str = project_name_option,
    experiment_number_or_name: str = typer.Argument(..., help="The unique experiment number or name"),
    path: str = typer.Argument(None, help='Output file path'),
    recursive: bool = typer.Option(False, '-r', '--recursive', help='recursive flag'),
    directory: bool = typer.Option(False, '-d', '--directory',
                                   help='list the directory itself, not its contents'),
):
    """
    List the output files of the experiment
    """
    experiment = ctx.authenticated_client.experiment_read(workspace_name, project_name, experiment_number_or_name)
    for volume_mount in experiment.volume_mounts.mounts:
        if volume_mount.source_type == 'output':
            volume_file_list(ctx, volume_mount.volume.volume.id, 'latest', path or '', recursive, directory)
    else:
        raise ExitException('No output volume mounted.')


@experiment_output_app.command(user_required=True)
def download(
    ctx: Context,
    workspace_name: str = workspace_name_option,
    project_name: str = project_name_option,
    experiment_number_or_name: str = typer.Argument(..., help="The unique experiment number or name"),
    dest_path: str = typer.Argument(None, help='The files will be downloaded to ./output if omitted.'),
):
    """
    Download experiment output files
    """
    experiment = ctx.authenticated_client.experiment_read(workspace_name, project_name, experiment_number_or_name)
    for volume_mount in experiment.volume_mounts.mounts:
        if volume_mount.source_type == 'output':
            volume_file_copy(
                ctx, volume_mount.volume.volume.id,
                'latest', '', None, None, dest_path or './output',
                recursive=True, watch=False)
            break
    else:
        raise ExitException('No output volume mounted.')
