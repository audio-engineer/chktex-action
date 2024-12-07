""""""

from chktex_action.environment import Environment


def test_environment() -> None:
    """"""

    env = Environment()

    assert env.github_workspace == "/home/github/"
    assert env.github_token == "123456789"
    assert env.github_event_path == "/home/event/"
    assert env.github_repository == "j2kun/chktex-action"
    assert env.github_event_name == "push"
    assert env.lint_all
    assert env.step_summary == "/home/step-summary.md"
    assert env.head_ref == "da39a3ee5e6b4b0d3255bfef95601890afd80709"
    assert env.is_push()
