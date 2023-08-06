import click
import pytest
import tests.resolvers as resolvers
from tests.utilities import create_test_credentials
from tests.utilities import monkey_patch_client

import grid.client as grid
import grid.observables.base as base_observables


def mp_execute(*args, **kwargs):
    raise Exception("{'message':'not found'}")


def test_style_status():
    value = 'test'
    result = base_observables.style_status(format_string=value,
                                           status='running')
    assert '\x1b[33m' in result
    assert value in result

    result = base_observables.style_status(format_string=value,
                                           status='failed')
    assert '\x1b[31m' in result
    assert value in result

    result = base_observables.style_status(format_string=value,
                                           status='finished')
    assert '\x1b[32m' in result
    assert value in result

    result = base_observables.style_status(format_string=value,
                                           status='cancelled')
    assert '\x1b[37m' in result
    assert value in result


class TestBaseObservable:
    @classmethod
    def setup_class(cls):
        create_test_credentials()

        grid.Grid._init_client = monkey_patch_client

        base_observables.gql = lambda x: x

        cls.grid = grid.Grid(load_local_credentials=False)
        cls.grid._init_client()

        cls.observable = base_observables.BaseObservable(
            client=cls.grid.client)

    def test_get_task_run_dependencies(self):
        results = self.observable._get_task_run_dependencies(run_name='test')
        assert len(results) > 0

    def test_get_task_run_dependencies_raise_exception(self, monkeypatch):
        monkeypatch.setattr(self.grid.client, 'execute', mp_execute)
        observable = base_observables.BaseObservable(client=self.grid.client)
        with pytest.raises(click.ClickException):
            observable._get_task_run_dependencies(run_name='test-run')

    def test_get_task_run_status(self, capsys):
        base_observables.env.SHOW_PROCESS_STATUS_DETAILS = False
        base_observables.env.DEBUG = True
        self.observable._get_task_run_status(run_name='test')

        captured = capsys.readouterr()
        assert 'grid status' in captured.out

        base_observables.env.SHOW_PROCESS_STATUS_DETAILS = True
        base_observables.env.DEBUG = True
        self.observable._get_task_run_status(run_name='test')

        captured = capsys.readouterr()
        assert 'Failed error details' in captured.out

    def test_get_task_run_status_with_non_user_facing_tasks(self, monkeypatch):
        base_observables.env.SHOW_PROCESS_STATUS_DETAILS = False
        base_observables.env.DEBUG = True

        def mp_get_run_task_status(*args, **kwargs):
            return {
                'success':
                True,
                'runId':
                'test',
                'name':
                '',
                'status':
                'failed',
                'message':
                '',
                'dependencies': [{
                    'taskId': 'test-task-0',
                    'status': 'failed',
                    'taskType':
                    'grid.core.repository_builder.RepositoryBuilder',
                    'message': 'Failed message',
                    'error': 'Failed error details'
                }, {
                    'taskId': 'test-task-1',
                    'status': 'running',
                    'taskType': 'grid.core.user.ReconcileUser',
                    'message': '',
                    'error': ''
                }, {
                    'taskId': 'test-task-2',
                    'status': 'running',
                    'taskType':
                    'grid.core.clusters.global_user_cluster.ReconcileCluster',
                    'message': '',
                    'error': ''
                }]
            }

        monkeypatch.setattr(resolvers, 'get_run_task_status',
                            mp_get_run_task_status)
        self.observable._get_task_run_status(run_name='test')
