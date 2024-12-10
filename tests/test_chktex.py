"""
Contains tests of the chktex module.
"""

import pytest
from pytest_mock import MockerFixture

from chktex_action.chktex import Analysis, Error, parse_chktex_output, run_chktex


@pytest.fixture(name="chktex_output_fixture")
def chktex_output() -> str:
    """
    Fixture that returns ChkTeX output.
    """

    return r"""Error 14 in src/fail.tex line 5: Could not find argument for command.
\end{document
^^^^
Warning 15 in src/fail.tex line 5: No match found for `{'.
\end{document
    ^
Warning 15 in src/fail.tex line 3: No match found for `document'.
\begin{document}
^^^^^^
Warning 17 in src/fail.tex line 5: Number of `{' doesn't match the number of `}'!


"""


def test_parse_chktex_output(chktex_output_fixture: str) -> None:
    """
    Test the parse_chktex_output function.
    """

    # Actual
    errors = parse_chktex_output(chktex_output_fixture)

    # Assertions
    assert len(errors) == 4

    assert errors[0].level == "Error"
    assert errors[0].path == "src/fail.tex"
    assert errors[0].number == 14
    assert errors[0].line == 5
    assert errors[0].message == "Could not find argument for command."
    assert errors[0].context == [r"\end{document", r"^^^^"]

    assert errors[1].level == "Warning"
    assert errors[1].path == "src/fail.tex"
    assert errors[1].number == 15
    assert errors[1].line == 5
    assert errors[1].message == "No match found for `{'."
    assert errors[1].context == [r"\end{document", r"    ^"]

    assert errors[2].level == "Warning"
    assert errors[2].path == "src/fail.tex"
    assert errors[2].number == 15
    assert errors[2].line == 3
    assert errors[2].message == "No match found for `document'."
    assert errors[2].context == [r"\begin{document}", r"^^^^^^"]

    assert errors[3].level == "Warning"
    assert errors[3].path == "src/fail.tex"
    assert errors[3].number == 17
    assert errors[3].line == 5
    assert errors[3].message == "Number of `{' doesn't match the number of `}'!"
    assert errors[3].context == []


def test_analysis(error_list: list[Error]) -> None:
    """
    Test the __str__ method of the Analysis class.
    """

    # Actual
    analysis = Analysis(error_list)

    # Assertions
    assert "Total files: 2, total errors: 2, total warnings: 1" == str(analysis)


def test_run_chktex_with_local_chktexrc(
    mocker: MockerFixture, chktex_output_fixture: str
) -> None:
    """
    Test `run_chktex` when a local .chktexrc file exists.
    """

    # Mock find_local_chktexrc
    mocker.patch(
        "chktex_action.chktex.find_local_chktexrc", return_value="/workspace/.chktexrc"
    )

    # Mock subprocess.run
    mock_subprocess_run = mocker.patch("chktex_action.chktex.subprocess.run")
    mock_subprocess_run.return_value.stdout = chktex_output_fixture
    mock_subprocess_run.return_value.stderr = ""
    mock_subprocess_run.return_value.returncode = 0

    # Mock logger
    mock_logger = mocker.patch("chktex_action.chktex.Log")

    # Actual
    errors = run_chktex("/workspace", ["src/fail.tex"])

    # Assertions
    mock_logger.notice.assert_called_once_with("Using local .chktexrc file.")
    mock_logger.debug.assert_called_once_with("Linting File: src/fail.tex")

    mock_subprocess_run.assert_called_once_with(
        [
            "chktex",
            "-q",
            "--inputfiles=0",
            "-l",
            "/workspace/.chktexrc",
            "src/fail.tex",
        ],
        cwd="/workspace",
        capture_output=True,
        text=True,
        check=False,
    )

    assert 4 == len(errors)

    assert errors[2] == Error(
        level="Warning",
        number=15,
        path="src/fail.tex",
        line=3,
        message="No match found for `document'.",
        context=[r"\begin{document}", r"^^^^^^"],
    )


def test_run_chktex_without_local_chktexrc(
    mocker: MockerFixture, chktex_output_fixture: str
) -> None:
    """
    Test `run_chktex` when no local .chktexrc file exists.
    """

    # Mock find_local_chktexrc
    mocker.patch("chktex_action.chktex.find_local_chktexrc", return_value=None)

    # Mock subprocess.run
    mock_subprocess_run = mocker.patch("chktex_action.chktex.subprocess.run")
    mock_subprocess_run.return_value.stdout = chktex_output_fixture
    mock_subprocess_run.return_value.stderr = ""
    mock_subprocess_run.return_value.returncode = 0

    # Mock logger
    mock_logger = mocker.patch("chktex_action.chktex.Log")

    # Actual
    errors = run_chktex("/workspace", ["src/fail.tex"])

    # Assertions
    mock_logger.notice.assert_called_once_with("Using global chktexrc file.")
    mock_logger.debug.assert_called_once_with("Linting File: src/fail.tex")

    mock_subprocess_run.assert_called_once_with(
        ["chktex", "-q", "--inputfiles=0", "src/fail.tex"],
        cwd="/workspace",
        capture_output=True,
        text=True,
        check=False,
    )

    assert 4 == len(errors)

    assert errors[2] == Error(
        level="Warning",
        number=15,
        path="src/fail.tex",
        line=3,
        message="No match found for `document'.",
        context=[r"\begin{document}", r"^^^^^^"],
    )
