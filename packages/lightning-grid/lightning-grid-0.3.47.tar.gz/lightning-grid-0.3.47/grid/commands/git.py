import subprocess
from typing import List


def execute_git_command(args: List[str]) -> str:
    """
    Executes a git command. This is expected to return a
    single string back.

    Returns
    -------
    output: str
        String combining stdout and stderr.
    """
    process = subprocess.run(['git'] + args,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             universal_newlines=True,
                             check=False)

    output = process.stdout.strip() + process.stderr.strip()
    return output
