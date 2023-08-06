"""
Uploader that uploads files into Cloud storage
"""

from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, IO, List

import requests
from requests.adapters import HTTPAdapter
from rich.progress import BarColumn
from rich.progress import DownloadColumn
from rich.progress import Progress
from rich.progress import TextColumn
from urllib3.util.retry import Retry


class UploadProgressCallback:
    """
    This class provides a interface for notifying upload progress
    """
    @staticmethod
    def upload_part_completed(part: int, etag: str):
        return NotImplemented


class S3Uploader:
    """
    This class uploads a source file with presigned urls to S3

    Attributes
    ----------
    source_file: str
        Source file to upload
    presigned_urls: Dict[int, str]
        Presigned urls dictionary, with key as part number and values as urls
    workers: int
        Amount of workers to upload parts
    retries: int
        Amount of retries when requests encounters an error
    total_size: int
        Size of all files to upload
    name: str
        Name of this upload to display progress
    progress_callback: UploadProgressCallback
        Callback for notifying upload progress
    """
    workers: int = 8
    retries: int = 10

    progress = Progress(
        TextColumn("[bold blue]{task.description}", justify="left"),
        BarColumn(bar_width=None),
        "[self.progress.percentage]{task.percentage:>3.1f}%")

    def __init__(self,
                 presigned_urls: Dict[int, str],
                 source_file: str,
                 total_size: int,
                 split_size: int,
                 name: str,
                 progress_callback: UploadProgressCallback = None):
        self.presigned_urls = presigned_urls
        self.source_file = source_file
        self.total_size = total_size
        self.split_size = split_size
        self.name = name
        self.progress_callback = progress_callback

    @staticmethod
    def upload_s3_data(url: str, data: bytes, retries: int) -> str:
        """
        Send data to s3 url

        Parameters
        ----------
        url: str
            S3 url string to send data to
        data: bytes
             Bytes of data to send to S3
        retries: int
            Amount of retries

        Returns
        -------
        str
            ETag from response
        """
        s = requests.Session()
        retries = Retry(total=retries, status_forcelist=[500, 502, 503, 504])
        s.mount('http://', HTTPAdapter(max_retries=retries))
        response = s.put(url, data=data)
        if 'ETag' not in response.headers:
            raise ValueError(
                f"Unexpected response from S3, response: {response.content}")

        return response.headers['ETag']

    def _upload_part(self, url: str, part_path: str, part: int,
                     task_id: str) -> None:
        """
        Upload part of the data file with presigned url

        Parameters
        ----------
        url: str
            Presigned url to upload to S3
        part_path: str
            Path to part file
        part: int
            Part number
        task_id: str
            Task id for tracking progress
        """
        with open(part_path, 'rb') as f:
            pos = self.split_size * (part - 1)
            f.seek(pos)
            data = f.read(self.split_size)

        etag = self.upload_s3_data(url, data, self.retries)
        self.progress.update(task_id, advance=len(data))
        if self.progress_callback:
            self.progress_callback.upload_part_completed(part=part, etag=etag)

    def upload(self) -> None:
        """
        Upload files from source dir into target path in S3
        """
        task_id = self.progress.add_task("upload",
                                         filename=self.name,
                                         total=self.total_size)
        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            try:
                self.progress.start()
                futures = []
                for part, url in self.presigned_urls.items():
                    f = pool.submit(self._upload_part, url, self.source_file,
                                    part, task_id)
                    futures.append(f)

                    for future in as_completed(futures):
                        future.result()
            finally:
                self.progress.stop()
