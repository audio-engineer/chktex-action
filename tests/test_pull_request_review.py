"""
Contains tests of the pull_request_review module.
"""

import pytest

from chktex_action.chktex import Analysis, Error
from chktex_action.pull_request_review import (
    Annotation,
    build_output,
    create_annotations,
)


@pytest.fixture(name="annotation_list_fixture")
def annotation_list() -> list[Annotation]:
    """
    Returns a list of error objects.
    """

    return [
        {
            "path": "fail.tex",
            "start_line": 5,
            "end_line": 5,
            "message": "Something went wrong.\n\n\\end{document\n    ^",
            "title": "ChkTeX Action",
            "annotation_level": "failure",
        },
        {
            "path": "fail.tex",
            "start_line": 10,
            "end_line": 10,
            "message": "Something went wrong.\n\n\\begin{document}\n^^^^^^",
            "title": "ChkTeX Action",
            "annotation_level": "warning",
        },
        {
            "path": "another.tex",
            "start_line": 32,
            "end_line": 32,
            "message": "Something went wrong.",
            "title": "ChkTeX Action",
            "annotation_level": "failure",
        },
    ]


def test_create_annotations(
    annotation_list_fixture: list[Annotation], error_list: list[Error]
) -> None:
    """
    Tests the create_annotations function.
    """

    # Actual
    annotations_list = create_annotations(error_list)

    # Assertions
    assert annotation_list_fixture == annotations_list


def test_build_output(error_list: list[Error]) -> None:
    """
    Tests the build_output function.
    """

    # Actual
    analysis_string = str(Analysis(error_list))
    output = build_output(error_list, analysis_string)

    # Assertions
    assert output["title"] == "ChkTeX Action"
    assert output["summary"] == analysis_string
    assert output["annotations"] == create_annotations(error_list)
