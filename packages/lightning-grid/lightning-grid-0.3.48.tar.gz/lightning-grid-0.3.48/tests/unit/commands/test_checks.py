import click
from click.exceptions import ClickException
import pytest

import grid.commands.checks as checks


def monkey_patch_click(*args, **kwargs):
    pass


def test_check_if_uncommited_files(monkeypatch):
    """
    Grid._check_if_uncommited_files() shows prompts if uncommited
    files are found
    """
    def monkey_pach_git_command(*args, **kwargs):
        return 'test_0.txt: needs update\ntest_1.txt: needs update'

    monkeypatch.setattr(checks, 'execute_git_command', monkey_pach_git_command)
    monkeypatch.setattr(click, 'confirm', monkey_patch_click)

    # Make sure that we are not ignoring warnings.
    checks.env.IGNORE_WARNINGS = False
    result = checks.WorkflowChecksMixin._check_if_uncommited_files()
    assert result == True

    _ignore = checks.env.IGNORE_WARNINGS
    checks.env.IGNORE_WARNINGS = True
    result = checks.WorkflowChecksMixin._check_if_uncommited_files()
    assert result == False

    checks.env.IGNORE_WARNINGS = _ignore


def test_check_if_remote_head_is_different(mocker, monkeypatch):
    """
    _check_if_remote_head_is_different() checks if remote SHA is
    different than local
    """
    def monkey_patch_git_command_fatal(*args, **kwargs):
        return 'fatal'

    monkeypatch.setattr(checks, 'execute_git_command',
                        monkey_patch_git_command_fatal)
    assert checks.WorkflowChecksMixin._check_if_remote_head_is_different(
    ) is None

    def monkey_patch_git_command_same(*args, **kwargs):
        return 'foo'

    monkeypatch.setattr(checks, 'execute_git_command',
                        monkey_patch_git_command_same)
    assert checks.WorkflowChecksMixin._check_if_remote_head_is_different(
    ) == False


def test_check_if_remote_head_is_different_shows_warning(mocker, monkeypatch):
    """
    _check_if_remote_head_is_different() shows warning if SHAs are different
    """
    def mp_git_command(*args, **kwargs):
        if r"@{u}" in args[0] or 'merge-base' in args[0]:
            return 'test-0'
        return 'test-1'

    def mp_confirm(*args, **kwargs):
        pass

    monkeypatch.setattr(click, 'confirm', mp_confirm)
    mocker.patch('click.confirm')
    monkeypatch.setattr(checks, 'execute_git_command', mp_git_command)

    result = checks.WorkflowChecksMixin._check_if_remote_head_is_different()
    assert result is True

    click.confirm.assert_called_once()


def test_check_github_repository(monkeypatch):
    """_check_github_repository() checks that we are in a git repository"""
    def mp_git_command_fatal(*args, **kwargs):
        return 'mygit.company.com'

    monkeypatch.setattr(checks, 'execute_git_command', mp_git_command_fatal)
    with pytest.raises(ClickException):
        checks.WorkflowChecksMixin._check_github_repository()

    def mp_git_command_fatal(*args, **kwargs):
        return None

    monkeypatch.setattr(checks, 'execute_git_command', mp_git_command_fatal)
    with pytest.raises(ClickException):
        checks.WorkflowChecksMixin._check_github_repository()
