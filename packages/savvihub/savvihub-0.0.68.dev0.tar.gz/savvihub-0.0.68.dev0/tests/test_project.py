from tests.conftest import BaseTestCase


class ProjectTest(BaseTestCase):
    def test_project(self):
        result = self.runner.invoke(['project', 'status'])
        assert f'Workspace: {self.workspace_name}' in result.output
        assert f'Project: {self.project_name}' in result.output
