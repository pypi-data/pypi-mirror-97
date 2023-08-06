from dataclasses import dataclass
from dataclasses import field
from enum import Enum
import json
import logging
import math
import os
from pathlib import Path
import shutil
from threading import Lock
from typing import Dict, List, Optional
import uuid

from click.exceptions import ClickException
from dataclasses_json import dataclass_json
from gql import Client
from gql import gql
import requests
import yaspin

from grid.tar import get_split_size
from grid.tar import tar_directory
from grid.uploader import S3Uploader
from grid.uploader import UploadProgressCallback


def check_source(source: str):
    """
    Check if the source is a valid source for datastore
    """
    if source.startswith("http"):
        supported_extensions = [".zip", ".tar.gz", ".tar"]

        valid_extension = any(
            source.endswith(extension) for extension in supported_extensions)

        if valid_extension is False:
            raise ClickException(f"""
                Grid currently only supports remote files with the
                following extensions: {supported_extensions}
                """)

        # Check if url is accessible
        status = requests.head(source, allow_redirects=True)
        if status.status_code != 200:
            raise ClickException(f"Source url {source} is not reachable")
        return

    if os.path.exists(source) is False:
        raise ClickException(
            f"Source local directory path {source} doesn't exist")


def create_datastore(name: str,
                     credential_id: str,
                     client: Client,
                     remote_source_url: Optional[str] = None):
    """Create datastore in Grid"""

    # Create Grid datastore directly in Grid without uploading,
    # since Grid will handle extraction and creating a optimizted
    # datastore automatically.

    mutation = gql("""
    mutation (
        $name: String!
        $credentialId: String!
        $remoteSourceUrl: String
        ) {
        createDatastore (
            properties: {
                    name: $name
                    credentialId: $credentialId
                    remoteSourceUrl: $remoteSourceUrl
                }
        ) {
        success
        message
        datastoreId
        datastoreVersion
        }
    }
    """)

    params = {
        'name': name,
        'credentialId': credential_id,
        'remoteSourceUrl': remote_source_url
    }

    result = client.execute(mutation, variable_values=params)
    success = result['createDatastore']['success']
    message = result['createDatastore']['message']
    if not success:
        raise ValueError(f"Unable to create datastore: {message}")

    datastoreId = result['createDatastore']['datastoreId']
    datastoreVersion = int(result['createDatastore']['datastoreVersion'])

    return (datastoreId, datastoreVersion)


def create_datastore_session(name: str, source: str, credential_id: str,
                             compression: bool, client: Client):
    """Creates datastore session based on source"""
    check_source(source)

    if source.startswith("http"):
        return DatastoreRemoteUpload(name=name,
                                     source_url=source,
                                     credential_id=credential_id,
                                     client=client)

    s = DatastoreUploadSession(name=name,
                               source_dir=source,
                               credential_id=credential_id,
                               compression=compression)
    s.configure(client=client)
    return s


class InvalidDatastoreError(Exception):
    """Error that is non-recoverable when uploading datastore"""


class UnsupportedDatastoreImplementationError(Exception):
    """Error when trying to recover a non-supported datastore implementation"""


class DatastoreUploadSteps(str, Enum):
    CREATE_DATASTORE = "create_datastore"
    GET_PRESIGNED_URLS = "get_presigned_urls"
    COMPRESS_SOURCE_DIRECTORY = "compress_source_directory"
    UPLOAD_PARTS = "upload_parts"
    MARK_UPLOAD_COMPLETE = "mark_upload_complete"


class DatastoreRemoteUpload:
    """
    This class handles creating a datastore in Grid.

    Attributes
    ----------
    name: str
        Name of the datastore
    source_url: str
        Source data url
    credential_id: str
        Credential Id to map datastore to
    """
    def __init__(self, name: str, source_url: str, credential_id: str,
                 client: Client):
        self.name = name
        self.source_url = source_url
        self.credential_id = credential_id
        self.client = client
        self.logger = logging.getLogger("grid.datastore")

    def upload(self):
        spinner = yaspin.yaspin(text=f'Creating datastore {self.name}',
                                color="yellow")
        spinner.start()

        try:
            create_datastore(name=self.name,
                             credential_id=self.credential_id,
                             client=self.client,
                             remote_source_url=self.source_url)
        except Exception as e:
            spinner.text = "Failed to create datastore"
            spinner.fail("✘")
            raise e

        spinner.text = "Finished creating datastore"
        spinner.ok("✔")


