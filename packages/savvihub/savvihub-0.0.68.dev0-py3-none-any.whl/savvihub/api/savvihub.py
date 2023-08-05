import sys
import typing

import requests
import typer

from savvihub.api.errors import parse_error_code, SavviHubError, SavviHubNotADirectoryError, \
    SavviHubNoSuchFileOrDirectoryError
from savvihub.api.types import PaginatedMixin, SavviHubListResponse, SavviHubFileObject, SavviHubDataset, \
    SavviHubKernelResource, SavviHubKernelImage, SavviHubExperiment, SavviHubProject, SavviHubWorkspace, SavviHubUser, \
    SavviHubExperimentLog, SavviHubSnapshot, SavviHubVolume, SavviHubExperimentMetric, SavviHubKernelCluster
from savvihub.common.constants import API_HOST, WEB_HOST, DEBUG


class SavviHubClient:
    def __init__(self, *, session=requests.Session(), token=None, url=API_HOST, content_type='application/json'):
        self.session = session
        self.url = url
        self.token = token
        
        session.headers = {'content-type': content_type}
        if token:
            session.headers['authorization'] = 'Token %s' % token

    def get(self, url, params=None, raise_error=False, **kwargs):
        r = self.session.get(f'{self.url}{url}', params=params, **kwargs)
        if DEBUG:
            print({
                'method': 'GET',
                'url': url,
                'params': params,
                'status_code': r.status_code if isinstance(r, requests.Response) else None,
                'response': r.text if isinstance(r, requests.Response) else None,
            })
        if raise_error and r.status_code / 100 >= 4:
            raise parse_error_code(r)
        return r

    def get_all(self, url, params=None, raise_error=False, **kwargs):
        raw_r = self.get(url, params=params, raise_error=raise_error, **kwargs)
        r = PaginatedMixin(raw_r.json())
        results = []

        fetched_items = 0
        while True:
            fetched_items += len(r.results)
            results.extend(r.results)
            if fetched_items >= r.total:
                break
            raw_r = self.get(url, params={**params, 'after': r.endCursor}, raise_error=raise_error, **kwargs)
            r = PaginatedMixin(raw_r.json())
        return results

    def get_all_without_pagination(self, url, params=None, raise_error=False, **kwargs):
        raw_r = self.get(url, params=params, raise_error=raise_error, **kwargs)
        r = SavviHubListResponse(raw_r.json())
        return r.results

    def post(self, url, data, raise_error=False, **kwargs):
        r = self.session.post(f'{self.url}{url}', json=data, **kwargs)
        if DEBUG:
            print({
                'method': 'POST',
                'url': url,
                'request': data,
                'status_code': r.status_code if isinstance(r, requests.Response) else None,
                'response': r.text if isinstance(r, requests.Response) else None,
            })
        if raise_error and r.status_code / 100 >= 4:
            raise parse_error_code(r)
        return r

    def delete(self, url, raise_error=False, **kwargs):
        r = self.session.delete(f'{self.url}{url}', **kwargs)
        if DEBUG:
            print({
                'method': 'DELETE',
                'url': url,
                'status_code': r.status_code if isinstance(r, requests.Response) else None,
                'response': r.text if isinstance(r, requests.Response) else None,
            })
        if raise_error and r.status_code / 100 >= 4:
            raise parse_error_code(r)
        return r

    def patch(self, url, data, raise_error=False, **kwargs):
        r = self.session.patch(f'{self.url}{url}', json=data, **kwargs)
        if DEBUG:
            print({
                'method': 'PATCH',
                'url': url,
                'request': data,
                'status_code': r.status_code if isinstance(r, requests.Response) else None,
                'response': r.text if isinstance(r, requests.Response) else None,
            })
        if raise_error and r.status_code / 100 >= 4:
            raise parse_error_code(r)
        return r

    def get_my_info(self):
        r = self.get(f'/api/v1/accounts/me')
        if r.status_code != 200:
            return None
        return SavviHubUser(r.json())

    def verify_access_token(self):
        r = self.post(f'/api/v1/accounts/access_tokens/verify', {})
        r.raise_for_status()

    def check_signin_token(self):
        r = self.post(f'/api/v1/accounts/signin/cli/token', {})
        r.raise_for_status()
        return r.json()['cli_token']

    def check_signin(self, cli_token):
        r = self.get(f'/api/v1/accounts/signin/cli/check', {
            'cli_token': cli_token,
        })
        r.raise_for_status()
        return r.json()['signin_success'], r.json()['access_token']

    def volume_read(self, volume_id, **kwargs):
        r = self.get(f'/api/v1/volumes/{volume_id}', **kwargs)
        return SavviHubVolume(r.json())

    def volume_file_list(
        self, volume_id, snapshot='latest', path='', recursive=False, need_download_url=False, **kwargs,
    ) -> typing.Optional[typing.List[SavviHubFileObject]]:
        try:
            r = self.get(f'/api/v1/volumes/{volume_id}/files', params={
                'path': path,
                'recursive': recursive,
                'snapshot': snapshot,
                'need_download_url': need_download_url,
            }, raise_error=True, **kwargs)
        except SavviHubError as e:
            if e == SavviHubNotADirectoryError:
                typer.echo(f'Not a directory: {path}')
            elif e == SavviHubNoSuchFileOrDirectoryError:
                typer.echo(f'No such file or directory: {path}')
            sys.exit(1)

        return [SavviHubFileObject(x) for x in r.json().get('results')]

    def volume_file_read(self, volume_id, path, snapshot, **kwargs):
        try:
            r = self.get(f'/api/v1/volumes/{volume_id}/files/read', params={
                'path': path, 'snapshot': snapshot,
            }, raise_error=True, **kwargs)
        except SavviHubError as e:
            if e == SavviHubNotADirectoryError:
                typer.echo(f'Not a directory: {path}')
            elif e == SavviHubNoSuchFileOrDirectoryError:
                return None
            print(e)
            sys.exit(1)

        return SavviHubFileObject(r.json())

    def volume_file_copy(self, volume_id, source_path, source_snapshot, dest_path, recursive=False, **kwargs):
        r = self.post(f'/api/v1/volumes/{volume_id}/files/copy', {
            'source_path': source_path,
            'source_snapshot': source_snapshot,
            'dest_path': dest_path,
            'recursive': recursive,
        }, **kwargs)
        r.raise_for_status()
        return [SavviHubFileObject(x) for x in r.json().get('copied_files')]

    def volume_file_delete(self, volume_id, path, recursive=False):
        r = self.delete(f'/api/v1/volumes/{volume_id}/files/delete', params={'path': path, 'recursive': recursive})
        if r.status_code != 200:
            return None
        return [SavviHubFileObject(x) for x in r.json().get('DeletedFiles')]

    def volume_file_create(self, volume_id, path, is_dir, **kwargs):
        return self.post(f'/api/v1/volumes/{volume_id}/files', {
            'path': path,
            'is_dir': is_dir
        }, **kwargs)

    def volume_file_uploaded(self, volume_id, path, **kwargs):
        return self.post(f'/api/v1/volumes/{volume_id}/files/uploaded?path={path}', {
        }, **kwargs)

    def snapshot_read(self, volume_id, ref, **kwargs):
        r = self.get(f'/api/v1/volumes/{volume_id}/snapshots/{ref}', **kwargs)
        if r.status_code != 200:
            return None
        return SavviHubSnapshot(r.json())

    def experiment_id_read(self, experiment_id, **kwargs):
        r = self.get(f'/api/v1/experiments/{experiment_id}', **kwargs)
        if r.status_code != 200:
            return None
        return SavviHubExperiment(r.json())

    def experiment_read(self, workspace, project, experiment_number_or_name, **kwargs) -> SavviHubExperiment:
        return SavviHubExperiment(
            self.get(f'/api/v1/workspaces/{workspace}/projects/{project}/experiments/{experiment_number_or_name}',
                     **kwargs).json())

    def experiment_list(self, workspace, project, **kwargs):
        return [SavviHubExperiment(x)
                for x in self.get_all_without_pagination(
                f'/api/v1/workspaces/{workspace}/projects/{project}/experiments?orderby.field=number&orderby.direction=desc', **kwargs)]

    def experiment_log(self, workspace, project, experiment_number_or_name, **kwargs):
        return [SavviHubExperimentLog(x)
                for x in self.get(
                f'/api/v1/workspaces/{workspace}/projects/{project}/experiments/{experiment_number_or_name}/log',
                **kwargs).json().get('logs')]

    def experiment_create(self, workspace, project, cluster_name, image_url, resource_spec_id, resource_spec,
                          git_ref, git_diff_file_path, start_command, datasets, env_vars, **kwargs):
        return self.post(f'/api/v1/workspaces/{workspace}/projects/{project}/experiments', {
            'cluster_name': cluster_name,
            'image_url': image_url,
            'resource_spec_id': resource_spec_id,
            'resource_spec': resource_spec,
            'git_ref': git_ref,
            'datasets': datasets,
            'git_diff_file_path': git_diff_file_path,
            'env_vars': env_vars,
            'start_command': start_command,
        }, **kwargs)

    def experiment_metrics_update(self, experiment_id, metrics: typing.Dict[str, typing.List[SavviHubExperimentMetric]], **kwargs):
        return self.post(f'/api/v1/experiments/{experiment_id}/metrics', {
            'metrics': metrics,
        }, **kwargs)

    def experiment_system_metrics_update(self, experiment_id, metrics: typing.Dict[str, typing.List[SavviHubExperimentMetric]], **kwargs):
        return self.post(f'/api/v1/experiments/{experiment_id}/system_metrics', {
            'system_metrics': metrics,
        }, **kwargs)

    def kernel_image_list(self, workspace, type):
        results = self.get_all_without_pagination(f'/api/v1/workspaces/{workspace}/kernels/images')
        return [SavviHubKernelImage(x) for x in results if x.get("processor_type") == type]

    def kernel_resource_list(self, workspace):
        results = self.get_all_without_pagination(f'/api/v1/workspaces/{workspace}/kernels/resource_specs')
        return [SavviHubKernelResource(x) for x in results]

    def workspace_list(self, **kwargs):
        r = self.get(f'/api/v1/workspaces', **kwargs)
        return [SavviHubWorkspace(x) for x in r.json().get('workspaces')]

    def workspace_read(self, workspace):
        r = self.get(f'/api/v1/workspaces/{workspace}')
        if r.status_code == 404:
            return None
        elif r.status_code != 200:
            r.raise_for_status()
        return SavviHubWorkspace(r.json())

    def project_read(self, workspace, project):
        r = self.get(f'/api/v1/workspaces/{workspace}/projects/{project}')
        if r.status_code == 404:
            return None
        elif r.status_code != 200:
            r.raise_for_status()
        return SavviHubProject(r.json())

    def project_github_create(self, workspace, project, github_owner, github_repo, **kwargs):
        return SavviHubProject(self.post(f'/api/v1/workspaces/{workspace}/projects_github', {
            'name': project,
            'github_owner': github_owner,
            'github_repo': github_repo,
        }, **kwargs).json())

    def public_dataset_list(self, **kwargs):
        results = self.get_all(f'/api/v1/datasets/public', **kwargs)
        return [SavviHubDataset(x) for x in results]

    def dataset_list(self, workspace, **kwargs):
        results = self.get_all(f'/api/v1/workspaces/{workspace}/datasets', **kwargs)
        if not results:
            return []
        return [SavviHubDataset(x) for x in results]

    def dataset_read(self, workspace, dataset, **kwargs):
        r = self.get(f'/api/v1/workspaces/{workspace}/datasets/{dataset}', **kwargs)
        if r.status_code != 200:
            return None
        return SavviHubDataset(r.json())

    def dataset_snapshot_file_list(self, workspace, dataset, ref, **kwargs):
        r = self.get(f'/api/v1/workspaces/{workspace}/datasets/{dataset}/snapshots/{ref}/files', **kwargs)
        return [SavviHubFileObject(x) for x in r.json().get('results')]

    def dataset_create(self, workspace, name, is_public, description, **kwargs):
        r = self.post(f'/api/v1/workspaces/{workspace}/datasets', {
            'name': name,
            'is_public': is_public,
            'description': description,
        }, **kwargs)
        if r.status_code == 409:
            typer.echo(f"Duplicate entity \"{workspace}/{name}\". Try another dataset name!")
            return
        elif r.status_code != 200:
            typer.echo('Unexpected error.')
            return
        return SavviHubDataset(r.json())

    def dataset_gs_create(self, workspace, name, is_public, description, gs_path, **kwargs):
        r = self.post(f'/api/v1/workspaces/{workspace}/datasets_gs', {
            'name': name,
            'is_public': is_public,
            'description': description,
            'gs_path': gs_path
        }, **kwargs)
        if r.status_code == 409:
            typer.echo(f"Duplicate entity \"{workspace}/{name}\". Try another dataset name!")
            return
        return SavviHubDataset(r.json())

    def dataset_s3_create(self, workspace, name, is_public, description, s3_path, aws_role_arn, **kwargs):
        r = self.post(f'/api/v1/workspaces/{workspace}/datasets_s3', {
            'name': name,
            'is_public': is_public,
            'description': description,
            's3_path': s3_path,
            'aws_role_arn': aws_role_arn,
        }, **kwargs)
        if r.status_code == 409:
            typer.echo(f"Duplicate entity \"{workspace}/{name}\". Try another dataset name!")
            return
        return SavviHubDataset(r.json())

    def cluster_create(self, workspace, cluster_name):
        try:
            r = self.post(f'/api/v1/workspaces/{workspace}/custom_clusters', {
                'name': cluster_name,
            }, raise_error=True)
        except SavviHubError as e:
            typer.echo(e.message())
            sys.exit(1)

        return SavviHubKernelCluster(r.json())

    def cluster_add(self, workspace_name, cluster_name, agent_access_token,
                    master_endpoint, namespace, service_account_token, ssl_ca_cert_base64_encoded):
        try:
            r = self.post(f'/api/v1/workspaces/{workspace_name}/custom_clusters', {
                'name': cluster_name,
                'agent_access_token': agent_access_token,
                'kubernetes_master_endpoint': master_endpoint,
                'kubernetes_namespace': namespace,
                'kubernetes_service_account_token': service_account_token,
                'kubernetes_ssl_ca_cert': ssl_ca_cert_base64_encoded,
            }, raise_error=True)
        except SavviHubError as e:
            typer.echo(e.message())
            sys.exit(1)

        return SavviHubKernelCluster(r.json())

    def cluster_list(self, workspace_name):
        try:
            r = self.get(f'/api/v1/workspaces/{workspace_name}/clusters', raise_error=True)
        except SavviHubError as e:
            typer.echo(e.message())
            sys.exit(1)

        return [SavviHubKernelCluster(x) for x in r.json()['clusters']]

    def cluster_delete(self, workspace_name, cluster_name):
        try:
            self.delete(f'/api/v1/workspaces/{workspace_name}/custom_clusters/{cluster_name}', raise_error=True)
        except SavviHubError as e:
            typer.echo(e.message())
            sys.exit(1)

    def cluster_rename(self, workspace_name, cluster_name, new_name):
        try:
            self.patch(f'/api/v1/workspaces/{workspace_name}/custom_clusters/{cluster_name}', {
                'name': new_name,
            }, raise_error=True)
        except SavviHubError as e:
            typer.echo(e.message())
            sys.exit(1)

    @staticmethod
    def get_full_info(workspace, project, experiment, form):
        return \
            f'\n\tFull {form} info at:\n' \
            f'\t\t{WEB_HOST}/{workspace}/{project}/experiments/{experiment}/{form}\n'

    @staticmethod
    def get_full_info_project(workspace, project):
        return \
            f'\n\tFull project info at:\n' \
            f'\t\t{WEB_HOST}/{workspace}/{project}\n'

    @staticmethod
    def get_full_info_dataset(workspace, dataset):
        return \
            f'\n\tFull dataset info at:\n' \
            f'\t\t{WEB_HOST}/{workspace}/datasets/{dataset}\n'

    @staticmethod
    def get_full_info_experiment(workspace, project, experiment):
        return \
            f'\n\tFull experiment info at:\n' \
            f'\t\t{WEB_HOST}/{workspace}/{project}/experiments/{experiment}\n'

    @staticmethod
    def get_download_url(volume_id, path):
        return f'{WEB_HOST}/file-download/{volume_id}/{path}'
