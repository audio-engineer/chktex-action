""""""

import pytest

from chktex_action.chktex import Error


@pytest.fixture(scope="module")
def errors_list() -> list[Error]:
    """"""

    return [
        Error("Error", 17, "fail.tex", 5, "Something", [""]),
        Error("Warning", 2, "fail.tex", 10, "Something", [""]),
        Error("Error", 15, "another.tex", 32, "Something", [""]),
    ]
