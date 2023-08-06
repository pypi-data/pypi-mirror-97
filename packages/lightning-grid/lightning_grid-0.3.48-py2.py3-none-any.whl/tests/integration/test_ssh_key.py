import logging
from pathlib import Path
import tempfile
from unittest.mock import MagicMock

from click.testing import CliRunner
from tests import resolvers
from tests.mock_backend import GridAIBackenedTestServer

from grid import cli
from grid import Grid
import grid.client as grid

logger = logging.getLogger()


def invoke(*args):
    result = CliRunner().invoke(cli.ssh_keys, args)
    output = result.stdout_bytes.decode('utf-8')
    logger.info(f"\n===== ssh-key {' '.join(args)} =====\n" + output)
    assert result.exit_code == 0
    return output


class TestSSHKey:
    def test_ssh_keys_flow(self, monkeypatch):
        # Disable this mock to test against real API server
        monkeypatch.setattr(Grid, '_init_client', MagicMock())
        monkeypatch.setattr(Grid, 'execute_gql', MagicMock())

        key_pub = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIL2cDUezQeiAzETVPCe4O1NI/U+04nYIeDHZs3uWPWOC nmiculinic@atlas"

        with tempfile.TemporaryDirectory() as tmpdirname:
            key_path_pub = Path(tmpdirname) / "id_ed25519.pub"
            key_path_pub.write_text(key_pub)

            key_id = invoke(
                'add', "my key",
                str(key_path_pub))[len('Added key with id: '):].strip()
            logger.info(f"key_id {key_id}")
            invoke('list')
            invoke('authorized_keys')
            invoke('rm', key_id)
            invoke('list')

    def test_list(self, monkeypatch):
        resolver = MagicMock(return_value=[{
            "id": "8156af4e-b7fc-466f-9cbf-a3db840fff45",
            "publicKey": "AAAA GGGG ZZZZ",
            "name": "my key"
        }])

        def monkey_patch_client(x):
            x.client = GridAIBackenedTestServer()

        monkeypatch.setattr(grid.Grid, '_init_client', monkey_patch_client)
        monkeypatch.setattr(grid, 'gql', lambda x: x)
        monkeypatch.setattr(resolvers, 'get_public_ssh_keys', resolver)
        result = invoke("list")
        resolver.assert_called()
        assert "8156af4e-b7fc-466f-9cbf-a3db840fff45" in result
        assert "AAAA GGGG ZZZZ" in result

    @staticmethod
    def test_add_ssh_key(monkeypatch):
        resolver = MagicMock(
            return_value={
                "message": "ok",
                "success": True,
                "id": "8156af4e-b7fc-466f-9cbf-a3db840fff45",
            })

        def monkey_patch_client(x):
            x.client = GridAIBackenedTestServer()

        monkeypatch.setattr(grid.Grid, '_init_client', monkey_patch_client)
        monkeypatch.setattr(grid, 'gql', lambda x: x)
        monkeypatch.setattr(resolvers, 'add_ssh_public_key', resolver)
        key_pub = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIL2cDUezQeiAzETVPCe4O1NI/U+04nYIeDHZs3uWPWOC nmiculinic@atlas"
        with tempfile.TemporaryDirectory() as tmpdirname:
            key_path_pub = Path(tmpdirname) / "id_ed25519.pub"
            key_path_pub.write_text(key_pub)
            result = invoke("add", "my key", str(key_path_pub)).strip()
            assert result == 'Added key my key with id: 8156af4e-b7fc-466f-9cbf-a3db840fff45'

        resolver.assert_called()

    def test_remove_ssh_key(self, monkeypatch):
        resolver = MagicMock(return_value={
            "success": True,
            "message": "deleted",
        })

        def monkey_patch_client(x):
            x.client = GridAIBackenedTestServer()

        monkeypatch.setattr(grid.Grid, '_init_client', monkey_patch_client)
        monkeypatch.setattr(grid, 'gql', lambda x: x)
        monkeypatch.setattr(resolvers, 'delete_ssh_public_key', resolver)

        invoke("rm", "8156af4e-b7fc-466f-9cbf-a3db840fff45")
        _, kwargs = resolver.call_args  # skipcq:PYL-E0633
        assert kwargs == {'id': '8156af4e-b7fc-466f-9cbf-a3db840fff45'}
