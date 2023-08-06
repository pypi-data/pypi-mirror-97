from typing import Optional

import click

from grid import Grid
from grid.cli.grid_train import get_credentials


@click.group(invoke_without_command=True)
@click.pass_context
def datastores(ctx) -> None:
    """Manages datastore workflows in Grid"""
    return


@datastores.command()
@click.argument('session_name', nargs=1)
@click.pass_context
def resume(ctx, session_name: str):
    """Resumes uploading a datastore"""
    client = Grid()
    if session_name == "list":
        client.list_resumable_datastore_sessions()
        return

    client.resume_datastore_session(session_name)


@datastores.command()
@click.option('--source',
              required=True,
              help="""
              Source to create datastore from. This could either be a local directory
              (e.g: /opt/local_folder) or a remote HTTP URL pointing to a TAR file
              (e.g: http://some_domain/data.tar.gz)
              """)
@click.option('--name', type=str, required=True, help='Name of the datastore')
@click.option('--grid_credential',
              type=str,
              required=False,
              help='Grid credential ID that will store this datastore')
@click.option('--compression',
              type=bool,
              required=False,
              help='Compresses datastores with GZIP when flag is passed.',
              default=False,
              is_flag=True)
@click.pass_context
def create(ctx,
           source: str,
           name: str,
           grid_credential: Optional[str] = None,
           compression: bool = False) -> None:
    """Creates datastores"""
    client = Grid()

    credential = get_credentials(client=client,
                                 grid_credential=grid_credential)

    client.upload_datastore(source=source,
                            credential_id=credential['credentialId'],
                            name=name,
                            compression=compression)


@datastores.command()
@click.pass_context
def list(ctx) -> None:
    """Lists datastores"""
    client = Grid()
    client.list_datastores()


@datastores.command()
@click.option('--name', type=str, required=True, help='Name of the datastore')
@click.option('--version',
              type=int,
              required=True,
              help='Version of the datastore')
@click.option('--grid_credential',
              type=str,
              required=True,
              help='Credential Id for this datastore')
@click.pass_context
def delete(ctx, name: str, version: int, grid_credential: str) -> None:
    """Lists datastores"""
    client = Grid()
    client.delete_datastore(name=name,
                            version=version,
                            credential_id=grid_credential)
