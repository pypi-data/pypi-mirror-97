from typing import List, Optional

import click
from click.exceptions import BadArgumentUsage

from grid import Grid
from grid.utilities import is_experiment


def _check_is_experiment(_ctx, _param, value):
    """
    Click callback that checks if passed list of experiments are
    actual experiments.
    """
    for experiment in value:
        if not is_experiment(experiment):
            raise BadArgumentUsage(
                f'{experiment} is not an experiment.'
                'You can only download artifacts for experiments.')

    return value


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
                callback=_check_is_experiment)
def artifacts(experiments: List[str],
              download_dir: Optional[str] = None) -> None:
    """Downloads artifacts for a given experiment or set of experiments."""
    client = Grid()

    for experiment in experiments:
        client.download_experiment_artifacts(experiment_id=experiment,
                                             download_dir=download_dir)
