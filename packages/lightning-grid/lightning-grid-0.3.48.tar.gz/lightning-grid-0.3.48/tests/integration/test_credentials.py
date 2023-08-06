from click.testing import CliRunner
from tests.mock_backend import resolvers
from tests.utilities import create_test_credentials
from tests.utilities import monkey_patch_client

from grid import cli
import grid.client as grid
import grid.commands.credentials as credentials

RUNNER = CliRunner()


class TestCredentials:
    @classmethod
    def setup_class(cls):
        grid.Grid._init_client = monkey_patch_client
        credentials.gql = lambda x: x

        create_test_credentials()

    def test_credentials_without_arguments_prints_table(self, monkeypatch):
        """grid credentials without arguments fails"""
        def mp_get_credentials(*args, **kwargs):
            return [{
                'credentialId': 'test-cred-0',
                'provider': 'aws',
                'alias': 'my credential name',
                'createdAt': resolvers.now,
                'lastUsedAt': resolvers.now,
                'defaultCredential': True
            }]

        monkeypatch.setattr(resolvers, 'get_user_credentials',
                            mp_get_credentials)
        result = RUNNER.invoke(cli.credentials, [])
        assert result.exit_code == 0
        assert not result.exception
        assert 'test-cred-0' in result.output

    def test_sets_default_credential(self):
        """grid credentials --set_default CREDENTIAL_ID sets default credential"""
        credential_id = 'test-cred'
        result = RUNNER.invoke(cli.credentials,
                               ['--set_default', credential_id])
        assert result.exit_code == 0
        assert not result.exception
        assert credential_id in result.output

    def test_add_credentials(self):
        """grid credentials add adds new credentials"""
        file_path = 'tests/data/aws.json'
        result = RUNNER.invoke(
            cli.credentials, ['add', '--provider', 'aws', '--file', file_path])
        assert result.exit_code == 0
        assert not result.exception
        assert 'created' in result.output

    def test_add_credentials_with_bad_provider_fails(self):
        """grid credentials with bad provider fails"""
        file_path = 'tests/data/aws.json'
        result = RUNNER.invoke(
            cli.credentials,
            ['add', '--provider', 'test-fails', '--file', file_path])
        assert result.exit_code == 2
        assert result.exception
