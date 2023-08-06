from array import array
import base64
import csv
import glob
import json
import os
from pathlib import Path
from unittest.mock import MagicMock
from urllib.parse import urljoin
import zlib

import click
from click.exceptions import ClickException
from gql import Client
import httpretty
import pytest
import requests
from tests.mock_backend import GridAIBackenedTestServer
from tests.mock_backend import resolvers
import yaspin

import grid.client as grid
from grid.datastore import DatastoreUploadSession
from grid.exceptions import AuthenticationError
from grid.exceptions import TrainError
import grid.globals as env
from grid.metadata import __version__
from grid.types import ObservableType
from grid.types import WorkflowType

#  Prevents Click from opening the browser.
click.launch = lambda x: True


def monkey_patch_observables():
    """Monkey patches the observables factory."""
    class MonkeyPatchedObservable:
        key = 'getRuns'

        def __init__(self, *args, **kwargs):  # skipcq: PTC-W0049
            pass

        def get(self, *args, **kwarrgs):
            return {
                self.key: [{
                    'columnn': 'value'
                }, {
                    'column_fail_a': []
                }, {
                    'column_fail_b': {}
                }]
            }

    return {
        ObservableType.EXPERIMENT: MonkeyPatchedObservable,
        ObservableType.RUN: MonkeyPatchedObservable,
        ObservableType.CLUSTER: MonkeyPatchedObservable,
    }


#  Test authentication errors
def monkey_patch_execute(*args, **kwargs):
    raise requests.exceptions.HTTPError('error')


class MonkeyPatchClient:
    def execute(self, *args, **kwargs):
        raise Exception("{'message': 'test exception'}")


