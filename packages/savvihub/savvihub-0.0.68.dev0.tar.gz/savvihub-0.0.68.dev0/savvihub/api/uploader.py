import os
from typing import List

from requests_futures.sessions import FuturesSession

from savvihub.api.file_object import UploadableFileObject, DownloadableFileObject
from savvihub.api.savvihub import SavviHubClient
from savvihub.api.types import SavviHubFileObject
from savvihub.common.utils import wait_all_futures, calculate_crc32c


def default_hooks():
    def fn(resp, **kwargs):
        resp.raise_for_status()
    return {
        'response': fn,
    }


class Downloader:
    @classmethod
    def download(cls, local_path, file: SavviHubFileObject, progressable=None):
        dirname = os.path.dirname(local_path)
        basename = os.path.basename(local_path)
        d = DownloadableFileObject(file.download_url.get('url'), dirname, basename)
        d.download(progressable=progressable)

    @classmethod
    def bulk_download(cls, context, local_base_path, remote_files: List[SavviHubFileObject], progressable=None):
        if len(remote_files) <= 0:
            return
        session = FuturesSession(max_workers=context.parallel)
        futures = []
        for remote_file in remote_files:
            if remote_file.path.endswith('/'):
                continue

            d = DownloadableFileObject(remote_file.download_url.get('url'), local_base_path, remote_file.path)
            futures.append(d.download(session, progressable=progressable))

        wait_all_futures(futures)


class Uploader:
    @classmethod
    def get_files_to_upload(cls, local_base_path, hashmap=None):
        local_base_path = local_base_path.rstrip('/')
        results = []
        for root, dirs, files in os.walk(local_base_path):
            for name in files:
                name = os.path.join(os.path.abspath(root), name)
                name = name[len(local_base_path) + 1:] if name.startswith(local_base_path) else name
                if hashmap and hashmap[name] == calculate_crc32c(os.path.join(local_base_path, name)):
                    continue
                results.append(name)
        return results

    @classmethod
    def get_hashmap(cls, local_base_path):
        files = cls.get_files_to_upload(local_base_path)
        hashmap = dict()
        for file in files:
            path = os.path.join(local_base_path, file)
            hashmap[file] = calculate_crc32c(path)
        return hashmap

    @classmethod
    def upload(cls, context, local_path, volume_id, remote_path, progressable=None):
        client = SavviHubClient(token=context.token)
        file_create_resp = client.volume_file_create(volume_id, remote_path, is_dir=False, raise_error=True)
        file_object = SavviHubFileObject(file_create_resp.json())

        dirname = os.path.dirname(local_path)
        basename = os.path.basename(local_path)
        u = UploadableFileObject(file_object.upload_url.get("url"), dirname, basename)
        u.upload(progressable=progressable)
        resp = client.volume_file_uploaded(volume_id, remote_path, raise_error=True)
        return SavviHubFileObject(resp.json())

    @classmethod
    def bulk_upload(cls, context, local_base_path, local_file_paths, volume_id, remote_base_path, *, progressable=None):
        if len(local_file_paths) <= 0:
            return

        session = FuturesSession(max_workers=context.parallel)
        client = SavviHubClient(token=context.token, session=session)

        futures = []
        for local_file_path in local_file_paths:
            future = client.volume_file_create(
                volume_id,
                os.path.join(remote_base_path, local_file_path),
                is_dir=False,
                hooks=default_hooks()
            )
            futures.append(future)
        resps = wait_all_futures(futures)

        futures = []
        for i, resp in enumerate(resps):
            file_object = SavviHubFileObject(resp.json())

            u = UploadableFileObject(file_object.upload_url.get("url"), local_base_path, local_file_paths[i])
            futures.append(u.upload(session, progressable=progressable))

        wait_all_futures(futures)

        futures = []
        for local_file_path in local_file_paths:
            future = client.volume_file_uploaded(
                volume_id,
                os.path.join(remote_base_path, local_file_path),
                hooks=default_hooks(),
            )
            futures.append(future)

        resps = wait_all_futures(futures)
        return [SavviHubFileObject(resp.json()) for resp in resps]
