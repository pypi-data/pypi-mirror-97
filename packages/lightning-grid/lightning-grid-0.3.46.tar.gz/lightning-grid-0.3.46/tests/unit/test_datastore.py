import json
import math
import os
from tempfile import TemporaryDirectory
from unittest.mock import MagicMock

from click.exceptions import ClickException
import pytest

from grid.datastore import check_source
from grid.datastore import create_datastore_session
from grid.datastore import DatastoreRemoteUpload
from grid.datastore import DatastoreUploadSession
from grid.datastore import DatastoreUploadSteps
from grid.datastore import requests
from grid.datastore import UnsupportedDatastoreImplementationError
import grid.datastore as datastore
from grid.tar import TarResults


class TestDatastore:
    @classmethod
    def setup_class(cls):
        datastore.gql = lambda x: x

    @staticmethod
    def test_check_source():
        with pytest.raises(ClickException):
            check_source("http://www.grid.ai/data.7z")

        with pytest.raises(ClickException):
            check_source("/not/exists")

        check_source("/usr")

    @staticmethod
    def test_datastore_recover(monkeypatch):
        with TemporaryDirectory() as tempdir:
            session = DatastoreUploadSession(name="test",
                                             source_dir="test_dir",
                                             credential_id="cc-abcdef")
            session.last_completed_step = DatastoreUploadSteps.GET_PRESIGNED_URLS
            session.session_file = os.path.join(tempdir, "session.json")
            session.presigned_urls = {
                1: "http://www.grid.ai/1",
                2: "http://www.grid.ai/2",
                3: "http://www.grid.ai/3",
                4: "http://www.grid.ai/4"
            }
            session.etags = {2: "etag2", 3: "etag3"}
            session.part_count = 4
            session._write_session()
            recovered_session = DatastoreUploadSession.recover(tempdir)
            assert session.last_completed_step == recovered_session.last_completed_step
            assert session.presigned_urls == recovered_session.presigned_urls
            assert session.part_count == recovered_session.part_count
            assert session.etags == recovered_session.etags

    @staticmethod
    def test_datastore_outdated_Version(monkeypatch):
        with TemporaryDirectory() as tempdir:
            session = DatastoreUploadSession(name="test",
                                             source_dir="test_dir",
                                             credential_id="cc-abcdef")
            session.last_completed_step = DatastoreUploadSteps.GET_PRESIGNED_URLS
            session.session_file = os.path.join(tempdir, "session.json")
            session.presigned_urls = {
                1: "http://www.grid.ai/1",
                2: "http://www.grid.ai/2",
                3: "http://www.grid.ai/3",
                4: "http://www.grid.ai/4"
            }
            session.etags = {2: "etag2", 3: "etag3"}
            session.part_count = 4
            session.DATASTORE_VERSION = 0
            session._write_session()
            with pytest.raises(UnsupportedDatastoreImplementationError):
                DatastoreUploadSession.recover(tempdir)

    @staticmethod
    def test_datastore_steps(monkeypatch):
        session = DatastoreUploadSession(name="test",
                                         source_dir="test_dir",
                                         credential_id="cc-abcdef")

        class MockS3Uploader:
            def __init__(self, session):
                self.session = session

            def upload(self):
                self.session.upload_part_completed(1, "etag1")
                self.session.upload_part_completed(2, "etag2")

        class MockClient:
            def execute(self, query, variable_values):
                if "createDatastore" in query:
                    assert variable_values == {
                        'credentialId': 'cc-abcdef',
                        'name': 'test',
                        'remoteSourceUrl': None
                    }

                    return {
                        'createDatastore': {
                            'datastoreId': 'abcde',
                            'datastoreVersion': 1,
                            'success': True,
                            'message': ''
                        }
                    }

                if "GetMultiPartPresignedUrls" in query:
                    assert variable_values == {
                        'datastoreId': 'abcde',
                        'count': 50,
                        'path': 'data.tar.gz'
                    }

                    return {
                        'getMultiPartPresignedUrls': {
                            'presignedUrls': [],
                            'uploadId': "upload1"
                        }
                    }

                if "completeMultipartDatastoreUpload" in query:
                    assert variable_values == {
                        'datastoreId': 'abcde',
                        'uploadId': 'upload1',
                        'path': 'data.tar.gz',
                        'parts': json.dumps({
                            1: "etag1",
                            2: "etag2"
                        })
                    }

                    return {
                        'completeMultipartDatastoreUpload': {
                            'success': True,
                            'message': ''
                        }
                    }

                if "completeDatastoreUpload" in query:
                    assert variable_values == {
                        'sizeMib': math.ceil((1024 * 1000 * 1000) / (1024**2)),
                        'datastoreId': 'abcde'
                    }

                    return {
                        'completeDatastoreUpload': {
                            'success': True,
                            'message': ''
                        }
                    }

                raise ValueError(f"Unexpected query {query}")

        client = MockClient()
        session.configure(client=client)

        def tar_directory(**kwargs):
            return TarResults(before_size=1024 * 1000 * 1000,
                              after_size=1024 * 1000 * 1000)

        def create_uploader(presigned_urls):
            return MockS3Uploader(session)

        monkeypatch.setattr('grid.datastore.tar_directory', tar_directory)
        monkeypatch.setattr(session, '_create_uploader', create_uploader)

        session.upload()

    def test_remote_datastore_url(self, monkeypatch):
        def mock_head(*args, **kwargs):
            request_mock = MagicMock()
            request_mock.status_code = 200
            request_mock.headers = {'Content-Length': 1024 * 1024 * 10}
            return request_mock

        monkeypatch.setattr(requests, 'head', mock_head)

        class MockClient:
            def execute(self, query, variable_values):
                if "createDatastore" in query:
                    assert variable_values == {
                        'credentialId': 'cc-abcdef',
                        'name': 'test-remote',
                        'remoteSourceUrl': "http://www.grid.ai/data.zip"
                    }

                    return {
                        'createDatastore': {
                            'datastoreId': 'abcde',
                            'datastoreVersion': 1,
                            'success': True,
                            'message': ''
                        }
                    }

                raise ValueError(f"Unexpected query {query}")

        client = MockClient()
        remote_session = create_datastore_session(
            name="test-remote",
            source="http://www.grid.ai/data.zip",
            credential_id="cc-abcdef",
            client=client,
            compression=False)

        assert isinstance(remote_session, DatastoreRemoteUpload)
        remote_session.upload()
