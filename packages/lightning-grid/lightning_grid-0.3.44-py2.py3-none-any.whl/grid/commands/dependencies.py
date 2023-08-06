import os
from typing import Dict

import click

from grid.commands.git import execute_git_command
from grid.dependency_manager import CondaManager
from grid.dependency_manager import PipManager
import grid.globals as env

# TODO: Custom requirement files from user
PIP_REQUIREMENTS_FILE = "requirements.txt"
CONDA_REQUIREMENTS_FILE = "environment.yml"


class DependencyMixin:
    def _serialize_dependencies(self, config: Dict):
        """
        Serialize dependency information to the corresponding source.

        Write python dependencies to the corresponding dependency listing
        (requirements.txt or environment.yml) and system dependencies to
        grid config (config.yml). Both write operations are actually offloaded
        downstream to the dependency manager object. Also fetches warnings
        from the dependency manager and echo to the user's terminal

        config:
            Grid config either read from the file provided by the user or the
            default generated one
        """
        self._deps_manager.write_spec()
        self._deps_manager.write_config(config)
        raise click.Abort()

    def _check_dependency_listing(self):
        """
        Evaluate if dependency listing is correct or not

        Determines the package manager employed by the user to specify
        application dependencies, setting up the appropriate interaction
        classes used to query one of the various package managers available
        as the system resolves dependency versions. Should no requirement file
        exist which specifies needed libraries+versions, this method provides
        the logic through which users are asked to select how they would like
        to proceed - automatic heuristic based generation or manual.

        Returns
        -------
        Return False if training can be continued, True if changes needs to be made
        """
        if env.IGNORE_WARNINGS:
            return False

        warning_str = click.style('WARNING', fg='yellow')
        docs_str = click.style('https://docs.grid.ai', fg='blue')
        conda_env = os.getenv("CONDA_DEFAULT_ENV")
        repo_root = execute_git_command(['rev-parse', '--show-toplevel'])
        # Assuming the requirements file is always at the repo root
        files = os.listdir(repo_root)

        if CONDA_REQUIREMENTS_FILE in files:
            if PIP_REQUIREMENTS_FILE in files:  # skipcq: PYL-R1705
                click.echo(
                    f"{warning_str} Found both {CONDA_REQUIREMENTS_FILE} "
                    f"and {PIP_REQUIREMENTS_FILE}. Delete one of them if"
                    "you need us to run the dependency check. Ignoring for now"
                )
                return False
            else:
                manager_class = CondaManager
        elif PIP_REQUIREMENTS_FILE in files:
            manager_class = PipManager
        elif conda_env:
            manager_class = CondaManager
        else:
            manager_class = PipManager

        # Returning False in-case of exceptions
        try:
            self._deps_manager = manager_class()
        except Exception as e:
            message = f"""

        {warning_str}

        We have encountered error while checking dependencies and dependency
        listing files (requirements.txt or environment.yml). Reach out to Grid
        Support at support@grid.ai with the error message below if you have
        questions

        "{e}"

        You can use the flag --ignore_warnings to skip this warning.
        See details at: {docs_str}

        Do you want to ignore the error and continue?
        """
            click.confirm(message, abort=True)
            return False

        # Returning if we find packages those are not specified in the
        # requirement listing or installed in the current environment
        missing = "\n        ".join(self._deps_manager.get_missing())
        if missing and not env.IGNORE_WARNINGS:
            message = f"""

        {warning_str}

        We found below packages being used in the source code but it is neither
        in your requirement listing (requirements.txt or environment.yml) nor
        installed in your current active environment.

        {missing}

        You can use the flag --ignore_warnings to skip this warning.
        See details at: {docs_str}

        Do you want to continue?
        """

            click.confirm(message, abort=True)
            return False  # returning if user continues

        message = f"""

        {warning_str}

        Listing of dependencies (requirements.txt or environment.yml) is
        incomplete/unavailable. This might lead to errors when running an Experiment
        in Grid. We can generate the dependency files for you by analysing your
        environment and source code. However, you'd still need to verify the files,
        commit and push it to your repository manually.

        Choose from below to continue

        [1] Generate dependency files and quit me from training
        [2] I don't care. Continue to train
        [3] Let me handle it. Exit!

        You can use the flag --ignore_warnings to skip this warning.
        See details at: {docs_str}

        """
        user_choice = "2"  # Ignore and continue to train
        if self._deps_manager.has_change:
            valid_choices = click.Choice(("1", "2", "3"))
            user_choice = click.prompt(message,
                                       show_default=False,
                                       default="1",
                                       type=valid_choices)
        if user_choice == "3":  # Ignore and exit
            raise click.Abort()
        # True if user decides to change deps and exit
        return True if user_choice == "1" else False  # skipcq: PYL-R1719
