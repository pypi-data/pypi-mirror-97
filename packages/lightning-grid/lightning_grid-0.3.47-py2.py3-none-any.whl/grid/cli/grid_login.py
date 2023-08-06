from typing import Optional

import click

from grid import Grid
import grid.globals as env


@click.option('--username', type=str, help='Username used in Grid')
@click.option('--key', type=str, help='API Key from Grid')
@click.command()
def login(username: Optional[str] = None, key: Optional[str] = None) -> None:
    """Login into Grid AI."""
    client = Grid(load_local_credentials=False)

    # Prompt the user for username and API Key.
    # We ask for the username first because that's
    # the same as their Github usernames.
    if not username:
        username = click.prompt('Please provide your Grid or GitHub username')
    if not key:
        settings_url = env.GRID_URL.replace("graphql", "#") + "/settings"
        click.launch(settings_url)
        key = click.prompt('Please provide your Grid API key')

    client.login(username=username, key=key)
    click.echo('Login successful. Welcome to Grid.')
