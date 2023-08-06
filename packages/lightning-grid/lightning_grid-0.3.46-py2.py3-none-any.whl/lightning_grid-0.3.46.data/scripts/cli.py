#!python
# Copyright 2020 Grid AI Inc.
"""Entrypoint for the Grid CLI."""
import sys

import click
from click import ClickException

import grid.cli as cli
import grid.globals as env
from grid.metadata import __logo__
from grid.metadata import __version__
from grid.tracking import Segment
from grid.tracking import TrackingEvents
from grid.utilities import introspect_module


@click.group()
@click.option(
    '--debug',
    type=bool,
    help='Used for logging additional information for debugging purposes.',
    is_flag=True)
def main(debug: bool = True) -> None:
    """Grid CLI"""
    if debug:
        env.logger.info('Starting gridrunner in DEGUB mode.')

    env.DEBUG = debug


@main.command()
def version() -> None:
    """
    Prints CLI version to stdout
    """
    logo = click.style(__logo__, fg='green')
    click.echo(logo)

    version = f"""
                                Grid CLI ({__version__})
                               https://docs.grid.ai
    """
    click.echo(version)


#  Adds all CLI commands. Commands are introspected
#  from the cli module.
for command in introspect_module(cli):
    command: click.Command
    main: click.Group
    main.add_command(command)

if __name__ == '__main__':
    tracker = Segment()
    tracker.send_event(event=TrackingEvents.CLI_STARTED)
    try:
        main.main(prog_name="grid", standalone_mode=False)
        tracker.send_event(event=TrackingEvents.CLI_FINISHED)
    except ClickException as e:
        tracker.report_exception(e)
        e.show()
        sys.exit(e.exit_code)
    except Exception as e:
        tracker.report_exception(e)
        sys.exit(1)
    finally:
        tracker.flush()
