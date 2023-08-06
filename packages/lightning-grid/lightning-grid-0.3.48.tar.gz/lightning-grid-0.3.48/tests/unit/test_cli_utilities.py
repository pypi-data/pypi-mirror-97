import click
import pytest

from grid.cli.utilities import validate_config
from grid.cli.utilities import validate_disk_size_callback


def test_validate_config_raises_exception():
    """validate_config() raises exception when disk size too small."""
    config = {'compute': {'train': {'disk_size': 10}}}
    with pytest.raises(click.ClickException):
        validate_config(cfg=config)


def test_validate_disk_size_callback_raises_exception():
    """validate_disk_size_callback() raises exception when value too low."""
    with pytest.raises(click.BadParameter):
        validate_disk_size_callback(None, None, 40)


def test_validate_disk_size_callback():
    """validate_disk_size_callback() returns value if correct."""
    expected = 200
    result = validate_disk_size_callback(None, None, expected)
    assert result == expected
