import click

from grid.client import Grid
import grid.globals as env
from grid.types import ObservableType
from grid.utilities import is_experiment


@click.command()
@click.argument('run_or_experiment', type=str, nargs=1)
@click.argument('page', type=str, nargs=1, required=False)
def view(run_or_experiment: str, page: str) -> None:
    """Grid view shows we web UI page for your runs and experiments."""
    # Fetch URL from globals.
    url = env.GRID_URL.replace('/graphql', '#')

    # Instantiate Grid client.
    client = Grid()

    # Figure out which object is requested
    # so we can construct path.
    base_path = 'view'
    qualifier_path = ''
    if is_experiment(run_or_experiment):
        qualifier_path = 'experiment'
        kind = ObservableType.EXPERIMENT
    else:
        qualifier_path = 'run'
        kind = ObservableType.RUN

    # Combine all strings into a single URL.
    launch_url = None
    if page:
        launch_url = '/'.join(
            [url, base_path, qualifier_path, run_or_experiment, page])
    else:
        launch_url = '/'.join(
            [url, base_path, qualifier_path, run_or_experiment])

    # If the page requested is Tensorboard
    # get the URLs for those services from the backend and
    # open those specific pages in the browser.
    #
    # We'll use Tensorboard filtering to construct the right URL.
    error_message = ''
    tensorboard_url = None
    if page == 'tensorboard':

        # If the user has asked for aexperiment, extract
        # the run name from the identn ifier so we an fetch the
        # Tensorboard instance for that.
        run_name = run_or_experiment
        if kind == ObservableType.EXPERIMENT:
            run_name = '-'.join(run_or_experiment.split('-')[:-1])

        # Always get the status for a given Run because
        # that's where we store the resource URLs.
        observable = client.status(kind=ObservableType.RUN,
                                   identifiers=[run_name])

        # Finds the run result.
        run_data = None
        for run in observable['getRuns']:
            if run['name'] == run_name:
                run_data = run
                break

        # Construct the URLs for both services.
        if run_data:
            resource_urls = run_data.get('resourceUrls')
            if resource_urls:
                tensorboard_url = run_data['resourceUrls'].get('tensorboard')
                if tensorboard_url:
                    tensorboard_url = f"{tensorboard_url}#scalars&regexInput={run_or_experiment}"

            if not tensorboard_url:
                error_message = "Tensorboard isn't ready yet."

            launch_url = tensorboard_url

    # If we could not find the requested URL, raise an error.
    if not launch_url:
        raise click.ClickException(
            f'Could not view page {page} for {run_or_experiment}. {error_message}'
        )

    # Open browser.
    click.echo()
    click.echo(f'Opening URL: {launch_url}')
    click.echo()

    click.launch(launch_url)
