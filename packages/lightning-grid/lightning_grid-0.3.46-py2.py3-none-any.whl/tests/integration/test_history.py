from click.testing import CliRunner
from tests.utilities import create_local_schema_client

from grid import cli
from grid.client import Grid

RUNNER = CliRunner()


def monkey_patch_client(self) -> None:
    """Monkey patches the GraphQL client to read from a local schema."""
    self.client = create_local_schema_client()


def monkey_patch_history(self, *args, **kwargs) -> None:
    """Monkey patches history() to avoid making a backend query."""
    return


def test_history_without_arguments_succeeds(monkeypatch):
    """grid history without arguments succeeds"""
    monkeypatch.setattr(Grid, '_init_client', monkey_patch_client)
    monkeypatch.setattr(Grid, 'history', monkey_patch_history)

    result = RUNNER.invoke(cli.history, [])
    assert result.exit_code == 0
    assert not result.exception
