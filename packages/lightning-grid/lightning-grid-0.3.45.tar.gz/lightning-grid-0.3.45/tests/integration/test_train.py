from click.testing import CliRunner
from tests.mock_backend import GridAIBackenedTestServer

from grid import cli
import grid.client as grid
import grid.globals as env

CREDENTIAL_ID = 'test-credential'
CREDENTIAL_ID_DEFAULT = 'defaultCredential'
RUNNER = CliRunner()

CONTENT = "content"


# Monkey patches the getting of credentials
def monkey_patch_get_credentials(self):
    return {
        'getUserCredentials': [{
            'credentialId': CREDENTIAL_ID,
            'provider': 'aws',
            'defaultCredential': True
        }]
    }


def monkey_patch_get_credentials_multiple(self):
    return {
        'getUserCredentials': [{
            'credentialId': CREDENTIAL_ID,
            'provider': 'aws',
            'defaultCredential': True
        }, {
            'credentialId': "Another",
            'provider': 'aws',
            'defaultCredential': False
        }]
    }


def monkey_patch_get_credentials_multiple_no_default(self):
    return {
        'getUserCredentials': [{
            'credentialId': CREDENTIAL_ID,
            'provider': 'aws',
            'defaultCredential': False,
            'createdAt': '2020-11-11',
            'lastUsedAt': '2020-11-11',
            'alias': None
        }, {
            'credentialId': "Another",
            'provider': 'aws',
            'defaultCredential': False,
            'createdAt': '2020-11-11',
            'lastUsedAt': '2020-11-11',
            'alias': None
        }]
    }


# Monkey patches the check for tokens
def monkey_patch_token_check(self):
    return {'checkUserGithubToken': {'hasValidToken': True}}


#  Monkey patch the client.
def monkey_patch_no_creds(self):
    return {'getUserCredentials': []}


#  Monkey patch the client.
def monkey_patch_wrong_creds(self):
    return {
        'getUserCredentials': [{
            'credentialId': 'wrong-cred',
            'provider': 'aws',
            'defaultCredential': True
        }]
    }


#  Monkey patches the GraphQL client to read from a local schema.
def monkey_patch_client(self):
    self.client = GridAIBackenedTestServer()


def test_train_fails_with_no_arguments(monkeypatch):
    """grid train without arguments fails"""
    monkeypatch.setattr(grid.Grid, '_init_client', monkey_patch_client)

    monkeypatch.setattr(grid.Grid, 'get_credentials',
                        monkey_patch_get_credentials)
    monkeypatch.setattr(grid.Grid, '_check_user_github_token',
                        monkey_patch_token_check)

    result = RUNNER.invoke(cli.train, [])
    assert result.exit_code == 2
    assert result.exception


def test_train_fails_with_no_credentials(monkeypatch):
    """grid train fails if user has no credentials."""
    monkeypatch.setattr(grid.Grid, 'get_credentials', monkey_patch_no_creds)
    monkeypatch.setattr(grid.Grid, '_set_local_credentials', lambda x: True)
    monkeypatch.setattr(grid.Grid, '_check_user_github_token',
                        monkey_patch_token_check)

    result = RUNNER.invoke(cli.train, ['--', 'tests/data/script.py'])

    assert result.exit_code == 1
    assert result.exception


def test_train_fails_if_credentials_dont_exist(monkeypatch):
    """grid train fails if credentials don't exist for user."""
    monkeypatch.setattr(grid.Grid, '_set_local_credentials', lambda x: True)
    monkeypatch.setattr(grid.Grid, '_check_user_github_token',
                        monkey_patch_token_check)

    result = RUNNER.invoke(cli.train, [
        '--grid_credential', 'test-fail', '--grid_cpus', 1, '--',
        'tests/data/script.py'
    ])

    assert result.exit_code == 1
    assert result.exception


def test_train_fails_if_wrong_credential(monkeypatch):
    """grid train fails if wrong credentials for user."""
    monkeypatch.setattr(grid.Grid, '_init_client', monkey_patch_client)

    monkeypatch.setattr(grid.Grid, 'get_credentials', monkey_patch_wrong_creds)

    result = RUNNER.invoke(
        cli.train,
        ['--grid_credential', CREDENTIAL_ID, '--', 'tests/data/script.py'])

    assert result.exit_code == 1
    assert result.exception
    assert f"Credential {CREDENTIAL_ID} does not exist" in result.output


