"""
Contains tests for the action module.
"""

from pytest_mock import MockerFixture

from chktex_action.action import run


def test_run_no_tex_files(mocker: MockerFixture) -> None:
    """
    Test case: No .tex files found.
    """

    mock_env = mocker.patch("chktex_action.action.Environment")
    mock_env_instance = mock_env.return_value
    mock_env_instance.get_token.return_value = "12343"
    mock_env_instance.is_push.return_value = True
    mock_env_instance.is_pull_request.return_value = False
    mock_env_instance.is_lint_all.return_value = False
    mock_env_instance.get_workspace.return_value = "/workspace"
    mock_env_instance.get_step_summary.return_value = "/github_step_summary.md"

    mock_github = mocker.patch("chktex_action.action.Github")
    mock_github_instance = mock_github.return_value
    mock_repository = mock_github_instance.get_repo.return_value
    mock_branch = mock_repository.get_branch.return_value
    mock_branch.commit.files = []

    mock_log = mocker.patch("chktex_action.action.Log")
    mock_write_summary = mocker.patch("chktex_action.action.write_step_summary")

    exit_code = run()

    assert 0 == exit_code

    mock_log.error.assert_called_once_with("No .tex files found.")
    mock_write_summary.assert_called_once_with(
        "/github_step_summary.md", "No .tex files found."
    )


def test_run_with_errors(mocker: MockerFixture) -> None:
    """
    Test case: Errors are found in .tex files.
    """

    mock_env = mocker.patch("chktex_action.action.Environment")
    mock_env_instance = mock_env.return_value
    mock_env_instance.get_token.return_value = "12343"
    mock_env_instance.is_push.return_value = True
    mock_env_instance.is_pull_request.return_value = False
    mock_env_instance.is_lint_all.return_value = False
    mock_env_instance.get_workspace.return_value = "/workspace"

    mock_error = mocker.patch("chktex_action.chktex.Error")
    mock_error_instance = mock_error.return_value
    mock_error_instance.level = "Error"
    mock_error_instance.path = "fail.tex"
    mock_error_instance.line = 2
    mock_error_instance.message = "Some error message."
    mock_error_instance.context = ["hello", "world"]

    mock_run_chktex = mocker.patch("chktex_action.action.run_chktex")
    mock_run_chktex.return_value = [mock_error_instance]

    mock_github = mocker.patch("chktex_action.action.Github")
    mock_github_instance = mock_github.return_value
    mock_repository = mock_github_instance.get_repo.return_value
    mock_branch = mock_repository.get_branch.return_value

    mock_file = mocker.patch("chktex_action.action.File")
    mock_file_instance = mock_file.return_value
    mock_file_instance.filename = "file.tex"
    mock_branch.commit.files = [mock_file_instance, mock_file_instance]

    mock_log = mocker.patch("chktex_action.action.Log")

    exit_code = run()

    assert 1 == exit_code

    mock_log.error.assert_called_once_with(
        "Total files: 1, total errors: 1, total warnings: 0"
    )


def test_run_no_errors(mocker: MockerFixture) -> None:
    """
    Test case: No errors or warnings in .tex files.
    """

    mock_env = mocker.patch("chktex_action.action.Environment")
    mock_env_instance = mock_env.return_value
    mock_env_instance.get_token.return_value = "12343"
    mock_env_instance.is_push.return_value = True
    mock_env_instance.is_pull_request.return_value = False
    mock_env_instance.is_lint_all.return_value = False
    mock_env_instance.get_workspace.return_value = "/workspace"

    mock_run_chktex = mocker.patch("chktex_action.action.run_chktex")
    mock_run_chktex.return_value = []

    mock_github = mocker.patch("chktex_action.action.Github")
    mock_github_instance = mock_github.return_value
    mock_repository = mock_github_instance.get_repo.return_value
    mock_branch = mock_repository.get_branch.return_value

    mock_file = mocker.patch("chktex_action.action.File")
    mock_file_instance = mock_file.return_value
    mock_file_instance.filename = "file.tex"
    mock_branch.commit.files = [mock_file_instance, mock_file_instance]

    mock_log = mocker.patch("chktex_action.action.Log")

    exit_code = run()

    assert 0 == exit_code

    mock_log.notice.assert_any_call("No errors or warnings found.")
