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

    def test_cancel_without_arguments(self):
        """grid cancel without arguments fails"""
        result = RUNNER.invoke(cli.cancel, [])
        assert result.exit_code == 2
        assert result.exception

    def test_cancel_experiment(self):
        """grid cancel experiments with single and multi-input"""
        experiments = [f'test-experiment-exp{i}' for i in range(5)]

        result = RUNNER.invoke(cli.cancel, experiments[0])
        assert result.exit_code == 0
        assert not result.exception

        result = RUNNER.invoke(cli.cancel, experiments)
        assert result.exit_code == 0
        assert not result.exception

    def test_cancel_runs(self):
        """grid cancel Runs with single and multi-input"""
        runs = [f'test-run-{i}' for i in range(5)]
        result = RUNNER.invoke(cli.cancel, runs[0])
        assert result.exit_code == 0
        assert not result.exception

        result = RUNNER.invoke(cli.cancel, runs)
        assert result.exit_code == 0
        assert not result.exception

    def test_cancel_run_fails_with_no_experiments(self, monkeypatch):
        """grid cancel Run fails if Run has no experiments."""
        test_run = 'test-no-experiments-run'

        def mp_get_experiments(*args, **kwargs):
            return []

        monkeypatch.setattr(resolvers, 'get_experiments', mp_get_experiments)
        result = RUNNER.invoke(cli.cancel, test_run)
        assert result.exit_code == 1
        assert result.exception

    def test_cancel_run_fails_because_run_does_not_exist(self, monkeypatch):
        """grid cancel Run fails if Run does not exist."""
        test_run = 'test-no-experiments-run'

        def mp_get_experiments(*args, **kwargs):
            return {'error': 'Run does not exist'}

        monkeypatch.setattr(resolvers, 'get_experiments', mp_get_experiments)
        result = RUNNER.invoke(cli.cancel, test_run)
        assert result.exit_code == 1
        assert result.exception

    def test_only_cancels_experiments_in_not_terminal_state(self, monkeypatch):
        """grid cancel skips experiments in a terminal state."""

        not_cancelled_experiments = [
            'test-run-exp0', 'test-run-exp1', 'test-run-exp2'
        ]
        cancelled_experiment = 'test-run-exp3'

        def mp_get_experiments(*args, **kwargs):
            return [{
                'experimentId': not_cancelled_experiments[0],
                'status': 'failed'
            }, {
                'experimentId': not_cancelled_experiments[1],
                'status': 'succeeded'
            }, {
                'experimentId': not_cancelled_experiments[2],
                'status': 'cancelled'
            }, {
                'experimentId': cancelled_experiment,
                'status': 'running'
            }]

        monkeypatch.setattr(resolvers, 'get_experiments', mp_get_experiments)
        result = RUNNER.invoke(cli.cancel, 'test-run')
        assert result.exit_code == 0
        assert cancelled_experiment in result.output
        assert all(e not in result.output for e in not_cancelled_experiments)
