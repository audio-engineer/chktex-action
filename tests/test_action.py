"""
Contains tests for the action module.
"""

import json
from unittest.mock import call

from pytest_mock import MockerFixture

from chktex_action.action import run


def test_run_not_push_not_pull_request(mocker: MockerFixture) -> None:
    """
    Test case: Neither push nor pull_request event
    """

    # Mock environment
    mock_env = mocker.patch("chktex_action.action.Environment")
    mock_env_instance = mock_env.return_value
    mock_env_instance.is_push.return_value = False
    mock_env_instance.is_pull_request.return_value = False

    # Mock logger
    mock_log = mocker.patch("chktex_action.action.Log")

    # Actual
    exit_code = run()

    # Assertions
    assert 1 == exit_code

    mock_log.notice.assert_called_once_with("Running ChkTeX Action version 2.2.0")
    mock_log.error.assert_called_once_with(
        "Only pull_request or push triggers are supported."
    )


def test_run_no_tex_files(mocker: MockerFixture) -> None:
    """
    Test case: Push event but no .tex files found.
    """

    # Mock environment
    mock_env = mocker.patch("chktex_action.action.Environment")
    mock_env_instance = mock_env.return_value
    mock_env_instance.get_token.return_value = "12343"
    mock_env_instance.is_push.return_value = True
    mock_env_instance.is_pull_request.return_value = False
    mock_env_instance.is_lint_all.return_value = False
    mock_env_instance.get_workspace.return_value = "/workspace"
    mock_env_instance.get_step_summary.return_value = "/github_step_summary.md"

    # Mock GitHub
    mock_github = mocker.patch("chktex_action.action.Github")
    mock_github_instance = mock_github.return_value
    mock_repository = mock_github_instance.get_repo.return_value
    mock_branch = mock_repository.get_branch.return_value
    mock_branch.commit.files = []

    # Mock write_step_summary
    mock_write_summary = mocker.patch("chktex_action.action.write_step_summary")

    # Mock logger
    mock_log = mocker.patch("chktex_action.action.Log")

    # Actual
    exit_code = run()

    # Assertions
    assert 0 == exit_code

    mock_log.notice.assert_has_calls(
        [call("Running ChkTeX Action version 2.2.0"), call("No .tex files found.")]
    )
    mock_write_summary.assert_called_once_with(
        "/github_step_summary.md", "No .tex files found."
    )


def test_run_no_errors(mocker: MockerFixture) -> None:
    """
    Test case: Push event, but no errors or warnings in .tex files.
    """

    # Mock environment
    mock_env = mocker.patch("chktex_action.action.Environment")
    mock_env_instance = mock_env.return_value
    mock_env_instance.get_token.return_value = "12343"
    mock_env_instance.is_push.return_value = True
    mock_env_instance.is_pull_request.return_value = False
    mock_env_instance.is_lint_all.return_value = False
    mock_env_instance.get_workspace.return_value = "/workspace"

    # Mock run_chktex
    mock_run_chktex = mocker.patch("chktex_action.action.run_chktex")
    mock_run_chktex.return_value = []

    # Mock GitHub
    mock_github = mocker.patch("chktex_action.action.Github")
    mock_github_instance = mock_github.return_value
    mock_repository = mock_github_instance.get_repo.return_value
    mock_branch = mock_repository.get_branch.return_value

    # Mock file
    mock_file = mocker.patch("chktex_action.action.File")
    mock_file_instance = mock_file.return_value
    mock_file_instance.filename = "file.tex"
    mock_branch.commit.files = [mock_file_instance, mock_file_instance]

    # Mock logger
    mock_log = mocker.patch("chktex_action.action.Log")

    # Actual
    exit_code = run()

    # Assertions
    assert 0 == exit_code

    mock_log.notice.assert_has_calls(
        [
            call("Running ChkTeX Action version 2.2.0"),
            call("Running ChkTeX version 1.7.9"),
            call("No errors or warnings found."),
        ]
    )


