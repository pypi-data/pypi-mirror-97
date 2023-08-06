import click
from gql.transport.exceptions import TransportQueryError
import pytest
from tests.utilities import create_test_credentials
from tests.utilities import monkey_patch_client

import grid.client as grid
import grid.observables.interactive_node as interactive_node_observable


def mp_execute(*args, **kwargs):
    raise Exception("{'message':'not found'}")


class TestIneteractiveObservable:
    @classmethod
    def setup_class(cls):
        create_test_credentials()

        grid.Grid._init_client = monkey_patch_client
        interactive_node_observable.gql = lambda x: x

        cls.grid = grid.Grid(load_local_credentials=False)
        cls.grid._init_client()

    def test_get(self, capsys):
        interactive_node_observable.env.SHOW_PROCESS_STATUS_DETAILS = False
        interactive_node_observable.env.DEBUG = True
        obsevable = interactive_node_observable.InteractiveNode(
            client=self.grid.client)

        obsevable.get()
        captured = capsys.readouterr()

        expected_columns = ['Name', 'Status']
        for column in expected_columns:
            assert column in captured.out

    def tets_get_handles_error(self, monkeypatch):
        def mp_transport_error(*args, **kwargs):
            raise TransportQueryError('test')

        monkeypatch.setattr(self.grid.client, 'execute', mp_transport_error)
        obsevable = interactive_node_observable.InteractiveNode(
            client=self.grid.client)
        with pytest.raises(click.ClickException):
            obsevable.get()