class TestGridClient:
    """Unit tests for the Grid class."""
    @classmethod
    def setup_class(cls):
        #  Monkey patches the GraphQL client to read from a local schema.
        def monkey_patch_client(self):
            self.client = GridAIBackenedTestServer()

        #  Monkey-patches the gql method so that it passes
        #  forward a GraphQL query string directly.
        grid.gql = lambda x: x

        #  skipcq: PYL-W0212
        grid.Grid._init_client = monkey_patch_client

        cls.creds_path = 'tests/data/credentials.json'
        cls.creds_path_incorrect = 'tests/data/test-credentials.json'
        cls.grid_header_keys = ['X-Grid-User', 'X-Grid-Key']

        cls.train_kwargs = {
            'config': 'test-config',
            'kind': WorkflowType.SCRIPT,
            'run_name': 'test-run',
            'run_description': 'test description',
            'entrypoint': 'test_file.py',
            'script_args': ['--learning_rate', '0.001']
        }

    def remove_env(self):
        #  Makes sure that the Grid env vars are not set
        envs_to_remove = [
            'GRID_CREDENTIAL_PATH', 'GRID_USER_ID', 'GRID_API_KEY'
        ]
        for env in envs_to_remove:
            if os.getenv(env):
                del os.environ[env]

    def remove_status_files(self):
        # path = 'test/data/'
        for e in ['csv', 'json']:
            for f in glob.glob(f'*.{e}'):
                os.remove(f)

    def remove_credentials_file(self):
        p = Path(self.creds_path_incorrect)
        if p.exists():
            p.unlink(missing_ok=True)

    def setUp(self):
        self.remove_env()
        self.remove_status_files()
        self.remove_credentials_file()

    def teardown(self):
        self.remove_env()

        #  Removes test credentials added to home path.
        P = Path.home().joinpath(self.creds_path)
        if P.exists():
            P.unlink(missing_ok=True)

        self.remove_status_files()
        self.remove_credentials_file()

    def test_client_local_path(self):
        """Client with local credentials path initializes correctly"""

        G = grid.Grid(credential_path=self.creds_path,
                      load_local_credentials=False)
        for key in self.grid_header_keys:
            assert key in G.headers.keys()

    def test_client_loads_credentials_from_env_var(self):
        """Client loads credentials path from env var"""
        os.environ['GRID_CREDENTIAL_PATH'] = self.creds_path
        G = grid.Grid()
        for key in self.grid_header_keys:
            assert key in G.headers.keys()

        os.environ['GRID_CREDENTIAL_PATH'] = 'fake-path'
        with pytest.raises(click.ClickException):
            grid.Grid()

        self.remove_env()

    def test_client_raises_exception_if_creds_path_not_found(self):
        """Client raises exception if credentials path not found"""
        credentials_path = 'tests/data/foo.json'
        with pytest.raises(click.ClickException):
            grid.Grid(credential_path=credentials_path)

    def test_nested_path_is_parsed_correctly(self):
        """Tests that we can add the Git root path to a script"""
        result = grid.Grid._add_git_root_path(entrypoint='foo.py')
        path_elems = result.split(os.path.sep)

        actual = path_elems[-2:]
        expected = ['grid-cli', 'foo.py']
        assert len(actual) == len(expected)
        assert all(a == b for a, b in zip(actual, expected))

    def test_client_loads_credentials_from_default_path(self):
        """Client loads credentials from default path"""
        test_path = 'tests/data/credentials.json'
        with open(test_path) as f:
            credentials = json.load(f)

        #  Let's create a credentials file in the home
        #  directory.
        creds_name = 'test_credentials.json'
        P = Path.home().joinpath(creds_name)
        with P.open('w') as f:
            json.dump(credentials, f)

        grid.Grid.grid_credentials_path = creds_name
        G = grid.Grid()

        assert G.credentials.get('UserID') == credentials['UserID']

    def test_client_raises_error_if_no_creds_available(self):
        """Client loads credentials from default path"""
        with pytest.raises(click.ClickException):
            grid.Grid(credential_path=self.creds_path_incorrect)

        # TODO: test not working
        # with pytest.raises(click.ClickException):
        #     # monkeypatch.setattr(grid.Grid, 'grid_credentials_path', self.creds_path_incorrect):
        #     grid.Grid.grid_credentials_path = self.creds_path_incorrect
        #     G = grid.Grid(load_local_credentials=False)
        #     G._set_local_credentials()

    #  NOTE: there's a race condition here with the env
    #  var. Let's leave this named this way.
    def test_a_client_local_init(self):
        """Client init without local credentials leaves headers unchanged"""

        assert not os.getenv('GRID_CREDENTIAL_PATH')

        G = grid.Grid(load_local_credentials=False)
        for key in self.grid_header_keys:
            assert key not in G.headers.keys()

    def test_train(self, monkeypatch):
        """grid.Grid().train() executes a training operation correctly."""
        G = grid.Grid(credential_path=self.creds_path,
                      load_local_credentials=False)
        env.IGNORE_WARNINGS = True
        G.train(**self.train_kwargs)

        # We want to ignore global settings to test debugging.
        monkeypatch.setattr(grid.Grid, '_load_global_settings', lambda: True)
        env.DEBUG = True
        G.train(**self.train_kwargs)

    def test_train_raises_exception_blueprint(self):
        """
        grid.Grid().train() raises exception when attempting to
        train a blueprint.
        """
        G = grid.Grid(credential_path=self.creds_path,
                      load_local_credentials=False)
        env.IGNORE_WARNINGS = True
        with pytest.raises(TrainError):
            G.train(**{**self.train_kwargs, 'kind': WorkflowType.BLUEPRINT})

    def test_train_raises_exception_if_query_fails(self):
        G = grid.Grid(credential_path=self.creds_path,
                      load_local_credentials=False)
        G.client = MonkeyPatchClient()
        G._check_user_github_token = lambda: True
        env.IGNORE_WARNINGS = True

        with pytest.raises(click.ClickException):
            G.train(**self.train_kwargs)

    def test_status_returns_results(self):
        """grid.Grid().status() returns a dict results."""
        G = grid.Grid(credential_path=self.creds_path,
                      load_local_credentials=False)

        G.available_observables = monkey_patch_observables()
        results = G.status()
        assert isinstance(results, dict)

    def test_status_generates_output_files(self):
        """grid.Grid().status() generates output files."""
        G = grid.Grid(credential_path=self.creds_path,
                      load_local_credentials=False)

        G.available_observables = monkey_patch_observables()

        #  Tests exporting.
        extensions = ['csv', 'json']
        for e in extensions:
            G.status(export=e)
            files = [*glob.glob(f'*.{e}')]
            assert len(files) == 1

            #  Test that lists or dict columns are not exported to CSV.
            if e == 'csv':
                with open(files[0], 'r') as f:
                    data = [*csv.DictReader(f)]
                    assert 'column_fail_a' not in data[0].keys()
                    assert 'column_fail_b' not in data[0].keys()

    def test_download_experiment_artifacts(self):
        """grid.Grid().download_experiment_artifacts() does not fail"""
        experiment_id = 'test-experiment-exp0'
        G = grid.Grid(credential_path=self.creds_path,
                      load_local_credentials=False)
        G.download_experiment_artifacts(experiment_id=experiment_id,
                                        download_dir='tests/data')

    @staticmethod
    def test_download_experiment_artifacts_handles_exception(monkeypatch):
        """
        grid.Grid().download_experiment_artifacts() handles exception for when
        the GraphQL query returns an error.
        """
        experiment_id = 'test-experiment-exp0'
        G = grid.Grid(load_local_credentials=False)
        G._init_client()

        monkey_patch_get_artifacts = lambda: {'errors': 'error'}
        monkeypatch.setattr(resolvers, 'get_artifacts',
                            monkey_patch_get_artifacts)
        with pytest.raises(click.ClickException):
            G.download_experiment_artifacts(experiment_id=experiment_id,
                                            download_dir='tests/data')

    def test_user_id(self):
        """Returns same User ID as specified in credentials file."""
        test_path = 'tests/data/credentials.json'
        with open(test_path) as f:
            credentials = json.load(f)

        G = grid.Grid(credential_path=self.creds_path,
                      load_local_credentials=False)

        assert G.credentials.get('UserID') == credentials['UserID']
        assert G.user_id == credentials['UserID']

    def test_setting_local_credentials_using_env_vars(self):
        """grid.Grid() sets credentials using environment variables."""
        test_user_id = 'test-user-id'
        test_api_key = 'test-api_key'

        os.environ['GRID_USER_ID'] = test_user_id
        os.environ['GRID_API_KEY'] = test_api_key
        G = grid.Grid(load_local_credentials=True)

        assert G.headers['X-Grid-User'] == test_user_id
        assert G.headers['X-Grid-Key'] == test_api_key

        self.remove_env()

    @staticmethod
    def test_check_user_github_token():
        """
        grid.Grid()._check_user_github_token() checks if user's GH
        token is valid.
        """
        G = grid.Grid(load_local_credentials=False)
        G._init_client()

        result = G._check_user_github_token()
        assert result == True

    @staticmethod
    def test_check_user_github_token_raises_exception(monkeypatch):
        """
        grid.Grid()._check_user_github_token() raises exception if no
        Github token is available.
        """
        G = grid.Grid(load_local_credentials=False)
        G._init_client()

        #  Test when users don't have a valid token
        def monkey_patch_token(*args, **kwargs):
            return {'hasValidToken': False}

        with pytest.raises(click.exceptions.ClickException):
            monkeypatch.setattr(resolvers, 'check_user_github_token',
                                monkey_patch_token)
            G._check_user_github_token()

        with pytest.raises(AuthenticationError):
            monkeypatch.setattr(GridAIBackenedTestServer, 'execute',
                                monkey_patch_execute)
            # Prevents browser from opening
            monkeypatch.setattr(click, 'launch', lambda x: True)
            G._check_user_github_token()

    @staticmethod
    def test_add_git_root_path():
        """Grid._add_git_root_path() adds the git root path to script."""
        G = grid.Grid(load_local_credentials=False)
        result = G._add_git_root_path(entrypoint='test.py')

        assert result == '/grid-cli/test.py'

    @staticmethod
    def test_login():
        """Grid.login() correctly sends login query."""
        G = grid.Grid(load_local_credentials=False)

        G.login(username='test-user', key='test-key')

    @staticmethod
    def test_login_handles_error(monkeypatch):
        """Grid.login() handles HTTPError exception."""
        G = grid.Grid(load_local_credentials=False)

        with pytest.raises(ClickException):
            monkeypatch.setattr(GridAIBackenedTestServer, 'execute',
                                monkey_patch_execute)
            G.login(username='test-user', key='test-key')

    @staticmethod
    def test_delete_cluster(monkeypatch):
        """Grid().delete_cluster() deletes a cluster."""
        G = grid.Grid(load_local_credentials=False)
        G._init_client()

        assert G.delete_cluster(cluster_id='test-cluster')

        def monkey_patch_delete_cluster(*args, **kwargs):
            return {'success': False, 'message': ''}

        monkeypatch.setattr(resolvers, 'delete_cluster',
                            monkey_patch_delete_cluster)
        assert not G.delete_cluster(cluster_id='test-cluster')

    @staticmethod
    def test_delete_cluster_handles_api_error(monkeypatch):
        """Grid().delete_cluster() handles API error."""
        monkey_patch_delete_cluster = lambda: {}

        G = grid.Grid(load_local_credentials=False)
        G._init_client()
        monkeypatch.setattr(resolvers, 'delete_cluster',
                            monkey_patch_delete_cluster)
        with pytest.raises(click.ClickException):
            G.delete_cluster(cluster_id='test-cluster')

    @staticmethod
    def test_upload_datstore_handles_error():
        G = grid.Grid(load_local_credentials=False)
        G.client = MonkeyPatchClient()

        with pytest.raises(click.ClickException):
            G.upload_datastore(source='./tests/data/datastore_test/',
                               name='datastore-test',
                               credential_id='test-credential',
                               compression=True)

    @staticmethod
    def test_resuming_upload_datastore():
        G = grid.Grid(load_local_credentials=False)
        G.client = MonkeyPatchClient()

        session = DatastoreUploadSession(name="test_session",
                                         version=1,
                                         source_dir="data",
                                         credential_id="cc-abcdef")
        upload = MagicMock()
        session.upload = upload

        DatastoreUploadSession.recover_sessions = MagicMock(
            return_value=[session])
        G.resume_datastore_session("test_session-v1")
        upload.assert_called_once()

    @staticmethod
    def test_experiment_details():
        G = grid.Grid(load_local_credentials=False)
        G._init_client()

        result = G.experiment_details(experiment_id='test-experiment-id')
        assert result['getExperimentDetails']['status'] == 'succeeded'

    @staticmethod
    def test_create_interactive_node(monkeypatch):
        G = grid.Grid(load_local_credentials=False)
        G._init_client()

        result = G.create_interactive_node(name='test-interactive-id',
                                           config='',
                                           description="test-description")
        assert result

        def monkey_path_create(*args, **kwargs):
            return {'success': False, 'message': ''}

        monkeypatch.setattr(resolvers, 'create_interactive_node',
                            monkey_path_create)
        env.DEBUG = True
        with pytest.raises(click.ClickException):
            G.create_interactive_node(name='test-interactive-id',
                                      config='',
                                      description='test-description')

    @staticmethod
    def test_create_interactive_node_handles_error():
        G = grid.Grid(load_local_credentials=False)
        G.client = MonkeyPatchClient()
        G._check_user_github_token = lambda: True

        with pytest.raises(click.ClickException):
            G.create_interactive_node(name='test-interactive-id',
                                      config='',
                                      description="test-desc")

    @staticmethod
    def test_pause_interactive_node(monkeypatch):
        G = grid.Grid(load_local_credentials=False)
        G._init_client()

        result = G.pause_interactive_node(
            interactive_node_name='test-interactive-id')
        assert result

        def monkey_path_pause(*args, **kwargs):
            return {'success': False, 'message': ''}

        monkeypatch.setattr(resolvers, 'pause_interactive_node',
                            monkey_path_pause)
        env.DEBUG = True
        with pytest.raises(click.ClickException):
            G.pause_interactive_node(
                interactive_node_name='test-interactive-id')

    @staticmethod
    def test_pause_interactive_node_handles_error():
        G = grid.Grid(load_local_credentials=False)
        G.client = MonkeyPatchClient()
        G._check_user_github_token = lambda: True

        with pytest.raises(click.ClickException):
            G.pause_interactive_node(
                interactive_node_name='test-interactive-id')

    @staticmethod
    def test_resume_interactive_node(monkeypatch):
        G = grid.Grid(load_local_credentials=False)
        G._init_client()

        result = G.resume_interactive_node(
            interactive_node_name='test-interactive-id')
        assert result

        def monkey_path_pause(*args, **kwargs):
            return {'success': False, 'message': ''}

        monkeypatch.setattr(resolvers, 'resume_interactive_node',
                            monkey_path_pause)
        env.DEBUG = True
        with pytest.raises(click.ClickException):
            G.resume_interactive_node(
                interactive_node_name='test-interactive-id')

    @staticmethod
    def test_resume_interactive_node_handles_error():
        G = grid.Grid(load_local_credentials=False)
        G.client = MonkeyPatchClient()
        G._check_user_github_token = lambda: True

        with pytest.raises(click.ClickException):
            G.resume_interactive_node(
                interactive_node_name='test-interactive-id')

    @staticmethod
    def test_delete_interactive_node(monkeypatch):
        G = grid.Grid(load_local_credentials=False)
        G._init_client()

        result = G.delete_interactive_node(
            interactive_node_name='test-interactive-id')
        assert result

        def monkey_path_delete(*args, **kwargs):
            return {'success': False, 'message': ''}

        monkeypatch.setattr(resolvers, 'delete_interactive_node',
                            monkey_path_delete)
        env.DEBUG = True
        with pytest.raises(click.ClickException):
            G.delete_interactive_node(
                interactive_node_name='test-interactive-id')

    @staticmethod
    def test_delete_interactive_node_handles_error():
        G = grid.Grid(load_local_credentials=False)
        G.client = MonkeyPatchClient()
        G._check_user_github_token = lambda: True

        with pytest.raises(click.ClickException):
            G.delete_interactive_node(
                interactive_node_name='test-interactive-id')

    @staticmethod
    def test_delete():
        G = grid.Grid(load_local_credentials=False)
        G._init_client()

        result = G.delete(experiment_id='test-experiment-id')
        assert result

        result = G.delete(run_id='test-run-id')
        assert result

    @staticmethod
    def test_delete_handles_errors(monkeypatch):
        G = grid.Grid(load_local_credentials=False)
        G._init_client()
        G._check_user_github_token = lambda: True

        def mp_delete_object(**kwargs):
            return {'success': False, 'message': None}

        monkeypatch.setattr(resolvers, 'delete_experiment', mp_delete_object)
        with pytest.raises(click.ClickException):
            G.delete(experiment_id='test-experiment-id')

        G.client = MonkeyPatchClient()
        with pytest.raises(click.ClickException):
            G.delete(experiment_id='test-experiment-id')

        monkeypatch.setattr(resolvers, 'delete_run', mp_delete_object)
        with pytest.raises(click.ClickException):
            G.delete(experiment_id='test-run-id')

        G.client = MonkeyPatchClient()
        with pytest.raises(click.ClickException):
            G.delete(run_id='test-run-id')

    @staticmethod
    def test_cancel():
        G = grid.Grid(load_local_credentials=False)
        G._init_client()

        result = G.cancel(run_name='test-run-id')
        assert result is True

        result = G.cancel(experiment_id='test-experiment-id')
        assert result is True

    @staticmethod
    def test_cancel_handles_errors(monkeypatch):
        G = grid.Grid(load_local_credentials=False)
        G.client = MonkeyPatchClient()
        G._check_user_github_token = lambda: True

        def monkey_patch_experiment_details(**kwargs):
            return 'failed'

        monkeypatch.setattr(G, 'experiment_details',
                            monkey_patch_experiment_details)
        with pytest.raises(click.ClickException):
            G.cancel(run_name='test-run-id')

    @staticmethod
    def test_cancel_experiments(monkeypatch):
        G = grid.Grid(load_local_credentials=False)
        G._init_client()

        spinner = yaspin.yaspin()

        def mp_cancel_experiments(*args, **kwargs):
            return {'success': False, 'message': ''}

        monkeypatch.setattr(resolvers, 'cancel_experiment',
                            mp_cancel_experiments)
        experiments = [{'experimentId': 'test0', 'status': False}]
        with pytest.raises(click.ClickException):
            G._cancel_experiments(experiments=experiments, spinner=spinner)

    def test_history(self):
        G = grid.Grid(credential_path=self.creds_path,
                      load_local_credentials=False)
        gql = MagicMock(Client, autospec=True)
        G.client = gql

        observable = MagicMock()
        observable_fact = MagicMock(return_value=observable)
        G.available_observables[ObservableType.EXPERIMENT] = observable_fact
        observable.get_history = MagicMock(return_value={"a": "b"})
        assert G.history(
            kind=ObservableType.EXPERIMENT,
            identifiers=["foo"],
        ) == {
            "a": "b"
        }
        observable_fact.assert_called_once()
        observable_fact.assert_called_once_with(client=G.client,
                                                identifier="foo")
        observable.get_history.assert_called_once()

        observable = MagicMock()
        observable_fact = MagicMock(return_value=observable)
        G.available_observables[ObservableType.RUN] = observable_fact
        observable.get_history = MagicMock(return_value={"a": "b"})
        assert G.history(kind=ObservableType.RUN, ) == {"a": "b"}
        observable_fact.assert_called_once()
        observable_fact.assert_called_once_with(client=G.client)
        observable.get_history.assert_called_once()

        observable = MagicMock()
        observable_fact = MagicMock(return_value=observable)
        G.available_observables[ObservableType.RUN] = observable_fact
        observable.get_history = MagicMock(return_value={"a": "b"})
        assert G.history() == {"a": "b"}
        observable_fact.assert_called_once()
        observable_fact.assert_called_once_with(client=G.client)
        observable.get_history.assert_called_once()

        with pytest.raises(click.BadArgumentUsage):
            G.history(kind=ObservableType.INTERACTIVE)

        with pytest.raises(click.BadArgumentUsage):
            G.history(kind=ObservableType.CLUSTER)

    def test_status(self):
        G = grid.Grid(credential_path=self.creds_path,
                      load_local_credentials=False)
        gql = MagicMock(Client, autospec=True)
        G.client = gql

        observable = MagicMock()
        observable_fact = MagicMock(return_value=observable)
        G.available_observables[ObservableType.EXPERIMENT] = observable_fact
        observable.get = MagicMock(return_value={"a": "b"})
        assert G.status(
            kind=ObservableType.EXPERIMENT,
            identifiers=["foo"],
        ) == {
            "a": "b"
        }
        observable_fact.assert_called_once()
        observable_fact.assert_called_once_with(client=G.client,
                                                identifier="foo")
        observable.get.assert_called_once()

        observable = MagicMock()
        observable_fact = MagicMock(return_value=observable)
        G.available_observables[ObservableType.RUN] = observable_fact
        observable.get = MagicMock(return_value={"a": "b"})
        assert G.status(kind=ObservableType.RUN, ) == {"a": "b"}
        observable_fact.assert_called_once()
        observable_fact.assert_called_once_with(client=G.client)
        observable.get.assert_called_once()

        observable = MagicMock()
        observable_fact = MagicMock(return_value=observable)
        G.available_observables[ObservableType.RUN] = observable_fact
        observable.get = MagicMock(return_value={"a": "b"})
        assert G.status() == {"a": "b"}
        observable_fact.assert_called_once()
        observable_fact.assert_called_once_with(client=G.client)
        observable.get.assert_called_once()

        observable = MagicMock()
        observable_fact = MagicMock(return_value=observable)
        G.available_observables[ObservableType.INTERACTIVE] = observable_fact
        observable.get = MagicMock(return_value={"a": "b"})
        assert G.status(kind=ObservableType.INTERACTIVE) == {"a": "b"}
        observable_fact.assert_called_once()
        observable_fact.assert_called_once_with(client=G.client)
        observable.get.assert_called_once()

        with pytest.raises(click.BadArgumentUsage):
            G.status(kind=ObservableType.CLUSTER)

    def test_experiment_logs_queued(self):
        G = grid.Grid(credential_path=self.creds_path,
                      load_local_credentials=False)

        G.client = MagicMock()
        G.experiment_details = MagicMock(return_value={
            'getExperimentDetails': {
                'status': 'queued',
                'experimentId': 'test'
            }
        })
        G.experiment_logs('test')
        G.client.execute.assert_not_called()

    def test_experiment_logs_succeeded(self):
        G = grid.Grid(credential_path=self.creds_path,
                      load_local_credentials=False)

        G.client = MagicMock(Client, autospec=True)
        G.experiment_details = MagicMock(
            return_value={'getExperimentDetails': {
                'status': 'succeeded'
            }})
        G.client.execute = MagicMock(
            return_value={
                'getArchiveExperimentLogs': {
                    'totalPages':
                    2,
                    'lines': [{
                        "message": "foo",
                        "timestamp": "date1"
                    }, {
                        "message": "bar",
                        "timestamp": "date2"
                    }]
                }
            })
        G.experiment_logs('test')
        G.client.execute.assert_called_once()

    def test_experiment_logs_running(self):
        G = grid.Grid(credential_path=self.creds_path,
                      load_local_credentials=False)

        G.client = MagicMock(Client, autospec=True)
        G._init_client = MagicMock()
        G.experiment_details = MagicMock(return_value={
            'getExperimentDetails': {
                'status': 'running',
                'experimentId': 'test'
            }
        })
        G.client.subscribe = MagicMock(return_value=[{
            'getLiveExperimentLogs': [{
                "message": "foo",
                "timestamp": "date1"
            }, {
                "message": "bar",
                "timestamp": "date2"
            }]
        }])

        G.experiment_logs('test')
        G._init_client.assert_called_once()
        G.client.subscribe.assert_called_once()

    def test_experiment_metrics_queued(self):
        G = grid.Grid(credential_path=self.creds_path,
                      load_local_credentials=False)

        G.client = MagicMock()
        G.experiment_details = MagicMock(return_value={
            'getExperimentDetails': {
                'status': 'queued',
                'experimentId': 'test'
            }
        })
        G.experiment_metrics('test', 'train_loss')
        G.client.execute.assert_not_called()

    def test_experiment_metrics_succeeded(self):
        G = grid.Grid(credential_path=self.creds_path,
                      load_local_credentials=False)

        G.client = MagicMock(Client, autospec=True)
        G.experiment_details = MagicMock(
            return_value={'getExperimentDetails': {
                'status': 'succeeded'
            }})

        # TODO: use when format = 'binary'
        # steps = base64.b64encode(zlib.compress(b'00000000'))
        # values = base64.b64encode(zlib.compress(b'00000000'))
        G.client.execute = MagicMock(
            return_value={
                'getExperimentScalarLogs': {
                    'steps': "[0, 1]",
                    'values': "[0.1, 0.2]",
                    'nextIndex': 10
                }
            })
        G.experiment_metrics('test', 'train_loss')
        G.client.execute.assert_called_once()

    @httpretty.activate
    def test_check_version_compatibility(self, capsys, monkeypatch):
        G = grid.Grid(credential_path=self.creds_path,
                      load_local_credentials=False)

        url = env.GRID_URL.replace('graphql', '')
        httpretty.register_uri(httpretty.GET,
                               urljoin(url, 'metadata'),
                               body=json.dumps({'version': __version__}))
        G._check_version_compatibility()

        captured = capsys.readouterr()
        assert 'pip install' not in captured.out

        httpretty.register_uri(httpretty.GET,
                               urljoin(url, 'metadata'),
                               body=json.dumps({'version': 'v100.1.1'}))

        try:
            G._check_version_compatibility()
        except Exception as e:
            captured = capsys.readouterr()
            assert 'pip install' in captured.out

            with pytest.raises(click.ClickException):
                raise e

        # Check that version check skips
        monkeypatch.setattr(env, 'SKIP_VERSION_CHECK', True)
        G._check_version_compatibility()

    @staticmethod
    def test_gen_ssh_config():
        assert grid.Grid._gen_ssh_config([],
                                         "",
                                         start_marker="#START",
                                         end_marker="#END") == '\n'.join([
                                             "#START",
                                             "#END",
                                         ])

        assert grid.Grid._gen_ssh_config([],
                                         "happy little config",
                                         start_marker="#START",
                                         end_marker="#END") == '\n'.join([
                                             "happy little config",
                                             "#START",
                                             "#END",
                                         ])

        with pytest.raises(ValueError):
            grid.Grid._gen_ssh_config([],
                                      '\n'.join(["#START"]),
                                      start_marker="#START",
                                      end_marker="#END")

        with pytest.raises(ValueError):
            grid.Grid._gen_ssh_config([],
                                      '\n'.join(["#END"]),
                                      start_marker="#START",
                                      end_marker="#END")

        with pytest.raises(ValueError):
            grid.Grid._gen_ssh_config([],
                                      '\n'.join([
                                          "#START",
                                          "#END",
                                          "#START",
                                      ]),
                                      start_marker="#START",
                                      end_marker="#END")

        with pytest.raises(ValueError):
            grid.Grid._gen_ssh_config([],
                                      '\n'.join([
                                          "#START",
                                          "#START",
                                          "#END",
                                      ]),
                                      start_marker="#START",
                                      end_marker="#END")

        with pytest.raises(ValueError):
            grid.Grid._gen_ssh_config([],
                                      '\n'.join([
                                          "#END",
                                          "#START",
                                      ]),
                                      start_marker="#START",
                                      end_marker="#END")

        assert grid.Grid._gen_ssh_config(
            [
                {
                    'name': 'ix1',
                    'ssh_url': 'ssh://jovyan@ix1.grid.ai:233',
                },
                {
                    'name': 'ix2',
                    'ssh_url': 'ssh://jovyan@ix2.grid.ai:433',
                },
            ],
            '\n'.join([
                "happy little config",
                "#START",
                "#END",
            ]),
            start_marker="#START",
            end_marker="#END") == '\n'.join([
                "happy little config",
                "#START",
                "Host ix1",
                "    User jovyan",
                "    Hostname ix1.grid.ai",
                "    Port 233",
                "    StrictHostKeyChecking accept-new",
                "Host ix2",
                "    User jovyan",
                "    Hostname ix2.grid.ai",
                "    Port 433",
                "    StrictHostKeyChecking accept-new",
                "#END",
            ])

    @staticmethod
    def test_gen_ssh_config_idempotent():
        assert grid.Grid._gen_ssh_config(
            [
                {
                    'name': 'ix1',
                    'ssh_url': 'ssh://jovyan@ix1.grid.ai:233',
                },
                {
                    'name': 'ix2',
                    'ssh_url': 'ssh://jovyan@ix2.grid.ai:433',
                },
            ],
            '\n'.join([
                "happy little config",
                "#START",
                "Host ix1",
                "    User jovyan",
                "    Hostname ix1.grid.ai",
                "    Port 233",
                "    StrictHostKeyChecking accept-new",
                "Host ix2",
                "    User jovyan",
                "    Hostname ix2.grid.ai",
                "    Port 433",
                "    StrictHostKeyChecking accept-new",
                "#END",
            ]),
            start_marker="#START",
            end_marker="#END") == '\n'.join([
                "happy little config",
                "#START",
                "Host ix1",
                "    User jovyan",
                "    Hostname ix1.grid.ai",
                "    Port 233",
                "    StrictHostKeyChecking accept-new",
                "Host ix2",
                "    User jovyan",
                "    Hostname ix2.grid.ai",
                "    Port 433",
                "    StrictHostKeyChecking accept-new",
                "#END",
            ])
