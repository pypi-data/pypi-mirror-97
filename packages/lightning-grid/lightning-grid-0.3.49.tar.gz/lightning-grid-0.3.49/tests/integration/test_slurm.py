from click.testing import CliRunner
from tests.mock_backend import resolvers
from tests.utilities import create_test_credentials
from tests.utilities import monkey_patch_client

from grid import cli
import grid.client as grid

RUNNER = CliRunner()


class TestCancel:
    @classmethod
    def setup_class(cls):
        grid.Grid._init_client = monkey_patch_client

        grid.gql = lambda x: x

        create_test_credentials()

        cls.cluster_alias = 'cluster_alias'

    def test_slurm_logs_succeeds(self):
        """grid slurm logs succeeds"""
        result = RUNNER.invoke(cli.slurm, ["logs"])
        assert result.exit_code == 0
        assert not result.exception

    def test_slurm_cancel_succeeds(self):
        """grid slurm cancel succeeds"""
        result = RUNNER.invoke(cli.slurm, ["cancel"])
        assert result.exit_code == 0
        assert not result.exception

    def test_slurm_status_fails(self, monkeypatch):
        """grid slurm status fails"""
        def get_slurm_status(*args, **kwargs):
            return {
                'success': False,
            }

        monkeypatch.setattr(resolvers, 'get_slurm_status', get_slurm_status)
        result = RUNNER.invoke(cli.slurm, [
            "status", "--run_name", "run", "--cluster_alias",
            self.cluster_alias
        ])
        assert result.exit_code == 0
        assert not result.exception
        assert 'Failed to get status' in result.output

    def test_slurm_status_query_fails(self, monkeypatch):
        """grid slurm status query fails"""
        def get_slurm_status(*args, **kwargs):
            return None

        monkeypatch.setattr(resolvers, 'get_slurm_status', get_slurm_status)
        result = RUNNER.invoke(cli.slurm, [
            "status", "--run_name", "run", "--cluster_alias",
            self.cluster_alias
        ])
        assert result.exit_code == 1
        assert result.exception
        assert 'Failed to send status request' in result.output

    def test_slurm_status_succeeds(self, monkeypatch):
        """grid slurm status succeeds"""
        def get_slurm_status(*args, **kwargs):
            return {
                'success': True,
            }

        monkeypatch.setattr(resolvers, 'get_slurm_status', get_slurm_status)
        result = RUNNER.invoke(cli.slurm, [
            "status", "--run_name", "run", "--cluster_alias",
            self.cluster_alias
        ])
        assert result.exit_code == 0
        assert not result.exception
        assert 'Finished getting status from cluster' in result.output

    def test_slurm_submit_fails(self, tmp_path, monkeypatch):
        """grid slurm submit fails"""

        script = tmp_path / "script.py"
        script.write_text("")

        def train_slurm_script(*args, **kwargs):
            return {
                'success': False,
            }

        monkeypatch.setattr(resolvers, 'train_slurm_script',
                            train_slurm_script)
        result = RUNNER.invoke(cli.slurm, [
            "train",
            script.as_posix(),
            "--cluster_alias",
            self.cluster_alias,
        ],
                               input='y\ny\n')
        assert result.exit_code == 1
        assert result.exception
        assert 'Unable to submit train task with error' in result.output

    def test_slurm_submit_fails_with_ex(self, tmp_path, monkeypatch):
        """grid slurm submit fails with exception"""

        script = tmp_path / "script.py"
        script.write_text("")

        def train_slurm_script(*args, **kwargs):
            raise Exception()

        monkeypatch.setattr(resolvers, 'train_slurm_script',
                            train_slurm_script)
        result = RUNNER.invoke(cli.slurm, [
            "train",
            script.as_posix(),
            "--cluster_alias",
            self.cluster_alias,
        ],
                               input='y\ny\n')
        assert result.exit_code == 1
        assert result.exception
        assert 'Failed to start training' in result.output

    def test_slurm_submit_succeeds(self, tmp_path, monkeypatch):
        """grid slurm submit succeeds"""

        script = tmp_path / "script.py"
        script.write_text("")

        def train_slurm_script(*args, **kwargs):
            return {
                'success': True,
            }

        monkeypatch.setattr(resolvers, 'train_slurm_script',
                            train_slurm_script)
        result = RUNNER.invoke(cli.slurm, [
            "train",
            script.as_posix(),
            "--cluster_alias",
            self.cluster_alias,
        ],
                               input='y\ny\n')
        assert result.exit_code == 0
        assert not result.exception
        assert 'Run submitted!' in result.output

    def test_slurm_get_token_succeeds(self, tmp_path, monkeypatch):
        """grid slurm get-token succeeds"""
        def get_slurm_auth_token(*args, **kwargs):
            return {
                'success': True,
            }

        monkeypatch.setattr(resolvers, 'get_slurm_auth_token',
                            get_slurm_auth_token)
        result = RUNNER.invoke(cli.slurm, ["get-token"])
        assert result.exit_code == 0
        assert not result.exception
        assert 'Generating token for grid-daemon use' in result.output

    def test_slurm_get_token_fails(self, monkeypatch):
        """grid slurm get-token fails"""
        def get_slurm_auth_token(*args, **kwargs):
            return {
                'success': False,
            }

        monkeypatch.setattr(resolvers, 'get_slurm_auth_token',
                            get_slurm_auth_token)
        result = RUNNER.invoke(cli.slurm, ["get-token"])
        assert result.exit_code == 1
        assert result.exception
        assert 'Failed to create auth token.' in result.output

    def test_slurm_get_token_fails_with_ex(self, monkeypatch):
        """grid slurm get-token fails with exception"""
        def get_slurm_auth_token(*args, **kwargs):
            raise Exception()

        monkeypatch.setattr(resolvers, 'get_slurm_auth_token',
                            get_slurm_auth_token)
        result = RUNNER.invoke(cli.slurm, ["get-token"])
        assert result.exit_code == 1
        assert result.exception
        assert 'Failed to create auth token.' in result.output
