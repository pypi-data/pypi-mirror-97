import click
from click.testing import CliRunner
from tests.mock_backend import GridAIBackenedTestServer
from tests.utilities import create_test_credentials

from grid import cli
from grid.client import Grid
import grid.globals as env


class TestView:
    """Test case for the view command"""
    @classmethod
    def setup_class(cls):
        cls.runner = CliRunner()

        cls.credentials_path = 'tests/data/credentials.json'
        cls.test_run = 'manual-test-run'
        cls.test_exp = 'manual-test-run-exp0'

        # Setup the global DEBUG flag to True.
        env.DEBUG = True

        #  Monkey patches the GraphQL client to read from a local schema.
        def monkey_patch_client(self):
            self.client = GridAIBackenedTestServer()

        #  skipcq: PYL-W0212
        Grid._init_client = monkey_patch_client

        create_test_credentials()

    def monkey_patched_method(self, *args, **kwargs):
        return True

    def monkey_patch_grid_status(self, *args, **kwargs):
        result = {
            'getRuns': [{
                'name': self.test_run,
                'resourceUrls': {
                    'tensorboard': ['http://test-url-tensorboard']
                }
            }]
        }
        return result

    def monkey_patch_grid_status_not_ready(self, *args, **kwargs):
        result = {'getRuns': [{'name': self.test_run, 'resourceUrls': {}}]}
        return result

    def monkey_patch_exception(self, *args, **kwargs):
        raise click.ClickException('test')

    def test_view_opens_browser(self, monkeypatch):
        """grid view RUN_ID opens browser."""
        monkeypatch.setattr(click, 'launch', self.monkey_patched_method)

        result = self.runner.invoke(cli.view, [self.test_run])

        assert result.exit_code == 0
        assert 'http' in result.output
        assert 'run' in result.output
        assert self.test_run in result.output

        result = self.runner.invoke(cli.view, [f'{self.test_run}-exp1'])
        assert result.exit_code == 0
        assert 'http' in result.output
        assert 'experiment' in result.output
        assert self.test_run in result.output

    def test_view_exception(self, monkeypatch):
        """grid view raises exception if resource URL not available."""
        monkeypatch.setattr(click, 'launch', self.monkey_patched_method)

        old_status = Grid.status
        monkeypatch.setattr(Grid, 'status', self.monkey_patch_exception)

        result = self.runner.invoke(cli.view, [self.test_run, 'tensorboard'])
        assert result.exit_code == 1
        assert result.exception

        result = self.runner.invoke(cli.view, [self.test_run, 'tensorboard'])
        assert result.exit_code == 1
        assert result.exception

        # Set attribute again.
        monkeypatch.setattr(Grid, 'status', old_status)

    def test_view_right_url_for_services(self, monkeypatch):
        """grid view generates the right URLs for services."""
        monkeypatch.setattr(click, 'launch', self.monkey_patched_method)

        old_status = Grid.status
        monkeypatch.setattr(Grid, 'status', self.monkey_patch_grid_status)

        for arg in [self.test_run, self.test_exp]:
            result = self.runner.invoke(cli.view, [arg, 'tensorboard'])
            assert result.exit_code == 0
            assert not result.exception
            assert 'http' in result.output

            # Test that the Tensorboard URL constructor is there.
            assert 'scalars&regexInput=' in result.output

        # Set attribute again.
        monkeypatch.setattr(Grid, 'status', old_status)

    def test_view_fail_tensorboard_not_ready(self, monkeypatch):
        """grid view fails when tensorboard is not ready."""
        old_status = Grid.status
        monkeypatch.setattr(Grid, 'status',
                            self.monkey_patch_grid_status_not_ready)

        result = self.runner.invoke(cli.view, [self.test_run, 'tensorboard'])
        assert result.exit_code == 1
        assert result.exception
        assert "Tensorboard isn't ready yet" in result.output

        # Set attribute again.
        monkeypatch.setattr(Grid, 'status', old_status)
