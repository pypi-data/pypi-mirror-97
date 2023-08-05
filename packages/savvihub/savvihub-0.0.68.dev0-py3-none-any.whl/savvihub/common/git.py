import re
import subprocess
import tempfile

from pathlib import Path


class InvalidGitRepository(Exception):
    pass


class GitRepository:
    def __init__(self):
        self.remote = 'origin'

        self.get_root_path()
        self.get_github_repo()
        self.get_remote_revision_or_branch()

    @staticmethod
    def get_root_path():
        try:
            return subprocess.check_output(['git', 'rev-parse', '--show-toplevel'], stderr=subprocess.DEVNULL).decode('utf-8').strip()
        except subprocess.CalledProcessError:
            raise InvalidGitRepository("Are you running in git repository?")

    def get_savvihub_config_file_path(self):
        return Path(self.get_root_path()) / ".savvihub" / "config"

    def get_github_repo(self):
        remotes = subprocess.check_output(['git', 'remote']).decode('utf-8').strip().split('\n')
        for remote in remotes:
            try:
                remote_url = subprocess.check_output(['git', 'remote', 'get-url', remote]).strip().decode('utf-8')
                if 'github.com' not in remote_url:
                    continue
            except subprocess.CalledProcessError:
                raise InvalidGitRepository(
                    "github.com is not found in remote repositories. You should add your repo to github first.")

            regex = re.compile(r'((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)?(/)?')
            repo = regex.search(remote_url).group(7).split('/')

            self.remote = remote

            return repo[-2], repo[-1]

    def get_active_branch_name(self):
        head_dir = Path(self.get_root_path()) / ".git" / "HEAD"
        with head_dir.open("r") as f:
            content = f.read().splitlines()

        for line in content:
            if line[0:4] == "ref:":
                return line.partition("refs/heads/")[2]

    @staticmethod
    def get_revision_hash():
        try:
            return subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode("utf-8").strip()
        except subprocess.CalledProcessError:
            raise InvalidGitRepository("git rev-parse HEAD failed. Are you running in git repository?")

    def get_latest_commit_revision(self, branch):
        return subprocess.check_output(['git', 'rev-parse', branch]).decode("utf-8").strip()

    def get_commit_message(self, revision, format='%h %s (%cr) <%an>'):
        return subprocess.check_output(['git', 'log', '--format=%s' % format, '-n', '1', revision]).decode('utf-8').strip()

    def check_revision_in_remote(self, revision):
        remote_branches = subprocess.check_output(['git', 'branch', '-r', '--contains', revision])\
            .decode('utf-8').strip().split('\n')
        for remote_branch in remote_branches:
            if remote_branch.startswith(f'{self.remote}/'):
                return True
        return False

    def get_remote_revision_or_branch(self):
        revision = self.get_revision_hash()
        if self.check_revision_in_remote(revision):
            # with revision and patch
            return revision, 'HEAD', True
        else:
            # with remote branch and patch
            try:
                upstream_branch_name = subprocess.check_output(
                    ['git', 'rev-parse', '--abbrev-ref', '--symbolic-full-name', '@{u}']).decode().strip()
            except subprocess.CalledProcessError:
                raise InvalidGitRepository(
                    f"You should push your branch <{self.get_active_branch_name()}> to github first!")

            revision = self.get_latest_commit_revision(upstream_branch_name)

            return revision, upstream_branch_name, False

    def get_current_diff_status(self, revision_or_branch):
        untracked_files = subprocess.check_output(['git', 'ls-files', '-o', '--exclude-standard']).decode('utf-8').strip().split('\n')
        uncommitted_files = subprocess.check_output(['git', 'diff', '--stat', revision_or_branch]).decode('utf-8').strip().split('\n')

        untracked_files = [x for x in untracked_files if len(x) > 0]
        uncommitted_files = [x for x in uncommitted_files if len(x) > 0]

        return len(untracked_files) > 0 or len(uncommitted_files) > 0, {
            'untracked': untracked_files,
            'uncommitted': uncommitted_files,
        }

    def get_current_diff_file(self, revision_or_branch, with_untracked=True):
        fp = tempfile.NamedTemporaryFile(suffix='.patch')

        untracked_files = []
        if with_untracked:
            untracked_files = subprocess.check_output(['git', 'ls-files', '-o', '--exclude-standard']).decode('utf-8').strip().split('\n')
            untracked_files = [x for x in untracked_files if len(x) > 0]
            for f in untracked_files:
                subprocess.check_output(['git', 'add', '-N', f])

        subprocess.call(['git', 'diff', '-p', '--binary', f'{revision_or_branch}'], stdout=fp)

        if with_untracked:
            for f in untracked_files:
                subprocess.check_output(['git', 'reset', '--', f])

        return fp

