import click
import pytest
from tests.utilities import captured_output

from grid.cli.grid_credentials import print_creds_table


class TestCredentialsUtilities:
    """Test utilities in credentials."""
    @staticmethod
    def test_print_creds_table_raises_exception():
        with pytest.raises(click.ClickException):
            print_creds_table(creds=[])

    @staticmethod
    def test_print_creds_table_prints_table():
        credentials = [{
            'credentialId': 'test',
            'provider': 'test',
            'alias': 'test',
            'createdAt': '2020-05-16T21:21:10.745898+00:00',
            'lastUsedAt': 'test',
            'defaultCredential': 'test'
        }]
        expected_columns = [
            'Credential', 'Provider', 'Alias', 'Created At', 'Last Used At',
            'Default'
        ]

        with captured_output() as (out, _):
            print_creds_table(creds=credentials)

        output = out.getvalue().strip()
        for column in expected_columns:
            assert column in output
