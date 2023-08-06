from datetime import datetime
from datetime import timezone
from typing import Optional

import click
from dateutil.parser import parse as date_string_parse
from gql import Client
from gql import gql
from gql.transport.exceptions import TransportQueryError

import grid.globals as env
from grid.observables.base import BaseObservable
from grid.utilities import get_abs_time_difference
from grid.utilities import string_format_date
from grid.utilities import string_format_timedelta


class Run(BaseObservable):
    def __init__(self, client: Client, identifier: Optional[str] = []):
        self.client = client

        self.identifier = identifier

        super().__init__(client=client, spinner_load_type="Runs")

    def get(self):
        """
        Gets the run status; either for a single run or all runs for
        user.
        """
        self.spinner.start()
        self.spinner.text = 'Getting Run status ...'

        query = gql("""
        query (
            $runName: ID
        ) {
            getRuns (runName: $runName) {
                name
                createdAt
                experiments {
                    experimentId
                }
                nExperiments
                nFailed
                nCancelled
                nRunning
                nCompleted
                nQueued
                projectId
                resourceUrls {
                    tensorboard
                }
            }
        }
        """)
        run_name = None
        if self.identifier:
            run_name = self.identifier

        params = {'runName': run_name}

        try:
            result = self.client.execute(query, variable_values=params)
            self.spinner.text = 'Done!'
        except TransportQueryError as e:
            self.spinner.fail("✘")
            self.spinner.stop()
            if env.DEBUG:
                click.echo(str(e))

            raise click.ClickException(
                'Query to Grid failed. Try again in a few minutes.')

        table_cols = [
            'Run',
            'Project',
            'Status',
            'Duration',
            'Experiments',
            'Running',
            'Queued',
            'Completed',
            'Failed',
            'Cancelled',
        ]
        table = BaseObservable.create_table(columns=table_cols)

        #  Whenever we don't have yet submitted experiments,
        table_rows = 0
        for row in result['getRuns']:
            status = None

            # we only have 3 statuses for runs
            # running (if something is running)
            is_running = row['nRunning'] is not None and row['nRunning'] > 0

            # quued if there are queued elements
            is_queued = row['nQueued'] is not None and row['nQueued'] > 0

            # If anything is queued, the the status of the entire
            # run is queued. All other statuses are running in
            # all other conditions.
            if is_queued:
                status = 'queued'

            # If you have anything running (and nothing queued)
            # then, mark the run as running.
            elif is_running:
                status = 'running'

            # If it doesn't match the conditions above, just
            # skip this row and add the row and put it in history.
            else:
                # don't render table because it should be in history
                continue

            #  Change the printed key from `None` to `-` if the
            #  no data exists for those keys.
            keys = [
                'nExperiments', 'nRunning', 'nQueued', 'nCompleted', 'nFailed',
                'nCancelled'
            ]
            for key in keys:
                if row[key] is None:
                    row[key] = '-'

            # Calculate the duration column
            created_at = date_string_parse(row['createdAt'])
            delta = get_abs_time_difference(datetime.now(timezone.utc),
                                            created_at)
            duration_str = string_format_timedelta(delta)

            table.add_row(row['name'], row['projectId'], status, duration_str,
                          str(row['nExperiments']), str(row['nRunning']),
                          str(row['nQueued']), str(row['nCompleted']),
                          str(row['nFailed']), str(row['nCancelled']))

            #  Let's count how many rows have been added.
            table_rows += 1

        #  Close the spinner.
        self.spinner.ok("✔")
        self.spinner.stop()

        # If there are no Runs to render, add a
        # placeholder row indicating none are active.
        if table_rows == 0:
            table.add_row("None Active.",
                          *[" " for i in range(len(table_cols) - 1)])

        self.console.print(table)

        #  Print useful message indicating that users can run
        #  grid history.
        history_runs = len(result['getRuns']) - table_rows
        if history_runs > 0:
            click.echo(
                f'\n{history_runs} Run(s) are not active. Use `grid history` '
                'to view your Run history.')

        return result

    def get_history(self):
        """
        Fetches a complete history of runs. This includes runs that
        are not currently active.
        """
        self.spinner.start()
        self.spinner.text = 'Getting Runs ...'

        query = gql("""
        query (
            $runName: ID
        ) {
            getRuns (runName: $runName) {
                name
                createdAt
                experiments {
                    experimentId
                }
                nExperiments
                nFailed
                nCancelled
                nRunning
                nCompleted
                nQueued
            }
        }
        """)
        run_id = None
        if self.identifier:
            run_id = self.identifier[0]

        params = {'runName': run_id}

        result = self.client.execute(query, variable_values=params)

        self.spinner.text = 'Done!'
        self.spinner.ok("✔")
        self.spinner.stop()

        table_cols = [
            'Run', 'Created At', 'Experiments', 'Failed', 'Cancelled',
            'Completed'
        ]
        table = BaseObservable.create_table(columns=table_cols)

        #  Whenever we don't have yet submitted experiments,
        table_rows = result['getRuns']
        for row in table_rows:
            keys = ['nExperiments', 'nFailed', 'nCancelled', 'nCompleted']
            for key in keys:
                if row[key] is None:
                    row[key] = '-'

            # check if it is running
            is_running = row['nRunning'] is not None and row['nRunning'] > 0

            # check if queued
            is_queued = row['nQueued'] is not None and row['nQueued'] > 0

            # history is everything else
            if is_queued or is_running:
                continue

            created_at = string_format_date(date_string_parse(
                row['createdAt']))

            table.add_row(row['name'], created_at, str(row['nExperiments']),
                          str(row['nFailed']), str(row['nCancelled']),
                          str(row['nCompleted']))

        # Add placeholder row if no records are available.
        if not table_rows:
            table.add_row("No History.",
                          *[" " for i in range(len(table_cols) - 1)])

        self.console.print(table)

        return result

    def follow(self):  # pragma: no cover
        pass
