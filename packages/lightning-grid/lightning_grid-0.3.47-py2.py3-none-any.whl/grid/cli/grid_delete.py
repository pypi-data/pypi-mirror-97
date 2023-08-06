import click

from grid import Grid
from grid.utilities import is_experiment


@click.command()
@click.argument('run_or_experiment', type=str, required=True, nargs=1)
def delete(run_or_experiment: str) -> None:
    """Deletes running run or experiment."""
    client = Grid()
    confirmed_is_experiment = is_experiment(run_or_experiment)

    # Confirm that the user really wants to do this.
    object_str = 'Experiment' if confirmed_is_experiment else 'Run'
    warning_str = click.style('WARNING!', fg='red')
    message = f"""

    {warning_str}

    Your are about to delete the {object_str} ({run_or_experiment}).
    This will delete all the associated artifacts, logs, and metadata.

    Are you sure you want to do this?

   """
    click.confirm(message, abort=True)

    if confirmed_is_experiment:
        client.delete(experiment_id=run_or_experiment)
    else:
        client.delete(run_id=run_or_experiment)
