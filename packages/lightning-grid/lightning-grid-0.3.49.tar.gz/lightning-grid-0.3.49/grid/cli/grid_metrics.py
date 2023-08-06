from typing import List

import click

from grid import Grid


@click.command()
@click.argument('experiment', type=str, nargs=1)
@click.argument('metric', type=str, nargs=1)
@click.option('--n_lines',
              default=10,
              type=int,
              help='Number of metrics lines (from the end) to return.')
def metrics(experiment: str, metric: str, n_lines: int) -> None:
    """Gets metric values from an experiment."""
    # Instantiate client.
    client = Grid()

    # Call client.
    client.experiment_metrics(experiment_id=experiment,
                              metric=metric,
                              n_lines=n_lines)
