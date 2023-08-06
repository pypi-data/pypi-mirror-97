from grid.commands.git import execute_git_command


def test_execute_git_command():
    """execute_git_command() executes a git command."""
    result = execute_git_command(['version'])
    assert 'git version' in result