def test_run_on_push_with_errors(mocker: MockerFixture) -> None:
    """
    Test case: Push event, with errors.
    """

    # Mock environment
    mock_env = mocker.patch("chktex_action.action.Environment")
    mock_env_instance = mock_env.return_value
    mock_env_instance.get_token.return_value = "12343"
    mock_env_instance.is_push.return_value = True
    mock_env_instance.is_pull_request.return_value = False
    mock_env_instance.is_lint_all.return_value = False
    mock_env_instance.get_workspace.return_value = "/workspace"

    # Mock error
    mock_error = mocker.patch("chktex_action.chktex.Error")
    mock_error_instance = mock_error.return_value
    mock_error_instance.level = "Error"
    mock_error_instance.path = "fail.tex"
    mock_error_instance.line = 2
    mock_error_instance.message = "Some error message."
    mock_error_instance.context = ["hello", "world"]

    # Mock run_chktex
    mock_run_chktex = mocker.patch("chktex_action.action.run_chktex")
    mock_run_chktex.return_value = [mock_error_instance]

    # Mock GitHub
    mock_github = mocker.patch("chktex_action.action.Github")
    mock_github_instance = mock_github.return_value
    mock_repository = mock_github_instance.get_repo.return_value
    mock_branch = mock_repository.get_branch.return_value

    # Mock file
    mock_file = mocker.patch("chktex_action.action.File")
    mock_file_instance = mock_file.return_value
    mock_file_instance.filename = "file.tex"

    mock_branch.commit.files = [mock_file_instance, mock_file_instance]

    # Mock logger
    mock_log = mocker.patch("chktex_action.action.Log")

    # Actual
    exit_code = run()

    # Assertions
    assert 1 == exit_code

    mock_log.notice.assert_has_calls(
        [
            call("Running ChkTeX Action version 2.2.0"),
            call("Running ChkTeX version 1.7.9"),
        ]
    )
    mock_log.error.assert_called_once_with(
        "Total files: 1, total errors: 1, total warnings: 0"
    )


def test_run_on_pull_request_with_errors(mocker: MockerFixture) -> None:
    """
    Test case: Pull request event, with errors.
    """

    # Mock environment
    mock_env = mocker.patch("chktex_action.action.Environment")
    mock_env_instance = mock_env.return_value
    mock_env_instance.get_token.return_value = "12343"
    mock_env_instance.is_push.return_value = False
    mock_env_instance.is_pull_request.return_value = True
    mock_env_instance.is_lint_all.return_value = False
    mock_env_instance.get_repository.return_value = "j2kun/chktex-action"
    mock_env_instance.get_event_path.return_value = "/workspace/events/event.json"

    # Mock GitHub
    mock_github = mocker.patch("chktex_action.action.Github")
    mock_github_instance = mock_github.return_value
    mock_repository = mock_github_instance.get_repo.return_value

    # Mock file
    mock_file = mocker.patch("chktex_action.action.File")
    mock_file_instance = mock_file.return_value
    mock_file_instance.filename = "file.tex"

    mock_repository.get_pull.return_value.get_files.return_value = [
        mock_file_instance,
        mock_file_instance,
    ]

    # Mock
    mocker.patch(
        "chktex_action.pull_request_review.open",
        mocker.mock_open(read_data=json.dumps({"pull_request": {"number": 2}})),
    )
    pr_number = mocker.patch(
        "chktex_action.pull_request_review.get_pull_request_number"
    )
    pr_number.return_value = 2

    # Mock error
    mock_error = mocker.patch("chktex_action.chktex.Error")
    mock_error_instance = mock_error.return_value
    mock_error_instance.level = "Error"
    mock_error_instance.path = "fail.tex"
    mock_error_instance.line = 2
    mock_error_instance.message = "Some error message."
    mock_error_instance.context = ["hello", "world"]

    # Mock run_chktex
    mock_run_chktex = mocker.patch("chktex_action.action.run_chktex")
    mock_run_chktex.return_value = [mock_error_instance]

    # Mock logger
    mock_log = mocker.patch("chktex_action.action.Log")

    # Actual
    exit_code = run()

    # Assertions
    assert 1 == exit_code

    mock_log.notice.assert_has_calls(
        [
            call("Running ChkTeX Action version 2.2.0"),
            call("Running ChkTeX version 1.7.9"),
        ]
    )
    mock_log.error.assert_called_once_with(
        "Total files: 1, total errors: 1, total warnings: 0"
    )
