import os

import click
import pytest

from grid.commands import dependencies


class DependencyManager:
    has_change = True
    write_spec = lambda self: "Mock warning from test!"  # NOQA
    get_missing = lambda self: []  # NOQA


def get_click_confirm(holder):
    def click_confirm(message, *args, **kwargs):
        holder.clear()
        holder.append(message)
        raise click.Abort()

    return click_confirm


def test_check_dependency_spec_if_missing(monkeypatch):
    monkeypatch.setattr(DependencyManager, "get_missing",
                        lambda self: ["fake-package"])
    monkeypatch.setattr(dependencies, "PipManager", DependencyManager)
    output = []
    monkeypatch.setattr(dependencies.click, "confirm",
                        get_click_confirm(output))
    obj = dependencies.DependencyMixin()
    with pytest.raises(click.exceptions.Abort):
        obj._check_dependency_listing()
    assert "fake-package" in " ".join(output)


def test_check_dependency_spec_user_choice(monkeypatch):
    monkeypatch.setattr(dependencies, 'execute_git_command',
                        lambda *args, **kwargs: "")
    monkeypatch.setattr(os, "listdir", lambda p: ["requirements.txt"])

    monkeypatch.setattr(dependencies, "PipManager", DependencyManager)

    # Exit training and generate dependency files
    monkeypatch.setattr(click, "prompt", lambda *args, **kwargs: "1")
    obj = dependencies.DependencyMixin()
    assert obj._check_dependency_listing() is True

    # Ignore and continue to train
    monkeypatch.setattr(click, "prompt", lambda *args, **kwargs: "2")
    assert dependencies.DependencyMixin()._check_dependency_listing() is False

    # Ignore and exit
    monkeypatch.setattr(click, "prompt", lambda *args, **kwargs: "3")
    with pytest.raises(click.exceptions.Abort):
        dependencies.DependencyMixin()._check_dependency_listing()

    # No change in requirement file
    DependencyManager.has_change = False
    assert dependencies.DependencyMixin()._check_dependency_listing() is False


def test_package_manager_selection(monkeypatch):
    monkeypatch.setattr(dependencies, 'execute_git_command',
                        lambda *args, **kwargs: "")

    def mock_init(self):
        self.get_missing = lambda: []

    monkeypatch.setattr(dependencies.PipManager, "__init__", mock_init)
    monkeypatch.setattr(dependencies.PipManager, "has_change", False)
    monkeypatch.setattr(dependencies.CondaManager, "__init__", mock_init)
    monkeypatch.setattr(dependencies.CondaManager, "has_change", False)

    with monkeypatch.context() as mp:
        mp.setattr(os, "listdir", lambda p: ["requirements.txt"])
        obj = dependencies.DependencyMixin()
        obj._check_dependency_listing()
        assert isinstance(obj._deps_manager, dependencies.PipManager)

    with monkeypatch.context() as mp:
        mp.setattr(os, "listdir", lambda p: ["environment.yml"])
        obj = dependencies.DependencyMixin()
        obj._check_dependency_listing()
        assert isinstance(obj._deps_manager, dependencies.CondaManager)

    with monkeypatch.context() as mp:
        mp.setattr(os, "listdir", lambda p: [])
        obj = dependencies.DependencyMixin()
        obj._check_dependency_listing()
        assert isinstance(obj._deps_manager, dependencies.PipManager)

    with monkeypatch.context() as mp:
        mp.setattr(os, "listdir", lambda p: [])
        mp.setenv("CONDA_DEFAULT_ENV", "fake_conda_env")
        obj = dependencies.DependencyMixin()
        obj._check_dependency_listing()
        assert isinstance(obj._deps_manager, dependencies.CondaManager)


def test_if_both_pipfile_and_condafile(monkeypatch):
    monkeypatch.setattr(os, "listdir",
                        lambda p: ["environment.yml", "requirements.txt"])
    obj = dependencies.DependencyMixin()
    assert obj._check_dependency_listing() is False
