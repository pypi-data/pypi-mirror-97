from click.testing import CliRunner
from tests.mock_backend import resolvers
from tests.utilities import create_test_credentials
from tests.utilities import monkey_patch_client

from grid import cli
import grid.client as grid

RUNNER = CliRunner()


class TestDelete:
    @classmethod
    def setup_class(cls):
        grid.Grid._init_client = monkey_patch_client
        grid.gql = lambda x: x

        create_test_credentials()

    def test_deletecluster_fails_without_arguments(self):
        """grid deletecluster fails without arguments"""
        result = RUNNER.invoke(cli.deletecluster, [])
        assert result.exit_code == 2
        assert result.exception

    def test_deletecluster_fails_with_extra_arguments(self):
        """grid deletecluster fails with extra arguments"""
        cluster_ids = ['test-cluster1', 'test-cluster2']
        result = RUNNER.invoke(cli.deletecluster, cluster_ids)
        assert result.exit_code == 2
        assert result.exception

    def test_deletecluster_success(self):
        """grid deletecluster succeeds"""
        cluster_id = 'test-run'
        result = RUNNER.invoke(cli.deletecluster, [cluster_id])
        assert result.exit_code == 0
        assert not result.exception
        assert 'Cluster deleted successfully' in result.output

    def test_deletecluster_failure(self, monkeypatch):
        """grid deletecluster succeeds for an existing cluster"""
        def mp_delete_cluster(*args, **kwargs):
            return {
                'success': False,
            }

        monkeypatch.setattr(resolvers, 'delete_cluster', mp_delete_cluster)
        cluster_id = 'test-run'
        result = RUNNER.invoke(cli.deletecluster, [cluster_id])
        assert result.exit_code == 0
        assert not result.exception
        assert 'Cluster failed to delete' in result.output
