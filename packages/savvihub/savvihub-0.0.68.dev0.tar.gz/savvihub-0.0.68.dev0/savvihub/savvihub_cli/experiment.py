import os
import pathlib
import re
import sys
import tempfile
from typing import List

import inquirer
import typer

from terminaltables import AsciiTable

from savvihub.api.file_object import DownloadableFileObject
from savvihub.api.uploader import Uploader
from savvihub.common.constants import INQUIRER_NAME_COMMAND, WEB_HOST, API_HOST, INQUIRER_NAME_CPU_LIMIT, \
    INQUIRER_NAME_MEMORY_LIMIT, INQUIRER_NAME_GPU_LIMIT
from savvihub.common.context import Context
from savvihub.common.formatter import TreeFormatter
from savvihub.common.utils import short_string, parse_time_to_ago, parse_str_time_to_datetime, \
    parse_timestamp_or_none, remove_file
from savvihub.savvihub_cli.errors import get_error_message
from savvihub.savvihub_cli.volume import volume_file_list, volume_file_copy

experiment_output_app = typer.Typer()
experiment_app = typer.Typer()
experiment_app.add_typer(experiment_output_app, name='output')


@experiment_app.callback()
def main():
    """
    Run the machine learning experiment
    """
    return


@experiment_app.command()
def list():
    """
    Display a list of experiments
    """

    context = Context(user_required=True, project_required=True)
    client = context.authorized_client

    experiments = client.experiment_list(context.project.workspace.name, context.project.name, raise_error=True)
    if not experiments:
        typer.echo(f'There is no experiment in {context.project.name} project.')
        return

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


@experiment_app.command()
def describe(
    experiment_number_or_name: str = typer.Argument(..., help="The unique experiment number or name"),
):
    """
    Describe the experiment in details
    """
    context = Context(user_required=True, project_required=True)
    client = context.authorized_client

    experiment = client.experiment_read(
        context.project.workspace.name, context.project.name, experiment_number_or_name,
        raise_error=True,
    )

    root = TreeFormatter()
    root.add_child(f'Number: {experiment.number}',
                   f'Name: {experiment.name}',
                   f'Created: {parse_str_time_to_datetime(experiment.created_dt)}',
                   f'Updated: {parse_str_time_to_datetime(experiment.updated_dt)}',
                   f'Git Commit Message: ({experiment.git_ref}) {experiment.message}')

    if experiment.git_diff_file:
        git_diff_file_desc = TreeFormatter('Git Diff File:')
        git_diff_file_desc.add_child(f'URL: {experiment.git_diff_file.download_url["url"]}')
        root.add_child(git_diff_file_desc)

    root.add_child(f'Status: {experiment.status}',
                   f'Tensorboard: {experiment.tensorboard or "N/A"}',
                   f'Tensorboard log_dir: {experiment.tensorboard_log_dir or "N/A"}')

    # Kernel Image Description
    kernel_image_desc = TreeFormatter('Kernel Image:')
    kernel_image_desc.add_child(f'Name: {experiment.kernel_image.name}',
                                f'URL: {experiment.kernel_image.image_url}',
                                f'Language: {experiment.kernel_image.language}')
    root.add_child(kernel_image_desc)

    # Resource Spec Description
    resource_spec_desc = TreeFormatter('Resource Spec:')
    resource_spec_desc.add_child(f'Name: {experiment.kernel_resource_spec.name}',
                                 f'CPU Type: {experiment.kernel_resource_spec.name}',
                                 f'CPU Limit: {experiment.kernel_resource_spec.cpu_limit}',
                                 f'CPU Guarantee: {experiment.kernel_resource_spec.cpu_guarantee}',
                                 f'Memory Limit: {experiment.kernel_resource_spec.memory_limit}',
                                 f'Memory Guarantee: {experiment.kernel_resource_spec.mem_guarantee}',
                                 f'GPU Type: {experiment.kernel_resource_spec.gpu_type}',
                                 f'GPU Limit: {experiment.kernel_resource_spec.gpu_limit}',
                                 f'GPU Guarantee: {experiment.kernel_resource_spec.gpu_guarantee}')
    root.add_child(resource_spec_desc)

    # Datasets Description
    datasets_desc = TreeFormatter('Datasets:')
    if not experiment.datasets:
        datasets_desc.add_child('Dataset Not Found')
    else:
        for dataset in experiment.datasets:
            dataset_desc = TreeFormatter(dataset['dataset_name'])
            dataset_desc.add_child(f'Mount Path: {dataset["mount_path"]}')
            datasets_desc.add_child(dataset_desc)
    root.add_child(datasets_desc)

    # Histories Description
    histories_desc = TreeFormatter('Histories:')
    if not experiment.histories:
        histories_desc.add_child('History Not Found')
    else:
        for history in experiment.histories:
            history_desc = TreeFormatter(history['status'])
            history_desc.add_child(f'Started: {parse_timestamp_or_none(history["started_timestamp"])}',
                                   f'Ended: {parse_timestamp_or_none(history["ended_timestamp"])}')
            histories_desc.add_child(history_desc)
    root.add_child(histories_desc)

    # Metrics Description
    metrics_desc = TreeFormatter('Metrics:')
    if not experiment.metrics:
        metrics_desc.add_child('Metrics Not Found')
    else:
        for history in experiment.metrics[-10:]:
            metrics_desc.add_child(history)

        full_metrics_info_desc = TreeFormatter('Full metrics info at:')
        full_metrics_info_desc.add_child(f'{WEB_HOST}/{context.project.workspace.name}/{context.project.name}/experiments/{experiment.number}/metrics')
        metrics_desc.add_child(full_metrics_info_desc)
    root.add_child(metrics_desc)

    # System Metrics Description
    system_metrics_desc = TreeFormatter('System Metrics:')
    full_system_metrics_info_desc = TreeFormatter('Full system metrics info at:')
    full_system_metrics_info_desc.add_child(f'{WEB_HOST}/{context.project.workspace.name}/{context.project.name}/experiments/{experiment.number}/system-metrics')
    system_metrics_desc.add_child(full_system_metrics_info_desc)
    root.add_child(system_metrics_desc)
    root.add_child(f'Start Command: {experiment.start_command}',
                   f'Source Code Link: {experiment.source_code_link}')

    typer.echo(root.format())


