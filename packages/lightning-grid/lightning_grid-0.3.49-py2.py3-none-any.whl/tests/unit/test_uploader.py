import os
import tempfile

from grid.uploader import S3Uploader
from grid.uploader import UploadProgressCallback


def test_s3_uploader():
    with tempfile.TemporaryDirectory() as tmpdir:
        data = {
            "aa": os.urandom(256),
            "ab": os.urandom(256),
            "ac": os.urandom(256),
            "ad": os.urandom(256)
        }
        keys = list(data.keys())
        keys.sort()
        with open(os.path.join(tmpdir, "data.tar.gz"), "wb") as f:
            for k in keys:
                f.write(data[k])

        urls = {
            1: "http://grid.ai/1",
            2: "http://grid.ai/2",
            3: "http://grid.ai/3",
            4: "http://grid.ai/4"
        }

        reverse_keys = {"aa": 1, "ab": 2, "ac": 3, "ad": 4}

        def mock_upload_data(url, part_data, _):
            found_key = None
            for k, d in data.items():
                if part_data == d:
                    found_key = k
                    break

            assert found_key
            part = reverse_keys[found_key]
            assert urls[part] == url
            return str(part)

        class MockProgressUpdater(UploadProgressCallback):
            def __init__(self):
                self.etags = {}

            def upload_part_completed(self, part: int, etag: str):
                self.etags[part] = etag

        updater = MockProgressUpdater()
        uploader = S3Uploader(source_file=os.path.join(tmpdir, "data.tar.gz"),
                              presigned_urls=urls,
                              progress_callback=updater,
                              name="test",
                              total_size=256 * 4,
                              split_size=256)

        uploader.upload_s3_data = mock_upload_data

        uploader.upload()
        assert updater.etags == {1: "1", 2: "2", 3: "3", 4: "4"}
