from click.testing import CliRunner
from tests.mock_backend import resolvers
from tests.utilities import create_test_credentials
from tests.utilities import monkey_patch_client

from grid import cli
import grid.client as grid

RUNNER = CliRunner()


class TestDelete:
    @classmethod
    def setup_class(cls):
        grid.Grid._init_client = monkey_patch_client
        grid.gql = lambda x: x

        create_test_credentials()

    def test_delete_fails_without_arguments(self):
        """grid delete fails without arguments"""
        result = RUNNER.invoke(cli.delete, [])
        assert result.exit_code == 2
        assert result.exception

    def test_delete_deletes_runs_and_experiments(self):
        """grid delete fails without arguments"""
        run_id = 'test-run'
        result = RUNNER.invoke(cli.delete, [run_id], input='y\n')
        assert result.exit_code == 0
        assert not result.exception
        assert 'Are you sure you want to do this?' in result.output

        experiment_id = 'test-run-exp0'
        result = RUNNER.invoke(cli.delete, [experiment_id], input='y\n')
        assert result.exit_code == 0
        assert not result.exception
        assert 'Are you sure you want to do this?' in result.output

    def test_delete_deletes_warning_prevents_delete(self):
        """grid delete warning prevents a deletion"""
        run_id = 'test-run'
        result = RUNNER.invoke(cli.delete, [run_id], input='N\n')
        assert result.exit_code == 1
        assert 'Are you sure you want to do this?' in result.output

    def test_delete_run_fails(self, monkeypatch):
        """grid delete run fails with exception"""
        def delete_run(*args, **kwargs):
            return {"success": False}

        monkeypatch.setattr(resolvers, 'delete_run', delete_run)
        run_id = 'test-run'
        result = RUNNER.invoke(cli.delete, [run_id], input='y\n')
        assert result.exit_code == 1
        assert result.exception
        assert 'Failed to delete run' in result.output

    def test_delete_run_fails_with_exception(self, monkeypatch):
        """grid delete run fails with exception"""
        def delete_run(*args, **kwargs):
            raise Exception()

        monkeypatch.setattr(resolvers, 'delete_run', delete_run)
        run_id = 'test-run'
        result = RUNNER.invoke(cli.delete, [run_id], input='y\n')
        assert result.exit_code == 1
        assert result.exception
        assert 'Failed to delete run' in result.output

    def test_delete_experiment_fails(self, monkeypatch):
        """grid delete experiment fails"""
        def delete_experiment(*args, **kwargs):
            return {"success": False}

        monkeypatch.setattr(resolvers, 'delete_experiment', delete_experiment)
        experiment_id = 'test-run-exp0'
        result = RUNNER.invoke(cli.delete, [experiment_id], input='y\n')
        assert result.exit_code == 1
        assert result.exception
        assert 'Failed to delete experiment' in result.output

    def test_delete_experiment_fails_with_exception(self, monkeypatch):
        """grid delete experiment fails with exception"""
        def delete_experiment(*args, **kwargs):
            raise Exception()

        monkeypatch.setattr(resolvers, 'delete_experiment', delete_experiment)
        experiment_id = 'test-run-exp0'
        result = RUNNER.invoke(cli.delete, [experiment_id], input='y\n')
        assert result.exit_code == 1
        assert result.exception
        assert 'Failed to delete experiment' in result.output
