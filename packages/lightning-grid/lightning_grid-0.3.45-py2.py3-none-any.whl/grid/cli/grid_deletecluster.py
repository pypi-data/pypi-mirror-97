import click

from grid import Grid


@click.command()
@click.argument('cluster_id', type=str, required=True, nargs=1)
def deletecluster(cluster_id: str) -> None:
    """Deletes cluster"""
    client = Grid()

    client.delete_cluster(cluster_id=cluster_id[0])
