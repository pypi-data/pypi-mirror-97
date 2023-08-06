import click

from grid import Grid
from grid.utilities import is_experiment


@click.command()
@click.argument('runs_or_experiments', type=str, required=True, nargs=-1)
def cancel(runs_or_experiments: str) -> None:
    """Cancels running runs or experiments"""
    client = Grid()

    for run_or_exp in runs_or_experiments:
        #  Cancel Experiment
        if is_experiment(run_or_exp):
            client.cancel(experiment_id=run_or_exp)

        #  Cancel Run
        else:
            client.cancel(run_name=run_or_exp)
