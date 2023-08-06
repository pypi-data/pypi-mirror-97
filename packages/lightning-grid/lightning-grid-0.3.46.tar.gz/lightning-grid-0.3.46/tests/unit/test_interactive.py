import os
from pathlib import Path

from tests.utilities import create_local_schema_client

from grid.cli.grid_interactive import _generate_default_interactive_config
from grid.client import Grid
from grid.types import WorkflowType


class TestGridInteractive:
    @classmethod
    def setup_class(cls):
        #  Monkey patches the GraphQL client to read from a local schema.
        def monkey_patch_client(self):
            self.client = create_local_schema_client()

        #  skipcq: PYL-W0212
        Grid._init_client = monkey_patch_client

        cls.creds_path = 'tests/data/credentials.json'
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
        #  Makes sure that the GRID_CREDENTIAL_PATH is not set
        if os.getenv('GRID_CREDENTIAL_PATH'):
            del os.environ['GRID_CREDENTIAL_PATH']

    def setup(self):
        self.remove_env()

    def teardown(self):
        self.remove_env()

        #  Removes test credentials added to home path.
        P = Path.home().joinpath(self.creds_path)
        if P.exists():
            P.unlink(missing_ok=True)

    def mock_get_credentials(self):
        return {
            'getUserCredentials': [{
                'credentialId': 'test',
                'provider': 'test',
                'defaultCredential': True
            }]
        }

    def test_grid_interactive_config(self):
        """Grid().train() executes a training operation correctly."""
        grid = Grid(credential_path=self.creds_path,
                    load_local_credentials=False)
        grid.get_credentials = self.mock_get_credentials

        interactive_config = _generate_default_interactive_config(
            credential_id='test', client=grid, instance_type='test')

        assert interactive_config['compute']['provider']['vendor'] == 'test'
        assert interactive_config['compute']['provider'][
            'credentials'] == 'test'
