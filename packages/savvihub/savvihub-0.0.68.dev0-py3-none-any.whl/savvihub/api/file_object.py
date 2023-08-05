import os

import requests

from savvihub.common.utils import read_in_chunks


class UploadableFileObject:
    def __init__(self, url, base_path, path):
        self.url = url
        self.base_path = base_path
        self.full_path = os.path.join(base_path, path)
        self.path = path

    def upload_chunks(self, *, callback=None):
        return read_in_chunks(self.full_path, callback=callback)

    def upload_hooks(self, *, log=None):
        def fn(resp, **kwargs):
            resp.raise_for_status()
        return {
            'response': fn,
        }

    def upload(self, session=requests.Session(), progressable=None):
        progress_callback = None
        if progressable:
            progress = progressable(length=os.path.getsize(self.full_path), label=self.path)
            progress_callback = lambda data: progress.update(len(data))

        future = session.put(
            self.url,
            data=self.upload_chunks(callback=progress_callback),
            headers={
                'content-type': 'application/octet-stream',
            },
            hooks=self.upload_hooks(),
        )
        return future


class DownloadableFileObject:
    def __init__(self, url, base_path, path, size=None):
        self.url = url
        self.full_path = os.path.join(base_path, path)
        self.size = size

    def download_hooks(self, *, callback=None):
        def fn(resp, **kwargs):
            os.makedirs(os.path.dirname(self.full_path), exist_ok=True)
            with open(self.full_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
                    if callback:
                        callback(chunk)
        return {
            'response': fn,
        }

    def download(self, session=requests.Session(), progressable=None):
        progress_callback = None
        if progressable and self.size:
            progress = progressable(length=self.size, label=self.full_path)
            progress_callback = lambda data: progress.update(len(data))

        future = session.get(
            self.url,
            stream=True,
            hooks=self.download_hooks(callback=progress_callback)
        )
        return future