@experiment_app.command()
def logs(
    experiment_number_or_name: str = typer.Argument(..., help="The unique experiment number or name"),
    tail: int = typer.Option(200, "--tail"),
    detail: bool = typer.Option(False, "--detail", hidden=True),
    all: bool = typer.Option(False, "--all", hidden=True),
):
    """
    Display the last fifty lines of the experiment logs
    """
    context = Context(user_required=True, project_required=True)
    client = context.authorized_client

    params = {}
    if not all:
        params = {'limit': tail}
    if detail:
        params = {'withEventLog': 'true'}

    experiment_logs = client.experiment_log(
        context.project.workspace.name, context.project.name, experiment_number_or_name, params=params, raise_error=True)

    for log in experiment_logs:
        typer.echo(f'{parse_timestamp_or_none(log.timestamp)} {log.message}')

    typer.echo(
        client.get_full_info(context.project.workspace.name, context.project.name, experiment_number_or_name, 'logs')
    )


@experiment_app.command()
def run(
    command_arg: str = typer.Option(None, "--start-command", help="Start command"),
    image_arg: str = typer.Option(None, "--image", "-i", help="Kernel docker image URL"),
    cluster_name: str = typer.Option(None, "--cluster", "-c", help="Cluster name"),
    resource_name: str = typer.Option(None, "--resource", "-r", help="Resource name (for savvihub-managed cluster)"),
    processor_type: str = typer.Option(None, "--processor-type", help="cpu or gpu (for custom cluster)"),
    cpu_limit: float = typer.Option(0, "--cpu-limit", help="Number of vCPUs (for custom cluster)"),
    memory_limit: str = typer.Option(None, "--memory-limit", help="Memory capacity (ex: 4Gi, 500Mi)"),
    gpu_limit: int = typer.Option(0, "--gpu-limit", help="number of GPU cores (for custom cluster)"),
    gpu_type: str = typer.Option(None, "--gpu-type", help="GPU product name such as Tesla-K80 (for custom cluster)"),
    env_vars_arg: List[str] = typer.Option([], "-e", help="Environment variables"),
    dataset_mount_args: List[str] = typer.Option([], "--dataset", "-d", help="Dataset mounted path"),
    git_ref_arg: str = typer.Option(None, "--git-ref", help="Git commit SHA"),
    git_diff_arg: str = typer.Option(None, "--git-diff", help="Git diff file URL"),
    ignore_git_diff_arg: bool = typer.Option(False, "--ignore-git-diff", help="Ignore git diff flag"),
    project: str = typer.Option(None, "--project", hidden=True),
):
    """
    Run an experiment in SavviHub
    """
    # TODO: refactoring...
    git_ref = None
    if project:
        if not git_ref_arg:
            typer.echo("You must specify git commit SHA with `--git-ref` option")
            sys.exit(1)

        git_ref = git_ref_arg
        workspace_name, project_name = project.split("/")
        context = Context(user_required=True)

        # set project_config of context
        config_file_path = os.path.join(pathlib.Path().absolute(), ".savvihub", "config")
        if os.path.exists(config_file_path):
            remove_file(config_file_path)
        context.project_config = context.load_project_config(config_file_path)
        context.project_config.set_savvihub(url=API_HOST, workspace=workspace_name, project=project_name)
        context.project_config.save()

        # set project
        context.project = context.get_project()
    else:
        context = Context(user_required=True, project_required=True)

    client = context.authorized_client

    def find_from_args(options, selector, error_message=''):
        for option in options:
            if selector(option):
                return option

        if error_message:
            typer.echo(error_message)
            sys.exit(1)

    def find_from_inquirer(options, display, message):
        answers = inquirer.prompt([inquirer.List(
            "question",
            message=message,
            choices=[f'[{i+1}] {display(option)}' for i, option in enumerate(options)],
        )])
        answer = int(re.findall(r"[\d+]", answers.get("question"))[0]) - 1
        return options[answer]

    clusters = [c for c in client.cluster_list(context.project.workspace.name) if c.status == 'connected']
    if cluster_name:
        selected_cluster = find_from_args(
            clusters,
            lambda x: x.name == cluster_name.strip(),
            error_message=f'Cannot find cluster {cluster_name}.',
        )
    else:
        selected_cluster = find_from_inquirer(
            clusters,
            lambda x: f'{x.name}{" (SavviHub)" if x.is_savvihub_managed else f" ({x.kubernetes_master_endpoint})"}',
            "Please choose a cluster"
        )

    resource_spec_id = None
    resource_spec = None
    if selected_cluster.is_savvihub_managed:
        resources = client.kernel_resource_list(context.project.workspace.name)
        if resource_name:
            selected_resource = find_from_args(
                resources,
                lambda x: x.name == resource_name.strip(),
                error_message=f'Cannot find resource {resource_name}.',
            )
        else:
            selected_resource = find_from_inquirer(
                resources,
                lambda x: f'{x.name} ({x.description})',
                "Please choose a resource"
            )
        processor_type = selected_resource.processor_type
        resource_spec_id = selected_resource.id
    else:
        if processor_type not in ['cpu', 'gpu']:
            processor_type = find_from_inquirer(
                ['cpu', 'gpu'],
                lambda x: x,
                "Please choose a processor type",
            )
        if cpu_limit <= 0:
            cpu_limit = int(inquirer.prompt([inquirer.Text(
                INQUIRER_NAME_CPU_LIMIT,
                message="CPU limit (the number of vCPUs)",
                default=1,
            )]).get(INQUIRER_NAME_CPU_LIMIT))
            if cpu_limit <= 0:
                typer.echo('Must be greater than 0')
                sys.exit(1)
        if memory_limit is None:
            memory_limit_int = int(inquirer.prompt([inquirer.Text(
                INQUIRER_NAME_MEMORY_LIMIT,
                message="Memory limit in GiB",
                default=4,
            )]).get(INQUIRER_NAME_MEMORY_LIMIT))
            if memory_limit_int <= 0:
                typer.echo('Must be greater than 0')
                sys.exit(1)
            memory_limit = f'{memory_limit_int}Gi'
        if processor_type == 'gpu' and gpu_type is None:
            gpu_type = inquirer.prompt([inquirer.Text(  # TODO: use find_from_inquirer
                INQUIRER_NAME_GPU_LIMIT,
                message="GPU type",
                default="Tesla-K80",
            )]).get(INQUIRER_NAME_GPU_LIMIT)
        if gpu_type is not None and gpu_type != 'Empty' and gpu_limit <= 0:
            gpu_limit = int(inquirer.prompt([inquirer.Text(
                INQUIRER_NAME_GPU_LIMIT,
                message="GPU limit (the number of GPUs)",
                default=1,
            )]).get(INQUIRER_NAME_GPU_LIMIT))
            if gpu_limit <= 0:
                typer.echo('Must be greater than 0')
                sys.exit(1)

        resource_spec = {
            'processor_type': processor_type,
            'cpu_type': 'Any',
            'cpu_limit': cpu_limit,
            'memory_limit': memory_limit,
            'gpu_type': gpu_type or 'Empty',
            'gpu_limit': 0 if gpu_type is None else gpu_limit,
        }

    images = client.kernel_image_list(context.project.workspace.name, processor_type)
    if not image_arg:
        selected_image_url = find_from_inquirer(
            images,
            lambda x: f'{x.image_url} ({x.name})',
            "Please choose a kernel image"
        ).image_url
    else:
        selected_image_url = image_arg.strip()

    if command_arg:
        start_command = command_arg
    else:
        start_command = inquirer.prompt([inquirer.Text(
            INQUIRER_NAME_COMMAND,
            message="Start command",
            default="python main.py",
        )]).get(INQUIRER_NAME_COMMAND)

    dataset_mounts_parsed = []
    for dataset_mount in dataset_mount_args:
        # parse dataset and volume
        if ':' not in dataset_mount:
            typer.echo(f'Invalid dataset name: {dataset_mount}. '
                       f'You should specify dataset and mount location.\n'
                       f'ex) savvihub/mnist:3d1e0f:/input/dataset1')
            sys.exit(1)

        # parse snapshot ref
        splitted = dataset_mount.split(':')
        if len(splitted) == 2:
            dataset_name_with_workspace, mount_path = splitted
            snapshot_ref = 'latest'
        elif len(splitted) == 3:
            dataset_name_with_workspace, snapshot_ref, mount_path = splitted
        else:
            typer.echo(f'Invalid dataset name: {dataset_mount}\n'
                       f'You should specify dataset and mount location.\n'
                       f'ex) savvihub/mnist:3d1e0f:/input/dataset1')
            sys.exit(1)

        if '/' not in dataset_name_with_workspace:
            typer.echo(f'Invalid dataset name: {dataset_mount}\n'
                       f'You should specify dataset with workspace.\n'
                       f'ex) savvihub/mnist:3d1e0f:/input/dataset1')
            sys.exit(1)

        workspace_name, dataset_name = dataset_name_with_workspace.split('/')

        # read dataset or snapshot
        dataset_obj = client.dataset_read(workspace_name, dataset_name)
        if not dataset_obj:
            typer.echo(f'Invalid dataset: {dataset_name_with_workspace}\n'
                       f'Please check your dataset exist in savvihub.\n')
            sys.exit(1)

        if snapshot_ref != 'latest':
            snapshot_obj = client.snapshot_read(dataset_obj.volume_id, snapshot_ref)
            if not snapshot_obj:
                typer.echo(f'Invalid dataset snapshots: {dataset_mount}\n'
                           f'Please check your dataset and snapshot exist in savvihub.')
                sys.exit(1)

        if not mount_path.startswith('/input'):
            typer.echo(f'Invalid dataset mount path: {mount_path}\n'
                       f'Dataset mount path should start with /input.')
            sys.exit(1)

        dataset_mounts_parsed.append(dict(
            dataset_id=dataset_obj.id,
            snapshot_ref=snapshot_ref,
            mount_path=mount_path,
        ))

    diff_file = None
    if git_ref:
        pass
    elif git_ref_arg:
        if not context.git_repo.check_revision_in_remote(git_ref_arg.strip()):
            typer.echo(f'Git commit {git_ref_arg.strip()} does not exist in a remote repository.')
            sys.exit(1)

        git_ref = git_ref_arg.strip()

        if git_diff_arg and (git_diff_arg.startswith('https://') or git_diff_arg.startswith('http://')):
            diff_file = tempfile.NamedTemporaryFile(suffix='.patch')
            d = DownloadableFileObject(git_diff_arg, os.path.dirname(diff_file.name), os.path.basename(diff_file.name))
            d.download(session=context.authorized_client.session)
            diff_file.seek(0)

    else:
        git_ref, branch, is_head = context.git_repo.get_remote_revision_or_branch()
        commit = context.git_repo.get_commit_message(git_ref)
        typer.echo(f'Run experiment with revision {git_ref[:6]} ({branch})')
        typer.echo(f'Commit: {commit}')
        if not is_head:
            typer.echo('Your current revision does not exist in remote repository. SavviHub will use latest remote '
                       'branch revision hash and diff.')
        typer.echo('')

        has_diff, diff_status = context.git_repo.get_current_diff_status(git_ref)
        if has_diff and not ignore_git_diff_arg:
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

            # TODO: reduce choices if uncommitted or untracked not exist

            answers = inquirer.prompt([inquirer.List(
                'experiment',
                message='Run experiment with diff?',
                choices=[
                    '[1] Run experiment with uncommitted and untracked changes.',
                    '[2] Run experiment with uncommitted changes.',
                    '[3] Run experiment without any changes.',
                    '[4] Abort.',
                ],
            )])
            answer = int(re.findall(r'[\d+]', answers.get('experiment'))[0])

            diff_file = None
            if answer == 1:
                diff_file = context.git_repo.get_current_diff_file(git_ref, with_untracked=True)
            elif answer == 2:
                diff_file = context.git_repo.get_current_diff_file(git_ref, with_untracked=False)
            elif answer == 3:
                pass
            else:
                typer.echo('Aborted.')
                return

    diff_file_path = None
    if diff_file:
        typer.echo('Generating diff patch file...')
        uploaded = Uploader.upload(
            context,
            local_path=diff_file.name,
            volume_id=context.project.volume_id,
            remote_path=os.path.basename(diff_file.name),
            progressable=typer.progressbar,
        )
        diff_file_path = uploaded.path
        diff_file.close()

    env_vars = []
    for env_var in env_vars_arg:
        try:
            env_key, env_value = env_var.split("=")
            env_vars.append({
                'key': env_key,
                'value': env_value,
            })
        except ValueError:
            typer.echo(f'Cannot parse environment variable: {env_var}')
            sys.exit(1)

    res = client.experiment_create(
        workspace=context.project.workspace.name,
        project=context.project.name,
        cluster_name=selected_cluster.name,
        image_url=selected_image_url,
        resource_spec=resource_spec,
        resource_spec_id=resource_spec_id,
        git_ref=git_ref,
        git_diff_file_path=diff_file_path,
        start_command=start_command,
        datasets=dataset_mounts_parsed,
        env_vars=env_vars,
    )

    res_data = res.json()
    if res.status_code == 400:
        typer.echo(get_error_message(res_data))
        sys.exit(1)

    res.raise_for_status()

    experiment_number = res_data.get('number')
    typer.echo(f'Experiment {experiment_number} is running. Check the experiment status at below link')
    typer.echo(f'{WEB_HOST}/{context.project.workspace.name}/{context.project.name}/experiments/{experiment_number}')


