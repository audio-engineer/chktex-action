"""
Provides global fixtures that are used by multiple test modules.
"""

import pytest

from chktex_action.chktex import Error


@pytest.fixture(scope="module")
def error_list() -> list[Error]:
    """
    Returns a list of error objects.
    """

    return [
        Error(
            "Error",
            17,
            "fail.tex",
            5,
            "Something went wrong.",
            [r"\end{document", r"    ^"],
        ),
        Error(
            "Warning",
            2,
            "fail.tex",
            10,
            "Something went wrong.",
            [r"\begin{document}", r"^^^^^^"],
        ),
        Error("Error", 15, "another.tex", 32, "Something went wrong.", []),
    ]
