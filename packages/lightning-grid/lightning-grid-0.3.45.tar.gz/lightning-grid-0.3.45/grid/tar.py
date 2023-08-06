"""
Create tar file from folder
"""
from dataclasses import dataclass
import math
import os
import subprocess
from typing import Optional, Tuple


def get_dir_size_and_count(source_dir: str,
                           prefix: Optional[str] = None) -> Tuple[int, int]:
    """
    Get size and file count of a directory

    Parameters
    ----------
    source_dir: str
        Directory path

    Returns
    -------
    Tuple[int, int]
        Size in megabytes and file count
    """
    size = 0
    count = 0
    for root, _, files in os.walk(source_dir, topdown=True):
        for f in files:
            if prefix and not f.startswith(prefix):
                continue

            full_path = os.path.join(root, f)
            size += os.path.getsize(full_path)
            count += 1

    return (size, count)


@dataclass
class TarResults:
    """
    This class holds the results of running tar_directory.

    Attributes
    ----------
    before_size: int
        The total size of the original directory files in bytes
    after_size: int
        The total size of the compressed and tarred split files in bytes
    """
    before_size: int
    after_size: int


def get_split_size(total_size: int,
                   minimum_split_size: int = 1024 * 1000 * 20,
                   max_split_count: int = 10000) -> int:
    """
    Calculate the split size we should use to split

    Parameters
    ----------
    minimum_split_size: int
        The minimum split size to use
    max_split_count: int
        The maximum split count
    total_size: int
        Total size of the file to split

    Returns
    -------
    int
        Split size
    """
    split_size = minimum_split_size
    split_count = math.ceil(total_size / split_size)
    if split_count > max_split_count:
        # Adjust the split size based on max split count
        split_size = math.ceil(total_size / max_split_count)

    return split_size


def tar_directory(source_dir: str,
                  target_file: str,
                  compression: bool = False) -> TarResults:
    """
    Create tar from directory using `tar`

    Parameters
    ----------
    source_dir: str
        Source directory
    target_file
        Target tar file
    compression: bool, default False
        Enable compression, which is disabled by
        default.

    Returns
    -------
    TarResults
        Results that holds file counts and sizes
    """
    before_size, _ = get_dir_size_and_count(source_dir)

    # Only add compression when users explicitly request it.
    # We do this because it takes too long to compress
    # large datastores.
    tar_flags = '-cvf'
    if compression:
        tar_flags = '-zcvf'

    command = f"tar -C {source_dir} {tar_flags} {target_file} ./"
    subprocess.check_call(command,
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL,
                          shell=True,
                          env={
                              "GZIP": "-9",
                              "COPYFILE_DISABLE": "1"
                          })

    after_size = os.stat(target_file).st_size
    return TarResults(before_size=before_size, after_size=after_size)
