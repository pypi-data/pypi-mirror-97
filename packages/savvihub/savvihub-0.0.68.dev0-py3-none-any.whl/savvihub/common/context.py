import os
import sys
from typing import Optional

import typer

from savvihub.api.types import SavviHubUser, SavviHubProject
from savvihub.common.config_loader import GlobalConfigLoader, ProjectConfigLoader
from savvihub.common.experiment import Experiment
from savvihub.common.git import GitRepository


class Value:
    def __init__(self, global_config_yml=None, savvihub_file_yml=None, env=None, computed=None, default_value=None):
        self.global_config_yml = global_config_yml
        self.savvihub_file_yml = savvihub_file_yml
        self.env = env
        self.computed = computed
        self.default_value = default_value


class Context:
    global_config = None
    project_config = None
    git_repo = None

    user: Optional[SavviHubUser] = None
    project: Optional[SavviHubProject] = None
    experiment: Optional[Experiment] = None

    experiment_id = os.environ.get("SAVVIHUB_EXPERIMENT_ID", None)
    access_token = os.environ.get("SAVVIHUB_ACCESS_TOKEN", None)
    parallel = os.environ.get("SAVVIHUB_PARALLEL", 20)

    def __init__(self, auth_required=False, user_required=False, project_required=False, experiment_required=False):
        self.global_config = self.load_global_config()

        if auth_required:
            self.verify_auth()

        if user_required:
            self.user = self.get_my_info()
            if self.user is None:
                typer.echo('Token expired. You should call `sv init` first.')
                sys.exit(1)

        if project_required:
            self.git_repo = GitRepository()
            self.project_config = self.load_project_config(self.git_repo.get_savvihub_config_file_path())
            self.project = self.get_project()

            if self.project is None:
                typer.echo('Project not found. Run `sv project init`.')
                sys.exit(1)

        if experiment_required:
            self.experiment = self.get_experiment()

            if self.experiment is None:
                typer.echo('Experiment ID and access token required.')
                sys.exit(1)

    def verify_auth(self):
        from savvihub.api.savvihub import SavviHubClient
        client = SavviHubClient(token=self.token)
        return client.verify_access_token()

    def get_my_info(self):
        from savvihub.api.savvihub import SavviHubClient
        client = SavviHubClient(token=self.token)
        return client.get_my_info()

    def get_experiment(self):
        if self.experiment_id is None or self.access_token is None:
            raise Exception('Experiment ID and access token required.')

        from savvihub.api.savvihub import SavviHubClient
        client = SavviHubClient(token=self.token)
        experiment = client.experiment_id_read(self.experiment_id, raise_error=True)
        if experiment is None:
            return None

        return Experiment.from_given(experiment, client)

    def get_project(self):
        from savvihub.api.savvihub import SavviHubClient
        client = SavviHubClient(token=self.token)
        project = client.project_read(self.project_config.workspace, self.project_config.project)
        return project

    @property
    def authorized_client(self):
        from savvihub.api.savvihub import SavviHubClient
        return SavviHubClient(token=self.token)

    @property
    def token(self):
        if self.access_token:
            return self.access_token
        if self.global_config.token:
            return self.global_config.token
        typer.echo('Login required. You should call `sv init` first.')
        sys.exit(1)

    @staticmethod
    def load_global_config():
        return GlobalConfigLoader()

    @staticmethod
    def load_project_config(project_config_path):
        if not project_config_path:
            return None
        return ProjectConfigLoader(project_config_path)
