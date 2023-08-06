from pathlib import Path
import shutil

from grid.downloader import DownloadableObject
from grid.downloader import Downloader


class TestArtifactCallbacks:
    """Tests callbacks in grid artifacts."""
    @classmethod
    def clean_test_directory(cls):
        path = Path(cls.test_dir)
        shutil.rmtree(path, ignore_errors=True)

    @classmethod
    def setup_class(cls):
        cls.test_dir = 'tests/data/download_path/nested_dir'
        cls.clean_test_directory()

    @classmethod
    def teardown_class(cls):
        # Deletes test directory with all files.
        cls.clean_test_directory()

    def test_downloader_creates_dir(self):
        """Downloader.create_dir_tree creates dir structure in path."""
        Downloader.create_dir_tree(self.test_dir)
        assert Path(self.test_dir).exists()

    def test_downloader_downloads_data(self):
        """Downloader().download() downloads data in nested directories."""
        # Google logo
        # skipcq: FLK-E501
        url = 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png'
        directory_path = 'nested_0/nested_1'
        filename = 'test-filename.png'
        objects = [
            DownloadableObject(url=url,
                               download_path=directory_path,
                               filename=filename)
        ]

        # Download file
        D = Downloader(downloadable_objects=objects, base_dir=self.test_dir)
        assert D.download()

        # Test that file as been downloaded.
        assert Path(self.test_dir).joinpath(directory_path).joinpath(
            filename).exists()
