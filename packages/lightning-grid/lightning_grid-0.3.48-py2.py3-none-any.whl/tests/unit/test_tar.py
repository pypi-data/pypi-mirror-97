import math
import os
import tarfile
import tempfile

from grid.tar import get_dir_size_and_count
from grid.tar import get_split_size
from grid.tar import tar_directory


class TestTar:
    @staticmethod
    def test_get_dir_size_and_count():
        sizes = [1024 * 512, 1024 * 1024 * 5]

        for size in sizes:
            with tempfile.TemporaryDirectory() as temp_dir:
                data = os.urandom(size)
                with open(os.path.join(temp_dir, "a"), "wb") as f:
                    f.write(data)
                with open(os.path.join(temp_dir, "b"), "wb") as f:
                    f.write(data)
                assert get_dir_size_and_count(temp_dir, "a") == (size, 1)

    @staticmethod
    def test_tar_directory():
        with tempfile.TemporaryDirectory() as temp_dir:
            source_dir = os.path.join(temp_dir, "source")
            inner_dir = os.path.join(source_dir, "dir")
            os.makedirs(inner_dir)
            with open(os.path.join(source_dir, "f1"), 'w') as f:
                f.write("f1")

            with open(os.path.join(inner_dir, "f2"), 'w') as f:
                f.write("f2")

            target_file = os.path.join(temp_dir, "target.tar.gz")
            results = tar_directory(source_dir=source_dir,
                                    target_file=target_file)
            assert results.before_size > 0
            assert results.after_size > 0

            verify_dir = os.path.join(temp_dir, "verify")
            os.makedirs(verify_dir)
            with tarfile.open(target_file) as target_tar:
                target_tar.extractall(verify_dir)

            assert os.path.exists(os.path.join(verify_dir, "f1"))
            assert os.path.exists(os.path.join(verify_dir, "dir", "f2"))

    @staticmethod
    def test_get_split_size():
        split_size = get_split_size(minimum_split_size=1024 * 1000 * 10,
                                    max_split_count=10000,
                                    total_size=200000000001)

        # We shouldn't go over the max split count
        assert math.ceil(200000000001 / split_size) <= 10000

        split_size = get_split_size(minimum_split_size=1024 * 1000 * 10,
                                    max_split_count=10000,
                                    total_size=1024 * 500 * 1000 * 10)

        assert split_size == 1024 * 1000 * 10

    @staticmethod
    def test_tar_directory_no_compression():
        with tempfile.TemporaryDirectory() as temp_dir:
            source_dir = os.path.join(temp_dir, "source")
            inner_dir = os.path.join(source_dir, "dir")
            os.makedirs(inner_dir)
            with open(os.path.join(source_dir, "f1"), 'w') as f:
                f.write("f1")

            with open(os.path.join(inner_dir, "f2"), 'w') as f:
                f.write("f2")

            target_file = os.path.join(temp_dir, "target.tar.gz")
            tar_directory(source_dir=source_dir,
                          target_file=target_file,
                          compression=False)

            verify_dir = os.path.join(temp_dir, "verify")
            os.makedirs(verify_dir)
            with tarfile.open(target_file) as target_tar:
                target_tar.extractall(verify_dir)

            assert os.path.exists(os.path.join(verify_dir, "f1"))
            assert os.path.exists(os.path.join(verify_dir, "dir", "f2"))