def test_train_fails_with_multiple_non_default_credentials(monkeypatch):
    """grid train fails if multiple non default credentials."""
    monkeypatch.setattr(grid.Grid, '_init_client', monkey_patch_client)

    monkeypatch.setattr(grid.Grid, 'get_credentials',
                        monkey_patch_get_credentials_multiple_no_default)

    result = RUNNER.invoke(cli.train, ['--', 'tests/data/script.py'])

    assert result.exit_code == 1
    assert result.exception
    assert 'Detected multiple credentials. Which would you like to use?' in result.output


def test_train_fails_if_config_not_found(tmp_path, monkeypatch):
    """grid train fails if config not found"""
    monkeypatch.setattr(grid.Grid, '_init_client', monkey_patch_client)

    monkeypatch.setattr(grid.Grid, 'get_credentials',
                        monkey_patch_get_credentials)

    result = RUNNER.invoke(cli.train, [
        '--grid_credential', CREDENTIAL_ID, '--grid_config', 'no-file',
        'tests/data/script.py'
    ])

    assert result.exit_code == 2
    assert result.exception
    assert 'Could not open file' in result.output


def test_train_fails_with_bad_config(tmp_path, monkeypatch):
    """grid train fails with bad config"""
    monkeypatch.setattr(grid.Grid, '_init_client', monkey_patch_client)

    monkeypatch.setattr(grid.Grid, 'get_credentials',
                        monkey_patch_get_credentials)

    bad_yamls = [
        """
        """, """
        compute
        """, """
        -
        """, """
        - random
        """
    ]

    for i, content in enumerate(bad_yamls):
        bad_config = tmp_path / f"bad_config_{i}.yaml"
        bad_config.write_text(content)

        result = RUNNER.invoke(cli.train, [
            '--grid_credential', CREDENTIAL_ID, '--grid_config',
            bad_config.as_posix(), '--', 'tests/data/script.py'
        ])

        assert result.exit_code == 2
        assert result.exception
        assert 'Could not load your YAML config file' in result.output


def test_train_fails_with_incomplete_config(tmp_path, monkeypatch):
    """grid train fails with incomplete config"""
    monkeypatch.setattr(grid.Grid, '_init_client', monkey_patch_client)

    monkeypatch.setattr(grid.Grid, 'get_credentials',
                        monkey_patch_get_credentials)

    bad_yamls = [
        """
        no_compute:
        """, """
        compute:
            no_train:
        """, """
        compute:
            train:
                random: e
        """
    ]

    for i, content in enumerate(bad_yamls):
        bad_config = tmp_path / f"bad_config_{i}.yaml"
        bad_config.write_text(content)

        result = RUNNER.invoke(cli.train, [
            '--grid_credential', CREDENTIAL_ID, '--grid_config',
            bad_config.as_posix(), '--ignore_warnings', 'tests/data/script.py'
        ])

        assert result.exit_code == 1
        assert result.exception
        assert isinstance(result.exception, KeyError)

    bad_yamls = [
        """
        compute:
        """, """
        compute:
            - random
        """, """
        compute:
            no_train
        """, """
        compute:
            - random: value
        """, """
        compute:
            train
        """, """
        compute:
            train:
        """, """
        compute:
            train:
                random
        """, """
        compute:
            train:
                - random
        """, """
        compute:
            train:
                - random: value
        """
    ]
    for i, content in enumerate(bad_yamls):
        bad_config = tmp_path / f"bad_config_{i}.yaml"
        bad_config.write_text(content)

        result = RUNNER.invoke(cli.train, [
            '--grid_credential', CREDENTIAL_ID, '--grid_config',
            bad_config.as_posix(), '--ignore_warnings', 'tests/data/script.py'
        ])

        assert result.exit_code == 1
        assert result.exception
        assert isinstance(result.exception, TypeError)


def test_train_fails_if_description_is_too_long(monkeypatch):
    """grid train fails if description is too long."""
    description = 201 * '-'  #  200 characters is the limit.
    result = RUNNER.invoke(cli.train, [
        '--grid_description', description, '--grid_credential', CREDENTIAL_ID,
        '--grid_cpus', 1, '--', 'tests/data/script.py'
    ])
    assert result.exit_code == 2
    assert result.exception


