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

    def test_logs_without_arguments(self):
        """grid logs without arguments fails"""
        result = RUNNER.invoke(cli.logs, [])
        assert result.exit_code == 2
        assert result.exception

    def test_logs_fails_with_ex(self, monkeypatch):
        """grid logs fails with exception"""
        def get_archive_experiment_logs(*args, **kwargs):
            raise Exception()

        monkeypatch.setattr(resolvers, 'get_archive_experiment_logs',
                            get_archive_experiment_logs)
        result = RUNNER.invoke(cli.logs, ["test-run"])
        assert result.exit_code == 1
        assert result.exception
        assert 'Failed to make query' in result.output

    def test_experiment_wthout_logs_raises_error(self, monkeypatch):
        """grid logs on experiment without archive logs raises exception"""
        def get_archive_experiment_logs(*args, **kwargs):
            return []

        monkeypatch.setattr(resolvers, 'get_archive_experiment_logs',
                            get_archive_experiment_logs)
        result = RUNNER.invoke(cli.logs, ["test-run"])
        assert result.exit_code == 1
        assert result.exception
        assert 'No logs available' in result.output
