from typing import List, Optional

import click

from grid import Grid
from grid.utilities import check_is_experiment


@click.command()
@click.option('--download_dir',
              type=click.Path(exists=False, file_okay=False, dir_okay=True),
              required=False,
              default='./grid_artifacts',
              help='Download directory that will host all artifact files')
@click.argument('experiments',
                type=str,
                required=True,
                nargs=-1,
                callback=check_is_experiment)
def artifacts(experiments: List[str],
              download_dir: Optional[str] = None) -> None:
    """Downloads artifacts for a given experiment or set of experiments."""
    client = Grid()

    for experiment in experiments:
        client.download_experiment_artifacts(experiment_id=experiment,
                                             download_dir=download_dir)
