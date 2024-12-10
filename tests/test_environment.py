"""
Contains tests of the environment module.
"""

from chktex_action.environment import Environment


def test_environment() -> None:
    """
    Tests the access to the environment variables.
    """

    # Actual
    env = Environment()

    # Assertions
    assert env.get_workspace() == "/home/github/"
    assert env.get_token() == "123456789"
    assert env.get_event_path() == "/home/event/"
    assert env.get_repository() == "j2kun/chktex-action"
    assert env.is_lint_all()
    assert env.get_step_summary() == "/home/step-summary.md"
    assert env.get_ref() == "da39a3ee5e6b4b0d3255bfef95601890afd80709"
    assert env.is_push()
