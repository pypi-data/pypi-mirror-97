import inspect
from functools import wraps

from openapi_client import *
from savvihub.api.exceptions import convert_to_savvihub_exception, NotFoundAPIException
from savvihub.common.constants import API_HOST


def raise_savvihub_exception(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ApiException as e:
            raise convert_to_savvihub_exception(e)

    return wrapped


def decorate_all_methods(method_decorator):
    def class_decorator(cls):
        for attr in inspect.classify_class_attrs(cls):
            if attr.kind == 'method' and issubclass(attr.defining_class, cls.__bases__[0]):
                setattr(cls, attr.name, method_decorator(attr[3]))
        return cls
    return class_decorator


@decorate_all_methods(raise_savvihub_exception)
class OpenAPIClientWithSavviHubException(APIV1Api):
    pass


class SavviHubClient:
    def __init__(self, *, auth_header=None, api_host=API_HOST):
        self.auth_header = {}
        kwargs = {
            'configuration': Configuration(host=api_host),
        }
        if auth_header:
            self.auth_header = auth_header
            for header_name, header_value in auth_header.items():
                kwargs['header_name'], kwargs['header_value'] = header_name, header_value

        self.client = OpenAPIClientWithSavviHubException(ApiClient(**kwargs))

    def signup_for_test_only(self, email, username, name, password, invitation_token) -> ResponseUserWithTokenResponse:
        return self.client.sign_up_api(
            sign_up_api_payload=SignUpAPIPayload(
                email=email,
                username=username,
                name=name,
                password=password,
                invitation_token=invitation_token,
            ),
        )

    def signin_confirm_for_test_only(self, cli_token):
        return self.client.sign_in_cli_confirm_api(
            sign_in_cli_confirm_api_payload=SignInCliConfirmAPIPayload(
                cli_token=cli_token,
            ),
        )

    def get_my_info(self) -> ResponseMyUser:
        return self.client.get_my_user_info_api()

    def verify_access_token(self):
        self.client.access_token_verify_api()

    def experiment_id_read(self, experiment_id) -> ResponseExperiment:
        return self.client.experiment_read_by_idapi(experiment_id=experiment_id)

    def project_read(self, workspace_name, project_name) -> ResponseProjectInfo:
        return self.client.project_read_api(workspace_name=workspace_name, project_name=project_name)

    def signin_cli_token(self) -> AccountSignInCliTokenResponse:
        return self.client.sign_in_cli_token_api()

    def check_signin(self, cli_token) -> AccountSignInCliCheckResponse:
        return self.client.sign_in_cli_check_api(cli_token=cli_token)

    def volume_read(self, volume_id) -> ResponseVolume:
        return self.client.volume_read_api(volume_id=volume_id)

    def volume_file_list(
        self, volume_id, snapshot='latest', path='', recursive=False, need_download_url=False,
    ) -> VolumeVolumeFileListResponse:
        return self.client.volume_file_list_api(
            volume_id=volume_id,
            path=path,
            recursive=recursive,
            snapshot=snapshot,
            need_download_url=need_download_url,
        )

    def volume_file_read(self, volume_id, path, snapshot) -> ResponseFileMetadata:
        return self.client.volume_file_read_api(volume_id=volume_id, path=path, snapshot=snapshot)

    def volume_file_copy(self, volume_id, source_path, source_snapshot, dest_path, recursive=False) -> VolumeVolumeFileCopyResponse:
        return self.client.volume_file_copy_api(
            volume_id=volume_id,
            volume_file_copy_api_payload=VolumeFileCopyAPIPayload(
                source_path=source_path,
                source_snapshot=source_snapshot,
                dest_path=dest_path,
                recursive=recursive,
            ),
        )

    def volume_file_delete(self, volume_id, path, recursive=False) -> VolumeVolumeFileDeleteResponse:
        return self.client.volume_file_delete_api(volume_id=volume_id, path=path, recursive=recursive)

    def volume_file_create(self, volume_id, path, is_dir) -> ResponseFileMetadata:
        return self.client.volume_file_create_api(
            volume_id=volume_id,
            volume_file_create_api_payload=VolumeFileCreateAPIPayload(
                path=path,
                is_dir=is_dir,
            ),
        )

    def volume_file_uploaded(self, volume_id, path) -> ResponseFileMetadata:
        return self.client.volume_file_uploaded_api(
            volume_id=volume_id,
            path=path,
        )

    def snapshot_read(self, volume_id, snapshot_name) -> ResponseSnapshot:
        return self.client.snapshot_read_api(volume_id=volume_id, snapshot_name=snapshot_name)

    def experiment_read(self, workspace, project, experiment_number_or_name) -> ResponseExperimentInfo:
        return self.client.experiment_read_api(
            workspace_name=workspace,
            project_name=project,
            experiment=experiment_number_or_name,
        )

    def experiment_list(self, workspace, project) -> ExperimentExperimentListResponse:
        return self.client.experiment_list_api(
            workspace_name=workspace,
            project_name=project,
            order_field='number',
            order_direction='desc',
        )

    def experiment_log(self, workspace, project, experiment_number_or_name, **kwargs) -> ExperimentExperimentLogResponse:
        return self.client.experiment_log_api(
            workspace_name=workspace,
            project_name=project,
            experiment=experiment_number_or_name,
            **kwargs,
        )

    def experiment_create(
        self, workspace, project, cluster_name, image_url, resource_spec_id, resource_spec,
        start_command, env_vars, volume_mounts,
    ) -> ResponseExperiment:
        return self.client.experiment_create_api(
            workspace_name=workspace,
            project_name=project,
            experiment_create_api_payload=ExperimentCreateAPIPayload(
                cluster_name=cluster_name,
                image_url=image_url,
                resource_spec_id=resource_spec_id,
                resource_spec=resource_spec,
                env_vars=env_vars,
                start_command=start_command,
                volumes=volume_mounts,
            ),
        )

    def experiment_metrics_update(self, experiment_id, metrics):
        self.client.cli_experiment_metrics_update_api(
            experiment_id=experiment_id,
            cli_experiment_metrics_update_api_payload=CliExperimentMetricsUpdateAPIPayload(
                metrics=metrics,
            ),
        )

    def kernel_image_list(self, workspace) -> KernelKernelImageListResponse:
        return self.client.kernel_image_list_api(workspace_name=workspace)

    def kernel_resource_list(self, workspace) -> KernelKernelResourceSpecListResponse:
        return self.client.kernel_resource_spec_list_api(workspace_name=workspace)

    def workspace_list(self) -> WorkspaceWorkspaceListResponse:
        return self.client.workspace_list_api()

    def workspace_read(self, workspace) -> ResponseWorkspace:
        return self.client.workspace_read_api(workspace_name=workspace)

    def project_list(self, workspace_name) -> ResponseProjectListResponse:
        return self.client.project_list_api(workspace_name=workspace_name)

    def project_github_create(self, workspace, project, github_owner, github_repo) -> ResponseProject:
        return self.client.project_git_hub_create_api(
            workspace_name=workspace,
            project_git_hub_create_api_payload=ProjectGitHubCreateAPIPayload(
                name=project,
                github_owner=github_owner,
                github_repo=github_repo,
            ),
        )

    def public_dataset_list(self) -> ResponseDatasetInfoList:
        return self.client.datasets_public_list_api()

    def dataset_list(self, workspace) -> ResponseDatasetInfoList:
        return self.client.dataset_list_api(workspace_name=workspace)

    def dataset_read(self, workspace, dataset) -> ResponseDatasetInfo:
        try:
            return self.client.dataset_read_api(workspace_name=workspace, dataset_name=dataset)
        except NotFoundAPIException:
            raise NotFoundAPIException(f'Dataset `{dataset}` is not in the workspace `{workspace}`.')

    def dataset_create(self, workspace, name, is_public, description) -> ResponseDatasetInfo:
        return self.client.savvi_hub_dataset_create_api(
            workspace_name=workspace,
            savvi_hub_dataset_create_api_payload=SavviHubDatasetCreateAPIPayload(
                name=name,
                is_public=is_public,
                description=description,
            ),
        )

    def dataset_gs_create(self, workspace, name, is_public, description, gs_path) -> ResponseDatasetInfo:
        return self.client.g_s_dataset_create_api(
            workspace_name=workspace,
            gs_dataset_create_api_payload=GSDatasetCreateAPIPayload(
                name=name,
                is_public=is_public,
                description=description,
                gs_path=gs_path,
            ),
        )

    def dataset_s3_create(self, workspace, name, is_public, description, s3_path, aws_role_arn) -> ResponseDatasetInfo:
        return self.client.s3_dataset_create_api(
            workspace_name=workspace,
            s3_dataset_create_api_payload=S3DatasetCreateAPIPayload(
                name=name,
                is_public=is_public,
                description=description,
                s3_path=s3_path,
                aws_role_arn=aws_role_arn,
            ),
        )

    def cluster_add(self, workspace_name, cluster_name, agent_access_token,
                    master_endpoint, namespace, service_account_token, ssl_ca_cert_base64_encoded) -> ResponseKernelCluster:
        return self.client.custom_cluster_add_api(
            workspace_name=workspace_name,
            custom_cluster_add_api_payload=CustomClusterAddAPIPayload(
                name=cluster_name,
                agent_access_token=agent_access_token,
                kubernetes_master_endpoint=master_endpoint,
                kubernetes_namespace=namespace,
                kubernetes_service_account_token=service_account_token,
                kubernetes_ssl_ca_cert=ssl_ca_cert_base64_encoded,
            ),
        )

    def cluster_list(self, workspace_name) -> ClusterAllClusterListResponse:
        return self.client.all_cluster_list_api(workspace_name=workspace_name)

    def cluster_delete(self, workspace_name, cluster_name):
        self.client.custom_cluster_delete_api(workspace_name=workspace_name, cluster_name=cluster_name)

    def cluster_rename(self, workspace_name, cluster_name, new_name) -> ResponseKernelCluster:
        return self.client.custom_cluster_update_api(
            workspace_name=workspace_name,
            cluster_name=cluster_name,
            custom_cluster_update_api_payload=CustomClusterUpdateAPIPayload(
                name=new_name,
            ),
        )
