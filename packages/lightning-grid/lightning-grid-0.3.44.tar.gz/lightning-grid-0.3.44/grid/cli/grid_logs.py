from typing import Optional

import click

from grid import Grid


@click.command()
@click.argument('experiment', type=str, nargs=1)
@click.option('--n_lines',
              default=10,
              type=int,
              help='Number of log lines (from the end) to return.')
@click.option('--page',
              type=int,
              help='Which page to fetch from archived logs')
@click.option('--max_lines',
              type=int,
              help='Maximum number of lines to print in terminal')
@click.option(
    '--use_pager',
    is_flag=True,
    default=False,
    help='If the log output should be displayed as a pager scrollable')
def logs(experiment: str, n_lines: int, page: Optional[int],
         max_lines: Optional[int], use_pager: bool) -> None:
    """Gets logs from an experiment."""
    # Instantiate client.
    client = Grid()

    # Call client.
    client.experiment_logs(experiment_id=experiment,
                           n_lines=n_lines,
                           page=page,
                           max_lines=max_lines,
                           use_pager=use_pager)
