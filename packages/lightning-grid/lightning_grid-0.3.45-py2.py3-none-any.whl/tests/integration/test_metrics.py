from click.testing import CliRunner
from tests.mock_backend import resolvers
from tests.utilities import create_test_credentials
from tests.utilities import monkey_patch_client

from grid import cli
import grid.client as grid

RUNNER = CliRunner()


class TestMetrics:
    @classmethod
    def setup_class(cls):
        grid.Grid._init_client = monkey_patch_client
        grid.gql = lambda x: x

        create_test_credentials()

    def test_metrics_without_arguments(self):
        """grid metrics without arguments fails"""
        result = RUNNER.invoke(cli.metrics, [])
        assert result.exit_code == 2
        assert result.exception

    def test_metrics_fails_with_ex(self, monkeypatch):
        """grid metrics fails with exception"""
        def get_experiment_scalar_logs(*args, **kwargs):
            raise Exception()

        monkeypatch.setattr(resolvers, 'get_experiment_scalar_logs',
                            get_experiment_scalar_logs)
        result = RUNNER.invoke(cli.metrics, ["test-run", "train_loss"])
        assert result.exit_code == 1
        assert result.exception
        assert 'Failed to make query' in result.output

    def test_experiment_wthout_metrics_raises_error(self, monkeypatch):
        """grid logs on experiment without metrics raises exception"""
        def get_experiment_scalar_logs(*args, **kwargs):
            return []

        monkeypatch.setattr(resolvers, 'get_experiment_scalar_logs',
                            get_experiment_scalar_logs)
        result = RUNNER.invoke(cli.metrics, ["test-run", "train_loss"])
        assert result.exit_code == 1
        assert result.exception
        assert 'No metrics available' in result.output
