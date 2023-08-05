import tempfile
from typing import Optional, Union, Iterable, Text, IO, Any, Mapping
from unittest import TestCase

from click.testing import Result
from typer.testing import CliRunner as TyperCliRunner

from savvihub import Context
from savvihub.api.savvihub import SavviHubClient
from savvihub.common import constants
from savvihub.common.utils import random_string
from savvihub.savvihub_cli.main import app


class CliRunner(TyperCliRunner):
    def invoke(
        self,
        args: Optional[Union[str, Iterable[str]]] = None,
        input: Optional[Union[bytes, Text, IO[Any]]] = None,
        env: Optional[Mapping[str, str]] = None,
        color: bool = False,
        allow_fail: bool = False,
        **extra: Any,
    ) -> Result:
        result = super().invoke(app, args, input, env, catch_exceptions=False, color=color, **extra)
        if not allow_fail:
            assert result.exit_code == 0, result.output
        return result


class BaseTestCase(TestCase):
    def setUp(self):
        super().setUp()
        constants.TEST = True
        self._auto_savvi_init()
        self._monkey_patch(self.token, self.workspace_name, self.project_name)
        self.context = Context(auth_required=True, project_required=True)
        self.client = SavviHubClient(token=self.context.token)
        self.runner = CliRunner()

    def _auto_savvi_init(self):
        # user init
        username = random_string()
        jwt_client = SavviHubClient()
        r = jwt_client.post('/api/v1/accounts/signup', {
            'email': f'{username}@savvihub.test',
            'username': username,
            'name': username,
            'password': 'testtest',
            'invitation_token': 'invitation_token_for_cli_test',
        }, raise_error=True).json()
        jwt_client.session.headers['Authorization'] = f'JWT {r["token"]}'

        cli_token = jwt_client.check_signin_token()
        jwt_client.post('/api/v1/accounts/signin/cli/confirm', {
            'cli_token': cli_token,
        }, raise_error=True)

        success, access_token = jwt_client.check_signin(cli_token)
        if not success:
            raise Exception('Signin Failed')

        # project init
        access_token_client = SavviHubClient(token=access_token)
        workspace_name = access_token_client.workspace_list()[0].name
        project_name = random_string()
        me = access_token_client.get_my_info()
        access_token_client.project_github_create(workspace_name, project_name, me.username, project_name)

        self.token = access_token
        self.workspace_name = workspace_name
        self.project_name = project_name

    @staticmethod
    def _monkey_patch(token, workspace_name, project_name):
        class MockConfig:
            def __init__(self):
                self.token = token
                self.workspace = workspace_name
                self.project = project_name

        class MockGitRepo:
            def check_revision_in_remote(self, ref):
                return True

            def get_remote_revision_or_branch(self):
                return 'dummy-ref', 'dummy-branch', False

            def get_commit_message(self, ref):
                return 'dummy-commit-message'

            def get_current_diff_status(self, ref):
                return True, {
                    'untracked': ['dummy-untracked-file.py', 'dummy-untracked-file.go'],
                    'uncommitted': ['dummy-uncommitted-file.py', 'dummy-uncommitted-file.go'],
                }

            def get_current_diff_file(self, git_ref, with_untracked=True):
                fp = tempfile.NamedTemporaryFile(suffix='.patch')
                fp.write('dummy-diff'.encode())
                return fp

        def context_init(
            self,
            auth_required=False,
            user_required=False,
            project_required=False,
            experiment_required=False,
        ):
            mock_config = MockConfig()
            self.global_config = mock_config

            if user_required:
                self.user = self.get_my_info()

            if project_required:
                self.git_repo = MockGitRepo()
                self.project_config = mock_config
                self.project = self.get_project()

            if experiment_required:
                raise NotImplementedError('Please implement this..')

        Context.__init__ = context_init
