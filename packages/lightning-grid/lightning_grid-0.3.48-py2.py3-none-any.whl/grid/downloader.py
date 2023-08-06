"""
Adapted from rich's example at:

    * https://github.com/willmcgugan/rich/blob/master/examples/downloader.py
"""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import partial
import os.path
from pathlib import Path
from typing import List, Optional
from urllib.request import urlopen

from rich.progress import BarColumn
from rich.progress import DownloadColumn
from rich.progress import Progress
from rich.progress import TaskID
from rich.progress import TextColumn
from rich.progress import TimeRemainingColumn
from rich.progress import TransferSpeedColumn


@dataclass
class DownloadableObject:
    """Object that can be downloaded from an URL into a local path."""
    url: str
    download_path: str
    filename: str


class Downloader:
    """
    Downloads multiple files into their respective location
    using background threads.

    Attributes
    ----------
    workers: int
        Number of background threads to use.
    progress: Progress
        Instance of a Progress bar object.
    Parameters
    ----------
    urls: List[DownloadableObject]
        List of URL objects containing.
    """
    workers: int = 4

    # Creates the layout for a progress bar.
    progress = Progress(
        TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
        BarColumn(bar_width=None),
        "[self.progress.percentage]{task.percentage:>3.1f}%", "•",
        DownloadColumn(), "•", TransferSpeedColumn(), "•",
        TimeRemainingColumn())

    def __init__(self, downloadable_objects: List[DownloadableObject],
                 base_dir: str):
        self.downloadable_objects = downloadable_objects
        self.base_dir = base_dir

    def _get_file(self, task_id: TaskID, url: str, path: str) -> None:
        """Copy data from a url to a local file."""
        # skipcq: BAN-B310
        response = urlopen(url)

        # This will break if the response doesn't contain content length
        self.progress.update(task_id,
                             total=int(response.info()['Content-length']))
        with open(path, 'wb') as dest_file:
            self.progress.start_task(task_id)
            for data in iter(partial(response.read, 32768), b''):
                dest_file.write(data)
                self.progress.update(task_id, advance=len(data))

    @staticmethod
    def create_dir_tree(dest_dir: str, base_dir: Optional[str] = None) -> None:
        """
        Creates directory structure for downloading file.

        Parameters
        ----------
        dest_dir: str
            Destination directory for where to download file.
        base_dir: str
            Base directory to place all targer directories into.
        """
        if base_dir:
            P = Path(base_dir) / Path(dest_dir)
        else:
            P = Path(dest_dir)

        P.mkdir(parents=True, exist_ok=True)

    def download(self):
        """
        Download multuple files to the given directory. This will download
        files using a ThreadPoolExecutor so that multiple files can
        be downloaded concurrently. We can set the concurrency level
        by changing the class' workers` attribute.
        """
        with self.progress:
            with ThreadPoolExecutor(max_workers=self.workers) as pool:
                for file_to_download in self.downloadable_objects:
                    Downloader.create_dir_tree(file_to_download.download_path,
                                               self.base_dir)
                    dest_path = os.path.join(self.base_dir,
                                             file_to_download.download_path,
                                             file_to_download.filename)
                    task_id = self.progress.add_task(
                        'download',
                        filename=file_to_download.filename,
                        start=False)
                    pool.submit(self._get_file, task_id, file_to_download.url,
                                dest_path)

        return True
