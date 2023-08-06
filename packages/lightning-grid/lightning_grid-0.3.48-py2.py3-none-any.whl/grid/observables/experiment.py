import ast
from shlex import split
from typing import Optional

import click
from gql import Client
from gql import gql
from rich.table import Table
import websockets

from grid.observables.base import BaseObservable
from grid.observables.base import style_status
from grid.observables.base import TASK_CLASS_MAPPING
from grid.utilities import get_experiment_duration_string
from grid.utilities import get_param_values


class Experiment(BaseObservable):
    def __init__(self, client: Client, identifier: str):
        self.client = client
        self.run_name = identifier

        super().__init__(client=client)

    def get_history(self, experiment_id: Optional[str] = None):
        """
        Parameters
        ----------
        experiment_id: Optional[str]
            Experiment ID
        """
        self.spinner.start()
        self.spinner.text = 'Getting Experiments ...'

        query = gql("""
        query (
            $runName: ID!
        ) {
            getExperiments(runName: $runName) {
                experimentId
                status
                invocationCommands
                createdAt
                finishedAt
                commitSha
                run {
                    runId
                }
                startedRunningAt
            }
        }
        """)
        params = {'runName': self.run_name}
        try:
            self._get_task_run_status(run_name=self.run_name)
        except ValueError:
            return

        result = self.client.execute(query, variable_values=params)

        if not result['getExperiments']:
            click.echo(f'No experiments available for run "{self.run_name}"')
            return

        self.spinner.text = 'Done!'
        self.spinner.ok("✔")
        self.spinner.stop()
        table = self.render_experiments(result['getExperiments'])
        self.console.print(table)

    def get(self, experiment_id: Optional[str] = None):
        """
        Parameters
        ----------
        experiment_id: Optional[str]
            Experiment ID
        """
        self.spinner.start()
        self.spinner.text = 'Fetching experiment status ...'

        query = gql("""
        query (
            $runName: ID!
        ) {
            getExperiments(runName: $runName) {
                experimentId
                status
                invocationCommands
                createdAt
                finishedAt
                commitSha
                run {
                    runId
                }
                startedRunningAt
            }
        }
        """)
        params = {'runName': self.run_name}
        try:
            self.spinner.text = 'Fetching experiment status ... done!'
            self._get_task_run_status(run_name=self.run_name)
            self.spinner.ok("✔")
        except ValueError:
            return
        finally:
            self.spinner.stop()

        result = self.client.execute(query, variable_values=params)

        experiments = result['getExperiments']

        if not experiments:
            click.echo(f'No experiments available for run "{self.run_name}"')
            return

        table = self.render_experiments(experiments)
        self.console.print(table)
        return result

    @staticmethod
    def render_experiments(experiments) -> Table:
        base_columns = [
            'Experiment',
            'Command',
            'Status',
            'Duration',
        ]
        if not experiments:
            return BaseObservable.create_table(columns=base_columns)

        command = experiments[0]['invocationCommands']
        toks = split(command)
        hparams = [tok.replace('--', '') for tok in toks if '--' in tok]

        table_columns = base_columns + hparams
        table = BaseObservable.create_table(columns=table_columns)

        for experiment in experiments:
            # Split hparam vals
            command = experiment['invocationCommands']
            base_command, *hparam_vals = get_param_values(command)
            # Get job duration - Since experiment started if running, since experiment created if queued
            duration_str = get_experiment_duration_string(
                created_at=experiment['createdAt'],
                started_running_at=experiment['startedRunningAt'],
                finished_at=experiment['finishedAt'])
            table.add_row(experiment['experimentId'], base_command,
                          experiment['status'], duration_str, *hparam_vals)
        return table

    def follow(self):
        """Follows a stream for a given Run."""
        self.spinner.text = 'Following Run details ...'
        self.spinner.start()

        #  Defines terminal states.
        terminal_state = ('finished', 'failed', 'cancelled')

        #  Get list of dependency IDs.
        dependencies = self._get_task_run_dependencies(run_name=self.run_name)

        # If no dependencies exists
        if not dependencies:
            raise click.ClickException(
                f"Could not find run with name {self.run_name}")

        dependency_ids = []
        dependency_statuses = []
        dependency_mapping = {}
        for dependency in dependencies:
            status = dependency['status']
            dependency_statuses.append(status)
            if status not in terminal_state:
                dependency_ids.append(dependency['taskId'])
                dependency_mapping[dependency['taskId']] = dependency

        #  Shows useful message to user.
        if all(s in terminal_state for s in dependency_statuses):
            self.spinner.ok("✔")
            self.spinner.stop()

            error_message = ''
            if any(s == 'failed' for s in dependency_statuses):
                error_message = f"""Use the following command to see errors in Run:
    grid status {self.run_name} --details"""

            # If an error was detected, raise an exception
            if error_message != '':
                click.echo()
                raise click.ClickException(f"""{error_message}""")

            # Get experiment statuses
            self.get()

            # Return here because there's no more scheduling steps to follow.
            return

        # If experiments are not in a terminal state,
        # open a websocket connection and consume messages.
        subscription = gql("""
        subscription GetTaskStream ($taskIds: [ID]!) {
            getTaskMessage(
                taskIds: $taskIds) {
                    taskId
                    message
                    timestamp
                    className
            }
        }
        """)

        params = {'taskIds': dependency_ids}

        #  Create a GraphQL subscription via websockect
        #  connection.
        try:
            stream = self.client.subscribe(subscription,
                                           variable_values=params)

            first_message = True
            for log in stream:

                #  Closes the spinner.
                if first_message:
                    self.spinner.text = 'Done!'
                    self.spinner.ok("✔")
                    first_message = False

                #  Patch a class name if not available with
                #  a placeholder.
                class_name = log['getTaskMessage']['className']
                if not class_name:
                    class_name = '-' * 10
                else:
                    class_name = TASK_CLASS_MAPPING[class_name]

                #  Extract task ID and status.
                task_id = log['getTaskMessage']['taskId']
                task_status = dependency_mapping[task_id]['status']

                #  Print each line to terminal.
                styled_class_name = style_status(class_name, task_status)
                message = log['getTaskMessage']['message']
                click.echo(f'[{styled_class_name}] {message}')

        # If connection is suddenly closed, indicate that a
        # known error happened.
        except websockets.exceptions.ConnectionClosedError:
            self.spinner.fail("✘")
            self.spinner.stop()
            raise click.ClickException('Could not fetch log data.')

        except websockets.exceptions.ConnectionClosedOK:
            self.spinner.fail("✘")
            self.spinner.stop()
            raise click.ClickException(
                'Could not continue fetching log stream.')

        #  Raise any other errors that the backend may raise.
        except Exception as e:  # skipcq: PYL-W0703
            self.spinner.fail("✘")
            self.spinner.stop()
            if 'Server error:' in str(e):
                e = str(e).replace('Server error: ', '')[1:-1]

            message = ast.literal_eval(str(e))['message']
            raise click.ClickException(message)
