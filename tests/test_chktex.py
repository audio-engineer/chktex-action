"""
Contains tests of the chktex module.
"""

import pytest

from chktex_action.chktex import Analysis, Error, parse_chktex_output


@pytest.fixture
def chktex_output() -> str:
    """
    Fixture that returns ChkTeX output.
    """

    return r"""
Error 14 in fail.tex line 5: Could not find argument for command.
\end{document
^^^^
Warning 15 in fail.tex line 5: No match found for `{'.
\end{document
    ^
Warning 15 in fail.tex line 3: No match found for `document'.
\begin{document}
^^^^^^
Warning 17 in fail.tex line 5: Number of `{' doesn't match the number of `}'!


"""


def test_parse_chktex_output(chktex_output: str) -> None:
    """
    Test the parse_chktex_output function.
    """

    errors = parse_chktex_output(chktex_output)

    assert len(errors) == 4

    assert errors[0].level == "Error"
    assert errors[0].path == "fail.tex"
    assert errors[0].number == 14
    assert errors[0].line == 5
    assert errors[0].message == "Could not find argument for command."
    assert errors[0].context == [r"\end{document", r"^^^^"]

    assert errors[1].level == "Warning"
    assert errors[1].path == "fail.tex"
    assert errors[1].number == 15
    assert errors[1].line == 5
    assert errors[1].message == "No match found for `{'."
    assert errors[1].context == [r"\end{document", r"    ^"]

    assert errors[2].level == "Warning"
    assert errors[2].path == "fail.tex"
    assert errors[2].number == 15
    assert errors[2].line == 3
    assert errors[2].message == "No match found for `document'."
    assert errors[2].context == [r"\begin{document}", r"^^^^^^"]

    assert errors[3].level == "Warning"
    assert errors[3].path == "fail.tex"
    assert errors[3].number == 17
    assert errors[3].line == 5
    assert errors[3].message == "Number of `{' doesn't match the number of `}'!"
    assert errors[3].context == []


def test_analysis(errors_list: list[Error]) -> None:
    """"""

    analysis = Analysis(errors_list)

    assert "Total files: 2, total errors: 2, total warnings: 1" == str(analysis)
