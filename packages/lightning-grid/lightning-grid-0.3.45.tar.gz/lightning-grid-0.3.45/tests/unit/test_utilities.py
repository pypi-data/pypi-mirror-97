from datetime import datetime
from datetime import timedelta
from datetime import timezone
import os
from pathlib import Path
import random
import unittest

import click
from dateutil.parser import parse as date_string_parse
import pytest

from grid.utilities import check_description_isnt_too_long
from grid.utilities import check_environment_variables
from grid.utilities import check_is_python_script
from grid.utilities import check_run_name_is_valid
from grid.utilities import convert_utc_string_to_local_datetime
from grid.utilities import get_abs_time_difference
from grid.utilities import get_experiment_duration_string
from grid.utilities import get_graphql_url
from grid.utilities import get_param_values
from grid.utilities import install_autocomplete
from grid.utilities import introspect_module
from grid.utilities import is_experiment
from grid.utilities import string_format_timedelta


def test_check_is_python_script():
    class Context:
        params = {}

    script = 'script.py'
    assert check_is_python_script(Context, None, script) == script

    bad_script = 'script.cpp'
    with pytest.raises(click.BadParameter):
        check_is_python_script(None, None, bad_script)


def test_check_run_name_is_valid():
    valid_run_name = 'run-test'
    assert check_run_name_is_valid(None, None,
                                   valid_run_name) == valid_run_name

    invalid_run_name_a = 'run name'
    with pytest.raises(click.BadParameter):
        check_run_name_is_valid(None, None, invalid_run_name_a)

    invalid_run_name_b = 'run-name-'
    with pytest.raises(click.BadParameter):
        check_run_name_is_valid(None, None, invalid_run_name_b)

    invalid_run_name_c = 'Run-Name'
    with pytest.raises(click.BadParameter):
        check_run_name_is_valid(None, None, invalid_run_name_c)


def test_check_run_name_raises_exception_if_experiment():
    experiment_name = 'run-test-exp0'
    with pytest.raises(click.BadParameter):
        check_run_name_is_valid(None, None, experiment_name)


def test_check_description_isnt_too_long():
    """
    _check_description_isnt_too_long() checks that description isn't
    too long
    """
    d = 'a' * 199
    assert d == check_description_isnt_too_long(None, None, d)

    d = 'a' * 201
    with pytest.raises(click.BadParameter):
        check_description_isnt_too_long(None, None, d)


def test_install_autocomplete(mocker, tmpdir):
    mocker.patch("pathlib.Path.home", return_value=Path(tmpdir))
    home = Path.home()
    (home / ".bashrc").write_text("")
    (home / ".zshrc").write_text("")
    install_autocomplete()
    assert (Path.home() / ".grid/autocomplete/complete.zsh").exists()
    assert (Path.home() / ".grid/autocomplete/complete.bash").exists()
    assert (home / ".bashrc").read_text().count("grid") == 2
    assert (home / ".zshrc").read_text().count("grid") == 2

    # make sure we are not writing more than once
    install_autocomplete()
    assert (home / ".bashrc").read_text().count("grid") == 2
    assert (home / ".zshrc").read_text().count("grid") == 2


class UtilitiesTestCase(unittest.TestCase):
    """Test utilities in credentials."""
    def test_convert_utc_string_to_local_datetime(self):
        date_string = "2016-08-29T16:02:54.884Z"
        date_date = convert_utc_string_to_local_datetime(date_string)
        assert isinstance(date_date, datetime)

    def test_get_abs_time_difference(self):
        date_time_now = datetime.now()
        date_a = date_time_now - timedelta(hours=1)
        date_b = date_time_now
        result = get_abs_time_difference(date_1=date_a, date_2=date_b)
        inverse_result = get_abs_time_difference(date_1=date_b, date_2=date_a)
        assert isinstance(result, timedelta)
        assert int(result.total_seconds()) == 60 * 60
        assert int(inverse_result.total_seconds()) == 60 * 60

    def test_conversion_with_time_difference_now(self):
        finished_at = datetime.now(timezone.utc)
        created_at = date_string_parse('2020-05-16T21:21:10.745898+00:00')
        delta = get_abs_time_difference(finished_at, created_at)
        assert isinstance(delta, timedelta)

    def test_string_formating_duration(self):
        a = datetime.now()
        b = datetime.now() - timedelta(hours=1)
        c = a - b

        result = string_format_timedelta(c)
        assert result == '0d-00:59:59'

    def test_environment_variables(self):
        var = '_TEST_VAR'

        #  Checks that the env var isn't set.
        assert not os.getenv(var)

        #  Tests that function raises error.
        with pytest.raises(ValueError):
            check_environment_variables(variables=[var])

        #  Tests that it doesn't raise an error
        #  if variable is set.
        os.environ[var] = 'foo'
        assert check_environment_variables(variables=[var])

    def test_introspect_module(self):
        #  Creates a class that represents the same
        #  module mechanics: it includes the __all__
        #  attribute that has a string reference to
        #  a class property (test).
        class M:
            @staticmethod
            def test():
                return True

            __all__ = ['test']

        #  Let's that the generator returns
        #  the defined method.
        for func in introspect_module(M):
            assert isinstance(func, staticmethod)

    def test_is_experiment(self):
        run_a = 'test-run-1'
        result_a = is_experiment(run_a)
        assert not result_a

        run_b = 'test-run-1-exp1'
        result_b = is_experiment(run_b)
        assert result_b

        run_c = 'test-run-1-exp1-foo'
        result_c = is_experiment(run_c)
        assert not result_c

    def test_is_experiment_many_ints(self):
        """is_experiment() returns true if experiment has many int digits."""

        for _ in range(10):
            digit = random.randint(10, 10000)
            run = f'test-run-1-exp{digit}'
            assert is_experiment(run)

    def test_get_param_vals(self):
        command = "command.py --flag1 val1 --flag2 --flag3 val3 --flag4"
        assert get_param_values(command) == ['val1', "True", "val3", "True"]

    def test_get_experiment_duration_string(self):
        created_at = str(datetime.now(timezone.utc) - timedelta(hours=3))
        started_running_at = str(
            datetime.now(timezone.utc) - timedelta(hours=2))
        finished_at = str(datetime.now(timezone.utc) - timedelta(hours=1))
        experiment_queued_result = get_experiment_duration_string(
            created_at=created_at, started_running_at=None, finished_at=None)
        assert experiment_queued_result >= f"{0}d-{3:02d}:{0:02d}:{0:02d}"
        assert experiment_queued_result < f"{0}d-{3:02d}:{1:02d}:{0:02d}"
        experiment_running_result = get_experiment_duration_string(
            created_at=created_at,
            started_running_at=started_running_at,
            finished_at=None)
        assert experiment_running_result >= f"{0}d-{2:02d}:{0:02d}:{0:02d}"
        assert experiment_running_result < f"{0}d-{2:02d}:{1:02d}:{0:02d}"
        experiment_finished_result = get_experiment_duration_string(
            created_at=created_at,
            started_running_at=started_running_at,
            finished_at=finished_at)
        assert experiment_finished_result >= f"{0}d-{1:02d}:{0:02d}:{0:02d}"
        assert experiment_finished_result < f"{0}d-{1:02d}:{1:02d}:{0:02d}"

    @staticmethod
    def test_get_graphql_url():
        url_with_graphql = 'http://localhost:8000/graphql'
        url_without_graphql = 'http://localhost:8000'
        assert get_graphql_url(
            url_without_graphql) == 'http://localhost:8000/graphql'
        assert get_graphql_url(
            url_with_graphql) == 'http://localhost:8000/graphql'