def test_train_fails_if_run_name_fails_validation(monkeypatch):
    """grid train fails if run name does not match validation requirements."""
    run_name = "RUN"  # capital letters not allowed in run name
    monkeypatch.setattr(grid.Grid, '_init_client', monkey_patch_client)

    monkeypatch.setattr(grid.Grid, 'get_credentials',
                        monkey_patch_get_credentials)
    monkeypatch.setattr(grid.Grid, '_set_local_credentials', lambda x: True)
    monkeypatch.setattr(grid.Grid, '_check_user_github_token',
                        monkey_patch_token_check)

    result = RUNNER.invoke(cli.train, [
        '--grid_credential',
        CREDENTIAL_ID,
        '--grid_name',
        run_name,
        '--grid_cpus',
        1,
        '--',
        'tests/data/script.py',
    ])
    assert result.exit_code == 2
    assert result.exception


def test_train_default_cred(monkeypatch):
    """grid train succeeds and uses default creds"""
    monkeypatch.setattr(grid, 'gql', lambda x: x)
    monkeypatch.setattr(grid.Grid, '_init_client', monkey_patch_client)

    monkeypatch.setattr(grid.Grid, 'get_credentials',
                        monkey_patch_get_credentials_multiple)

    result = RUNNER.invoke(cli.train,
                           ['--ignore_warnings', 'tests/data/script.py'])

    assert result.exit_code == 0
    assert not result.exception
    assert f'Using default cloud credentials {CREDENTIAL_ID} to run on' in result.output


def test_train_fails_no_ignore_warnings(monkeypatch):
    """grid train fails if no ignore_warnings"""
    monkeypatch.setattr(grid, 'gql', lambda x: x)
    monkeypatch.setattr(grid.Grid, '_init_client', monkey_patch_client)

    monkeypatch.setattr(grid.Grid, 'get_credentials',
                        monkey_patch_get_credentials)
    monkeypatch.setattr(grid.Grid, '_set_local_credentials', lambda x: True)
    monkeypatch.setattr(grid.Grid, '_check_user_github_token',
                        monkey_patch_token_check)

    env.DEBUG = True
    result = RUNNER.invoke(
        cli.train,
        ['--grid_credential', CREDENTIAL_ID, 'tests/data/script.py'])

    #assert result.exit_code == 0
    #assert not result.exception
    assert '1 CPU will be used as a default.' in result.output


def test_train(monkeypatch):
    """grid train returns 0 exit code"""
    monkeypatch.setattr(grid, 'gql', lambda x: x)
    monkeypatch.setattr(grid.Grid, '_init_client', monkey_patch_client)

    monkeypatch.setattr(grid.Grid, 'get_credentials',
                        monkey_patch_get_credentials)
    monkeypatch.setattr(grid.Grid, '_set_local_credentials', lambda x: True)
    monkeypatch.setattr(grid.Grid, '_check_user_github_token',
                        monkey_patch_token_check)

    env.DEBUG = True
    description = 199 * '-'  # 200 characters is the limit.
    result = RUNNER.invoke(cli.train, [
        '--grid_credential', CREDENTIAL_ID, '--grid_description', description,
        '--grid_strategy', 'grid_search', '--grid_trials', "1",
        '--ignore_warnings', 'tests/data/script.py'
    ])
    assert result.exit_code == 0
    assert not result.exception


def test_train_with_framework(monkeypatch):
    """grid train takes a famework parameters"""
    monkeypatch.setattr(grid, 'gql', lambda x: x)
    monkeypatch.setattr(grid.Grid, '_init_client', monkey_patch_client)

    monkeypatch.setattr(grid.Grid, 'get_credentials',
                        monkey_patch_get_credentials)
    monkeypatch.setattr(grid.Grid, '_set_local_credentials', lambda x: True)
    monkeypatch.setattr(grid.Grid, '_check_user_github_token',
                        monkey_patch_token_check)

    env.DEBUG = True
    result = RUNNER.invoke(cli.train, [
        '--grid_credential', CREDENTIAL_ID, '--grid_description', 'test',
        '--grid_strategy', 'grid_search', '--grid_trials', "1",
        '--grid_framework', 'lightning', '--ignore_warnings',
        'tests/data/script.py'
    ])
    assert result.exit_code == 0
    assert not result.exception
