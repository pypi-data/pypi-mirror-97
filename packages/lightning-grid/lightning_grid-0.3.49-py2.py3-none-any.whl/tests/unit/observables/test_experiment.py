import click
import pytest
from tests.utilities import create_test_credentials
from tests.utilities import monkey_patch_client
import websockets

import grid.client as grid
import grid.observables.experiment as experiment_observable


def mp_execute(*args, **kwargs):
    raise Exception("{'message':'not found'}")


class TestExperimentObservable:
    @classmethod
    def setup_class(cls):
        create_test_credentials()

        grid.Grid._init_client = monkey_patch_client

        experiment_observable.gql = lambda x: x

        cls.grid = grid.Grid(load_local_credentials=False)
        cls.grid._init_client()

    def test_get(self, capsys):
        obsevable = experiment_observable.Experiment(
            client=self.grid.client, identifier='test-experiment')
        result = obsevable.get()
        assert len(result) > 0

        captured = capsys.readouterr()
        assert 'running' in captured.out

    def test_get_history(self, capsys):
        obsevable = experiment_observable.Experiment(client=self.grid.client,
                                                     identifier='test-run')
        obsevable.get_history()

        captured = capsys.readouterr()
        assert 'failed' in captured.out

    def test_follow(self, capsys):
        obsevable = experiment_observable.Experiment(client=self.grid.client,
                                                     identifier='test-run')
        obsevable.follow()

        captured = capsys.readouterr()
        assert 'Following Run details' in captured.out

    def test_follow_handles_exceptions(self, capsys, monkeypatch):
        def mp_websocket_closed(*args, **kwargs):
            raise websockets.exceptions.ConnectionClosedError(code=1,
                                                              reason='test')

        monkeypatch.setattr(self.grid.client, 'subscribe', mp_websocket_closed)
        obsevable = experiment_observable.Experiment(client=self.grid.client,
                                                     identifier='test-run')
        with pytest.raises(click.ClickException):
            obsevable.follow()

        # def mp_websocket_connection_closed_ok(*args, **kwargs):
        #     raise websockets.exceptions.ConnectionClosedOK(code=1, reason='test')

        # monkeypatch.setattr(self.grid.client, 'subscribe', mp_websocket_connection_closed_ok)
        # obsevable = observables.Experiment(client=self.grid.client,
        #                                 identifier='test-run')
        # with pytest.raises(click.ClickException):
        #     obsevable.follow()

        # def mp_execute(*args, **kwargs):
        #     raise Exception("Server error: {'message':'not found'}")

        # monkeypatch.setattr(self.grid.client, 'subscribe', mp_execute)
        # obsevable = observables.Experiment(client=self.grid.client,
        #                                 identifier='test-run')
        # with pytest.raises(click.ClickException):
        #     obsevable.follow()

    def test_render_no_expriment(self):
        obsevable = experiment_observable.Experiment(client=self.grid.client,
                                                     identifier='test-run')
        table = obsevable.render_experiments([])
        assert table.row_count == 0
        assert [x.header for x in table.columns
                ] == ["Experiment", "Command", "Status", "Duration"]

    def test_render_no_hparam_expriment(self):
        obsevable = experiment_observable.Experiment(client=self.grid.client,
                                                     identifier='test-run')
        table = obsevable.render_experiments([{
            'experimentId':
            'gentle-grasshopper-960-exp0',
            'status':
            'succeeded',
            'invocationCommands':
            'python pl_mnist.py',
            'createdAt':
            '2020-11-16T21:01:29.813309+00:00',
            'finishedAt':
            '2020-11-16T21:44:05+00:00',
            'commitSha':
            'e2f16c5c14d52c332568718bfef9f632e3191825',
            'run': {
                'runId': '34dfb18f-d64b-4a67-ac68-773022a81996'
            },
            'startedRunningAt':
            '2020-11-16T21:18:45+00:00'
        }])
        assert table.row_count == 1
        assert [x.header for x in table.columns
                ] == ["Experiment", "Command", "Status", "Duration"]
        assert [x._cells[0] for x in table.columns] == [
            "gentle-grasshopper-960-exp0",
            'pl_mnist.py',
            'succeeded',
            '0d-00:25:20',
        ]

    def test_render_hparam_expriment(self):
        obsevable = experiment_observable.Experiment(client=self.grid.client,
                                                     identifier='test-run')
        table = obsevable.render_experiments([{
            'experimentId':
            'gentle-grasshopper-960-exp0',
            'status':
            'succeeded',
            'invocationCommands':
            'python pl_mnist.py --lr 0.5',
            'createdAt':
            '2020-11-16T21:01:29.813309+00:00',
            'finishedAt':
            '2020-11-16T21:44:05+00:00',
            'commitSha':
            'e2f16c5c14d52c332568718bfef9f632e3191825',
            'run': {
                'runId': '34dfb18f-d64b-4a67-ac68-773022a81996'
            },
            'startedRunningAt':
            '2020-11-16T21:18:45+00:00'
        }])
        assert table.row_count == 1
        assert [x.header for x in table.columns
                ] == ["Experiment", "Command", "Status", "Duration", "lr"]
        assert [x._cells[0] for x in table.columns] == [
            "gentle-grasshopper-960-exp0",
            'pl_mnist.py',
            'succeeded',
            '0d-00:25:20',
            '0.5',
        ]
