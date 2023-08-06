import random
from typing import Any, Optional

import click
from coolname import generate_slug
import yaml

from grid import Grid
import grid.globals as env
from grid.utilities import check_is_python_script
from grid.utilities import check_run_name_is_valid


@click.group(invoke_without_command=True)
@click.pass_context
def slurm(ctx) -> None:
    """Manages SLURM workflows in Grid"""
    return


def _print_submission_message(instance_type: str, provider: str,
                              credential_id: str, entrypoint: str,
                              grid_name: str):
    """Prints train submission message to the client."""
    message = f"""
        Run submitted!
        `grid slurm status` to list all runs
        `grid slurm status {grid_name}` to see all experiments for this run

        ----------------------
        Submission summary
        ----------------------
        script:                  {entrypoint}
        instance_type:           {instance_type}
        provider:                {provider}
        credentials:             {credential_id}
        grid_name:               {grid_name}
        """
    click.echo(message)


@slurm.command()
@click.argument('alias', required=False, type=str)
@click.pass_context
def get_token(ctx, alias: str) -> None:
    """Get's an auth token for registering a grid-daemon in a SLURM cluster."""
    client = Grid()
    client.get_slurm_auth_token()


@slurm.command()
@click.option('--run_name', required=False, type=str)
@click.pass_context
def cancel(ctx, run_name: str) -> None:
    """Cancels a slurm run."""
    pass


@slurm.command()
@click.option('--run_name', required=False, type=str)
@click.pass_context
def logs(ctx, run_name: str) -> None:
    """Prints the logs from a slurm job."""
    pass


@slurm.command()
@click.option(
    '--cluster_alias',
    required=True,
    type=str,
    help='The alias assigned to the daemon running in your SLURM cluster.')
@click.option('--run_name',
              required=False,
              type=str,
              help='Name of a run to see a status for.')
@click.pass_context
def status(ctx, cluster_alias: str, run_name: str = None):
    """Get's status for jobs in slurm."""
    client = Grid()

    client.slurm_status(cluster_alias=cluster_alias, run_name=run_name)


@slurm.command(context_settings=dict(ignore_unknown_options=True))
@click.option('--grid_name',
              '--g_name',
              'name',
              type=str,
              required=False,
              help='Name for this run',
              callback=check_run_name_is_valid)
@click.option(
    '--cluster_alias',
    type=str,
    required=True,
    help='The alias assigned to the daemon running in your SLURM cluster.')
@click.option(
    '--ntasks',
    type=int,
    required=False,
    help=
    'This option advises the Slurm controller that job steps run within the allocation will launch a maximum of number tasks and to provide for sufficient resources.'
)
@click.option('--ntasks_per_node',
              type=int,
              required=False,
              help='Request that ntasks be invoked on each node.')
@click.option('--job_time',
              type=str,
              required=False,
              help='Set a limit on the total run time of the job allocation.')
@click.option('--mem_per_cpu',
              type=str,
              required=False,
              help='Minimum memory required per allocated CPU.')
@click.option('--gpus',
              type=int,
              required=False,
              help='Specify the total number of GPUs required for the job.')
@click.option(
    '--cpus',
    type=int,
    required=False,
    help=
    'Advise the Slurm controller that ensuing job steps will require ncpus number of processors per task.'
)
@click.option(
    '--nodes',
    type=int,
    required=False,
    help='Request that a minimum of minnodes nodes be allocated to this job.')
@click.argument('script',
                required=True,
                type=click.Path(exists=True),
                callback=check_is_python_script)
@click.argument('script_args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def train(ctx, script: str, entrypoint: str, name: Optional[str],
          cluster_alias: str, ntasks: int, ntasks_per_node: int, job_time: str,
          mem_per_cpu: int, gpus: int, cpus: int, nodes: int,
          script_args: Optional[Any]) -> None:
    """Trains on a SLURM cluster"""
    #  Captures all other user arguments that are not
    #  parsed automatically.
    script_arguments = list(script_args)

    if env.DEBUG:
        click.echo(f"Script Arguments {script_arguments}")

    # make a fun random name when user does not pass in a name
    if name is None:
        name = f'{generate_slug(2)}-{random.randint(0, 1000)}'
        click.echo(f'No --grid_name passed, naming your run {name}')

    config = {
        "job_name": name,
        "cluster_alias": cluster_alias,
        "script_name": entrypoint,
        "script_args": script_arguments,
        "ntasks": ntasks,
        "ntasks_per_node": ntasks_per_node,
        "job_time": job_time,
        "mem_per_cpu": mem_per_cpu,
        "gpus": gpus,
        "cpus": cpus,
        "nodes": nodes
    }

    _config_yaml = yaml.dump(config)
    client = Grid()

    if not cpus and not gpus:
        notice_str = click.style('NOTICE', fg='yellow')
        cpu_warning = f"""
        {notice_str}

        Neither a CPU or GPU number was specified, so 1 CPU will be
        used as a default.

        Would you like to still continue running this job?

        """
        if not env.IGNORE_WARNINGS:
            click.confirm(cpu_warning, abort=True)

    #  Send to client.
    result = client.train_on_slurm(config_str=_config_yaml,
                                   run_name=name,
                                   script_args=script_arguments)
    if result['success']:
        #  Shows a friendly submission message to the
        #  user.
        _print_submission_message(
            instance_type=f"SLURM Cluster with alias {cluster_alias}",
            provider="Slurm",
            credential_id=cluster_alias,
            entrypoint=entrypoint,
            grid_name=name)
    else:
        message = result['message']
        raise click.ClickException(
            f"Unable to submit train task with error {message}")
