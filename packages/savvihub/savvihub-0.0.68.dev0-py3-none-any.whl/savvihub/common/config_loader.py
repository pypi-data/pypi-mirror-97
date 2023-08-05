import os
import sys

import toml
from jsonschema import validate, ValidationError

from savvihub.common.constants import DEFAULT_CONFIG_PATH


class ConfigLoader:
    def __init__(self, filename, schema):
        self.filename = filename
        self.schema = schema
        try:
            self.data = self._load()
        except toml.decoder.TomlDecodeError as e:
            print(f"fatal: bad config line {e.lineno} in file {filename}")
            sys.exit(1)

        self._validate()

    def _load(self):
        try:
            with open(self.filename) as f:
                documents = toml.load(f)
                if not documents:
                    return None
                data_dict = dict()
                for item, doc in documents.items():
                    data_dict[item] = doc
                return data_dict
        except FileNotFoundError:
            return {}

    def _validate(self):
        try:
            validate(instance=self.data, schema=self.schema)
        except ValidationError as e:
            return e.schema["Validation Error"]

    def save(self):
        self._validate()
        os.makedirs(os.path.dirname(self.filename), exist_ok=True)
        try:
            with open(self.filename, 'w') as f:
                toml.dump(self.data, f)
        except EnvironmentError:
            print('Error: Config file not found')


class ProjectConfigLoader(ConfigLoader):
    schema = {
        "anyOf": [
            {},
            {
                "type": "object",
                "properties": {
                    "savvihub": {
                        "type": "object",
                        "properties": {
                            "url": {"type": "string"},
                            "workspace": {"type": "string"},
                            "project": {"type": "string"},
                        },
                    },
                },
            },
        ],
    }

    def __init__(self, filename):
        super().__init__(filename, self.schema)

    @property
    def workspace(self):
        return self.data.get('savvihub', {}).get('workspace')

    @property
    def project(self):
        return self.data.get('savvihub', {}).get('project')

    @property
    def url(self):
        return self.data.get('savvihub', {}).get('project')

    def set_savvihub(self, url=None, workspace=None, project=None):
        savvihub = self.data.get('savvihub', {})
        if url:
            savvihub['url'] = url
        if workspace:
            savvihub['workspace'] = workspace
        if project:
            savvihub['project'] = project
        self.data['savvihub'] = savvihub
        self.save()


class GlobalConfigLoader(ConfigLoader):
    schema = {
        "anyOf": [
            {},
            {
                "type": "object",
                "properties": {
                    "user": {
                        "type": "object",
                        "properties": {
                            "token": {"type": "string"},
                        },
                    },
                }
            },
        ]
    }

    def __init__(self):
        super().__init__(DEFAULT_CONFIG_PATH, self.schema)

    @property
    def token(self):
        return self.data.get('user', {}).get('token')

    def set_user(self, token=None):
        user = self.data.get('user', {})
        if token:
            user['token'] = token
        self.data['user'] = user
        self.save()
