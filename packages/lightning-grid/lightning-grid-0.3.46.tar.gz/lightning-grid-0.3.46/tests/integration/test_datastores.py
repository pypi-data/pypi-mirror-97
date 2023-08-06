import uuid

from click.testing import CliRunner
from click.testing import Result
from tests.mock_backend import resolvers
from tests.utilities import create_test_credentials
from tests.utilities import monkey_patch_client

from grid import cli
import grid.client as grid
import grid.commands.credentials as credentials
import grid.datastore as datastore
import grid.uploader as uploader

RUNNER = CliRunner()


class TestDatastores:
    @classmethod
    def setup_class(cls):
        grid.Grid._init_client = monkey_patch_client
        grid.gql = lambda x: x
        datastore.gql = lambda x: x
        credentials.gql = lambda x: x
        cls.name = str(uuid.uuid4())[:8]

        create_test_credentials()

    @staticmethod
    def assert_exit(result: Result, exit_code: int = 0):
        assert result.exit_code == exit_code, \
         f"exit code is not zero, output: {result.output}"

    def test_create_without_grid_credential_works(self, monkeypatch):
        """grid datastores create without passing credentials works"""
        def mp_get_credentials(*args, **kwargs):
            return [{
                'credentialId': 'test-cred-0',
                'provider': 'aws',
                'alias': 'my credential name',
                'createdAt': resolvers.now,
                'lastUsedAt': resolvers.now,
                'defaultCredential': True
            }]

        def mp_upload(*args, **kwargs):
            return {'key': 'value'}

        monkeypatch.setattr(uploader.S3Uploader, 'upload', mp_upload)
        monkeypatch.setattr(resolvers, 'get_user_credentials',
                            mp_get_credentials)
        result = RUNNER.invoke(
            cli.datastores,
            ['create', '--source', 'tests/data', '--name', self.name])
        self.assert_exit(result)
        assert not result.exception
        assert 'Finished uploading datastore' in result.output

        result = RUNNER.invoke(
            cli.datastores,
            ['create', '--source', 'tests/data', '--name', self.name])
        self.assert_exit(result)
        assert not result.exception
        assert 'Finished uploading datastore' in result.output

    def test_list_prints_table_of_datastores(self):
        """grid datastores list prints table of datstores"""
        result = RUNNER.invoke(cli.datastores, ['list'])
        assert result.exit_code == 0
        assert not result.exception
        assert 'Credential Id' in result.output
        assert 'Name' in result.output
        assert 'Version' in result.output
        assert 'Size' in result.output
        assert 'Created' in result.output
        assert 'Status' in result.output
        assert 'test datastore' in result.output
        assert 'Fail' in result.output

    def test_deletes_a_datastore(self):
        """grid datastores delete deletes a datastore"""
        result = RUNNER.invoke(cli.datastores, [
            'delete', '--name', self.name, '--version', '1',
            '--grid_credential', 'test-cred-0'
        ])
        self.assert_exit(result)
        assert not result.exception

    def test_deletes_a_datastore_fails(self, monkeypatch):
        """grid datastores delete fails to delete a datastore"""
        def delete_datastore(*args, **kwargs):
            return {"success": False}

        monkeypatch.setattr(resolvers, 'delete_datastore', delete_datastore)
        result = RUNNER.invoke(cli.datastores, [
            'delete', '--name', self.name, '--version', '1',
            '--grid_credential', 'test-cred-0'
        ])
        self.assert_exit(result)
        assert not result.exception
        assert 'Failed to delete datastore' in result.output

    def test_deletes_a_datstore_fails_with_ex(self, monkeypatch):
        """grid datastores delete fails to delete a datastore with exception"""
        def delete_datastore(*args, **kwargs):
            raise Exception()

        monkeypatch.setattr(resolvers, 'delete_datastore', delete_datastore)
        result = RUNNER.invoke(cli.datastores, [
            'delete', '--name', self.name, '--version', '1',
            '--grid_credential', 'test-cred-0'
        ])
        self.assert_exit(result=result, exit_code=1)
        assert result.exception
        assert 'Failed to delete datastore' in result.output