@dataclass_json
@dataclass
class DatastoreUploadSession(UploadProgressCallback):
    """
    This class handles uploading datastore

    Attributes
    ----------
    name: str
        Name of the datastore
    source_dir: str
        Source directory to upload from
    credential_id: str
        Credential Id to use for uploading
    presigned_urls: Dict[int, str]
        Presigned urls retrieved from backend
    etags: Dict[int, str]
        Etags per part after uploading to cloud
    session_path: str
        Path to session files (data and state file)
    session_state_file: str
        Path to session state file
    """
    # This version is a datastore implementation version. If we change this
    # version means we no longer able to recover sessions that is not the same
    # version. This is assuming to be fine as datastore upload recovering
    # should be a optimization.
    DATASTORE_VERSION = 2
    # Path storing datastore session and compresed data
    grid_datastores_path = '.grid/datastores'

    # Datastore upload fields
    name: str
    source_dir: str
    credential_id: str

    version: int = 1
    id: str = ""
    upload_id: str = ""
    original_size: int = 0
    compressed_size: int = 0
    part_count: int = 0

    # Session state
    session_id: str = ""
    session_path: str = ""
    session_state_file: str = ""
    last_completed_step: DatastoreUploadSteps = None

    presigned_urls: Dict[int, str] = field(default_factory=dict)
    etags: Dict[int, str] = field(default_factory=dict)

    # Compression
    compression: bool = False

    def configure(self, client: Client, session_id: str = ""):
        self.client = client
        self.lock = Lock()
        self.logger = logging.getLogger("uploader.DatastoreUploadSession")
        self.spinner = None

    @staticmethod
    def recover_sessions() -> List['DatastoreUploadSession']:
        """
        Recover all upload sessions that wasn't completed, so
        user can resume them.

        Returns
        -------
        List[DatastoreUploadSession]
            List of resumable sessions
        """
        logger = logging.getLogger("DatastoreUploadSession")
        sessions = []
        session_path = str(Path.home().joinpath(
            DatastoreUploadSession.grid_datastores_path))
        session_dirs = os.listdir(session_path)
        for session_dir in session_dirs:
            session_dir = os.path.join(session_path, session_dir)
            try:
                session = DatastoreUploadSession.recover(session_dir)
                last_completed_step = session.last_completed_step
                if last_completed_step in \
                    [None, DatastoreUploadSteps.COMPRESS_SOURCE_DIRECTORY]:
                    # We choose not to resume sessions that hasn't finished getting
                    # presigned_urls, since the datastore version is only determined
                    # when that's called, and we don't know what version we're going
                    # to be resuming.
                    raise ValueError("Session not yet finished compression")

                sessions.append(session)
            except (ValueError, UnsupportedDatastoreImplementationError) as e:
                logger.warning(
                    f"Removing incomplete session {session_dir}, reason: {e}")
                shutil.rmtree(session_dir, ignore_errors=True)

        return sessions

    @staticmethod
    def recover(session_dir: str) -> "DatastoreUploadSession":
        """
        Recover session if sessions exists
        """
        session_state_file = os.path.join(session_dir, "session.json")
        if not os.path.exists(session_state_file):
            raise ValueError("Session state file does not exist")

        with open(session_state_file, "r") as f:
            content = json.load(f)
            datastore_version = 0
            if "DATASTORE_VERSION" in content:
                datastore_version = content["DATASTORE_VERSION"]
            if datastore_version != DatastoreUploadSession.DATASTORE_VERSION:
                name = content["name"]
                version = content["version"]
                session_name = f"{name}-v{version}"
                raise UnsupportedDatastoreImplementationError(
                    f"Incomplete datastore session {session_name} is no " +
                    "longer supported. Please restart this upload.")

            session = DatastoreUploadSession.from_dict(content)

        return session

    def _update_progress(self, text: str):
        """
        Update current progress

        Parameters
        ----------
        text: str
            Latest progress text
        """
        if self.spinner:
            self.spinner.text = text

    def _get_presigned_urls(self):
        """Gets presigned urls from backend"""
        if self.part_count <= 0:
            raise InvalidDatastoreError(
                f"Invalid part count calculated for datastore: {self.part_count}"
            )

        self._update_progress("Requesting presigned URLs from Grid...")

        query = gql("""
        query GetMultiPartPresignedUrls (
            $path: String!,
            $datastoreId: ID!,
            $count: Int!
        ) {
            getMultiPartPresignedUrls (
                path: $path,
                datastoreId: $datastoreId,
                count: $count
            ) {
                uploadId
                presignedUrls {
                    url
                    part
                }
            }
        }
        """)
        params = {
            'datastoreId': self.id,
            'count': self.part_count,
            # TODO: This is going to change once we implement
            # a new tarring scheme, so hardcoding the path here for now.
            'path': "data.tar.gz"
        }

        result = self.client.execute(query, variable_values=params)

        result = result['getMultiPartPresignedUrls']
        presigned_urls = result['presignedUrls']
        self.upload_id = result['uploadId']
        presigned_map = {}
        for url in presigned_urls:
            presigned_map[int(url['part'])] = url['url']

        self.presigned_urls = presigned_map

    @property
    def target_file(self) -> str:
        """Get target compressed data file"""
        return os.path.join(self.session_path, "data.tar.gz")

    def _create_datastore(self):
        self._update_progress("Creating datastore in Grid...")
        datastore_id, datastore_version = create_datastore(
            name=self.name,
            credential_id=self.credential_id,
            client=self.client)
        self.id = datastore_id
        self.version = datastore_version

    def _compress_source_directory(self):
        if self.compression:
            self._update_progress(
                f"Packaging and compressing datastore {self.name}...")
        else:
            self._update_progress(f"Packaging datastore {self.name}...")

        tar_results = tar_directory(source_dir=self.source_dir,
                                    target_file=self.target_file,
                                    compression=self.compression)

        self.original_size = tar_results.before_size
        self.compressed_size = tar_results.after_size
        split_size = get_split_size(self.compressed_size)
        self.part_count = math.ceil(self.compressed_size / split_size)

    def _create_uploader(self, presigned_urls: Dict[int, str]):
        size = self.compressed_size
        if size == 0:
            # We added compressed size later, so if a session didn't have it serialized,
            # we will look it up.
            # This is used for the progress bar only and not affect functionality.
            size = os.stat(self.target_file).st_size

        split_size = get_split_size(size)

        return S3Uploader(source_file=self.target_file,
                          presigned_urls=presigned_urls,
                          name=f"{self.name}-{self.version}",
                          split_size=split_size,
                          total_size=size,
                          progress_callback=self)

    def _upload_parts(self):
        self._update_progress(
            f"Uploading datastore {self.name} (v{self.version}) datastore" +
            " to S3...")

        # Skip uploading parts that is already uploaded.
        # This can happen if we resume an upload session.
        unuploaded_presigned_urls = {}
        for part, url in self.presigned_urls.items():
            if part not in self.etags:
                unuploaded_presigned_urls[part] = url

        uploader = self._create_uploader(
            presigned_urls=unuploaded_presigned_urls)

        # Stoping and starting the spinner, as the progress bar
        # in uploader will conflict with the spinner

        if self.spinner:
            self.spinner.stop()

        uploader.upload()

        if self.spinner:
            self.spinner.start()

    def _mark_upload_complete(self):
        self._update_progress("Completing multi-part uploads with Grid...")
        mutation = gql("""
        mutation (
            $datastoreId: ID!
            $uploadId: String!
            $parts: JSONString!
            $path: String!
            ) {
            completeMultipartDatastoreUpload (
                properties: {
                        datastoreId: $datastoreId
                        uploadId: $uploadId
                        parts: $parts
                        path: $path
                    }
            ) {
            success
            message
            }
        }
        """)

        params = {
            'datastoreId': self.id,
            'uploadId': self.upload_id,
            'parts': json.dumps(self.etags),
            'path': 'data.tar.gz'
        }

        result = self.client.execute(mutation, variable_values=params)
        success = result['completeMultipartDatastoreUpload']['success']
        message = result['completeMultipartDatastoreUpload']['message']
        if not success:
            raise ValueError(
                f"Unable to complete multi-part upload: {message}")

        self._update_progress("Completing datastore upload...")

        mutation = gql("""
        mutation (
            $datastoreId: ID!
            $sizeMib: Int!
            ) {
            completeDatastoreUpload (
                properties: {
                        datastoreId: $datastoreId
                        sizeMib: $sizeMib
                    }
            ) {
            success
            message
            }
        }
        """)

        params = {
            'datastoreId': self.id,
            'sizeMib': math.ceil(self.original_size / (1024**2))
        }

        result = self.client.execute(mutation, variable_values=params)
        success = result['completeDatastoreUpload']['success']
        message = result['completeDatastoreUpload']['message']
        if not success:
            raise ValueError(f"Unable to complete datastore upload: {message}")

    def _create_session_file(self, session_id: str):
        """
        Create session state file so we can resume upload progress.
        """
        self.session_path = os.path.join(self.grid_datastores_path, session_id)
        self.session_path = str(Path.home().joinpath(self.session_path))
        Path.home().joinpath(self.session_path).mkdir(parents=True,
                                                      exist_ok=True)
        self.session_file = os.path.join(self.session_path, "session.json")

    @property
    def session_name(self) -> str:
        return f"{self.name}-v{self.version}"

    def upload(self):
        """
        Upload completes the full datastore upload operation,
        and also records the progress of the upload, so
        it can be resumed later.
        """
        if self.session_id == "":
            self.session_id = str(uuid.uuid4())

        self._create_session_file(self.session_id)

        self.spinner = yaspin.yaspin(
            text=f'Uploading datastore {self.name} v{self.version}',
            color="yellow")
        self.spinner.start()

        steps = [(self._create_datastore,
                  DatastoreUploadSteps.CREATE_DATASTORE),
                 (self._compress_source_directory,
                  DatastoreUploadSteps.COMPRESS_SOURCE_DIRECTORY),
                 (self._get_presigned_urls,
                  DatastoreUploadSteps.GET_PRESIGNED_URLS),
                 (self._upload_parts, DatastoreUploadSteps.UPLOAD_PARTS),
                 (self._mark_upload_complete,
                  DatastoreUploadSteps.MARK_UPLOAD_COMPLETE)]

        current_step = 0
        if self.last_completed_step:
            for i, step in enumerate(steps):
                if step[1] == self.last_completed_step:
                    current_step = i + 1
                    break

            if current_step == 0:
                raise ValueError(f"Unsupported upload step: " +
                                 self.last_completed_step)

        try:
            while current_step < len(steps):
                func, step = steps[current_step]
                func()
                self.last_completed_step = step
                self._write_session()
                current_step += 1

            self._remove_session()

            self.spinner.text = "Finished uploading datastore."
            self.spinner.ok("✔")

        except InvalidDatastoreError as e:
            self.spinner.fail("✘")
            self.logger.error(f"""
            An non-recoverable error occured when uploading datastore
            {self.session_name}.

            Please try again or contact Grid for support
            """)
            raise e
        except (Exception, KeyboardInterrupt) as e:
            self.spinner.fail("✘")
            message = f"""
            Whoops, your datastore creation failed!

            To resume, run:

            grid datastores resume {self.session_name}
            """
            self.logger.error(message)
            raise e
        finally:
            self.spinner.stop()

    def upload_part_completed(self, part: int, etag: str):
        """
        Mark part uploaded

        Parameters
        ----------
        part: int
            Part number
        etag: str
            ETag returned
        """
        self.logger.debug(f"Part {part} finished uploading")
        with self.lock:
            self.etags[part] = etag
            self._write_session()

    def _write_session(self):
        """
        Writes the session state into session file
        """
        with open(self.session_file, "w") as f:
            data = self.to_dict()
            data["DATASTORE_VERSION"] = self.DATASTORE_VERSION
            json.dump(data, f)

    def _remove_session(self):
        shutil.rmtree(self.session_path, ignore_errors=True)
