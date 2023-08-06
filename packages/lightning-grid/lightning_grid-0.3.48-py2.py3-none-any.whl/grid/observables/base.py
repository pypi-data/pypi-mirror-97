import ast
from typing import List

import click
from gql import gql
from rich.console import Console
from rich.progress import BarColumn
from rich.progress import Progress
from rich.progress import TextColumn
from rich.table import Table
from yaspin import yaspin

import grid.globals as env

#  Maps backend class types to user-friendly messages.
TASK_CLASS_MAPPING = {
    'grid.core.repository_builder.RepositoryBuilder': 'Building container',
    'grid.core.cluster.Cluster': 'Creating cluster',
    'grid.core.trainer.experiment.Experiment': 'Scheduling experiment',
    'grid.core.trainer.run.RunNodePool': 'Creating node pool',
    'grid.core.trainer.interactive.InteractiveNodeTask':
    'Creating interactive node',
    'grid.core.trainer.experiment.ExperimentsWarpSpeed':
    'Scheduling experiment'
}

# Backend classes that we don't show to users. These
# are automatically triggered if a given user does not
# have global properties set.
TASK_CLASS_IGNORE = (
    'grid.core.clusters.deploy_tensorboard.ReconcileTensorboard',
    'grid.core.clusters.global_user_cluster.ReconcileCluster',
    'grid.core.user.ReconcileUser')


def style_status(format_string: str, status: str):
    """
    Styles a status message using click.stye.

    Parameters
    ----------
    status: str
        Status message to style.

    Return
    ------
    styled_status: str
        Styled string
    """
    styled_status = format_string

    if status == 'failed':
        styled_status = click.style(styled_status, fg='red')
    elif status in ('finished', 'ready'):
        styled_status = click.style(styled_status, fg='green')
    elif status in ('running', 'queued', 'pending'):
        styled_status = click.style(styled_status, fg='yellow')
    elif status in ('cancelled'):
        styled_status = click.style(styled_status, fg='white')

    return styled_status


class BaseObservable:
    def __init__(self, client, spinner_load_type=""):
        self.client = client
        self.console = Console()
        self.spinner = yaspin(text=f"Loading {spinner_load_type}...",
                              color="yellow")

    @staticmethod
    def create_table(columns: List[str]) -> Table:
        table = Table(show_header=True, header_style="bold green")

        table.add_column(columns[0], style='dim')
        for column in columns[1:]:
            table.add_column(column, justify='right')

        return table

    def _get_task_run_dependencies(self, run_name: str):
        """Gets dependency data for a given Run"""
        query = gql("""
        query (
            $runName: ID!
        ) {
            getRunTaskStatus (
                runName: $runName
            ) {
                success
                runId
                name
                status
                message
                dependencies {
                    taskId
                    status
                    taskType
                    message
                    error
                }
            }
        }
        """)
        params = {'runName': run_name}

        #  Make GraphQL query.
        result = None
        try:
            result = self.client.execute(query, variable_values=params)
            if not result['getRunTaskStatus']['success']:
                raise Exception(result['getRunTaskStatus'])
        except Exception as e:  # skipcq: PYL-W0703
            message = ast.literal_eval(str(e))['message']
            self.spinner.fail("✘")
            self.spinner.stop()

            if env.DEBUG:
                click.echo(message)

            if 'not found' in message or 'No runs available' in message:
                raise click.ClickException(
                    f'Run {run_name} not found. Did you cancel it already?')

        if result:
            dependencies = result['getRunTaskStatus']['dependencies']
            return dependencies

    def _get_task_run_status(self, run_name: str):
        #  Get dependency data.
        dependencies = self._get_task_run_dependencies(run_name=run_name)

        #  Dict to collect all errors for given tasks.
        dependency_data = {
            k: {
                'statuses': [],
                'errors': [],
                'messages': []
            }
            for k in TASK_CLASS_MAPPING if k not in TASK_CLASS_IGNORE
        }
        for task in dependencies:
            if task['taskType'] in TASK_CLASS_IGNORE:
                continue
            dependency_data[task['taskType']]['statuses'].append(
                task['status'])
            dependency_data[task['taskType']]['errors'].append(task['error'])
            dependency_data[task['taskType']]['messages'].append(
                task['message'])

        #  Inform user that she can see error logs by passing
        #  a flag.
        all_statuses = []
        for status in dependency_data.values():
            all_statuses += status['statuses']

        if any(s == 'failed' for s in all_statuses) and \
            not env.SHOW_PROCESS_STATUS_DETAILS:
            click.echo(f'''
        The Run "{run_name}" failed to start due to a setup error.
        You can see the errors by running

            grid status {run_name} --details

            ''')

        #  If there's an error with and pre-run steps, then
        #  print that error to the terminal.
        if env.SHOW_PROCESS_STATUS_DETAILS:
            for key, value in dependency_data.items():
                for error, message, status in zip(value['errors'],
                                                  value['messages'],
                                                  all_statuses):
                    styled_key = style_status(TASK_CLASS_MAPPING[key], status)
                    if error:
                        for line in error.splitlines():
                            click.echo(f'[{styled_key}] {line}')
                    else:
                        click.echo(f'[{styled_key}] {message} ... ')