@experiment_output_app.callback()
def output_main():
    """
    Manage experiment output files
    """


@experiment_output_app.command()
def ls(
    experiment_number_or_name: str = typer.Argument(..., help="The unique experiment number or name"),
    path: str = typer.Argument(None, help='Output file path'),
    recursive: bool = typer.Option(False, '-r', '--recursive', help='recursive flag'),
    directory: bool = typer.Option(False, '-d', '--directory',
                                   help='list the directory itself, not its contents'),
):
    """
    List the output files of the experiment
    """
    context = Context(user_required=True, project_required=True)
    client = context.authorized_client

    experiment = client.experiment_read(
        context.project.workspace.name, context.project.name, experiment_number_or_name, raise_error=True,
    )
    volume_file_list(experiment.output_volume.volume_id, 'latest', path or '', recursive, directory)


@experiment_output_app.command()
def download(
    experiment_number_or_name: str = typer.Argument(..., help="The unique experiment number or name"),
    dest_path: str = typer.Argument(None, help='The files will be downloaded to ./output if omitted.'),
):
    """
    Download experiment output files
    """
    context = Context(user_required=True, project_required=True)
    client = context.authorized_client

    experiment = client.experiment_read(
        context.project.workspace.name, context.project.name, experiment_number_or_name, raise_error=True,
    )
    volume_file_copy(experiment.output_volume.volume_id, 'latest', '',
                     None, None, dest_path or './output',
                     recursive=True, watch=False)


if __name__ == "__main__":
    experiment_app()
