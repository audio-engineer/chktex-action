"""
Handles pull requests.
"""

import json
from typing import TYPE_CHECKING, TypedDict

from github.CheckRun import CheckRun
from github.PullRequest import PullRequest

from chktex_action.logger import Log

if TYPE_CHECKING:
    from chktex_action.chktex import Error

annotation_level_mapping = {
    "Error": "failure",
    "Warning": "warning",
}


class Annotation(TypedDict):
    """
    Represents an annotation.
    """

    path: str
    start_line: int
    end_line: int
    message: str
    title: str
    annotation_level: str


def get_pull_request_number(github_event_path: str) -> int:
    """
    Retrieves the pull request number from the GitHub Actions event payload.

    Returns:
        int: The pull request number if available, or None if not a pull request event.
    """

    with open(github_event_path, "r", encoding="utf-8") as event_file:
        event_data = json.load(event_file)
        pull_request_number = event_data.get("pull_request", {}).get("number")

        return int(pull_request_number)


def build_message(error: "Error") -> str:
    """
    Builds the annotation message from an error.
    """

    if error.context:
        return f"{error.message}\n\n{'\n'.join(error.context)}"

    return error.message


def create_annotations(errors: list["Error"]) -> list[Annotation]:
    """
    Create a list of GitHub check-run annotations from the error list.
    """

    return [
        {
            "path": error.path,
            "start_line": error.line,
            "end_line": error.line,
            "message": build_message(error),
            "title": "ChkTeX Action",
            "annotation_level": annotation_level_mapping.get(error.level, "warning"),
        }
        for error in errors
    ]


def build_output(
    errors: list["Error"], analysis_string: str
) -> dict[str, str | list[Annotation]]:
    """
    Build the output dictionary for the check run.
    """

    return {
        "title": "ChkTeX Action",
        "summary": analysis_string,
        "annotations": create_annotations(errors),
    }


def process_pull_request(
    pull_request: PullRequest,
    check_run: CheckRun,
    errors: list["Error"],
    analysis_string: str,
) -> None:
    """
    Process the pull request by creating reviews and updating check runs with results.
    """

    output = build_output(errors, analysis_string)
    Log.debug("Check Run Output: " + str(output))
    check_run.edit(output=output)

    if errors:
        pull_request.create_review(
            body="## ChkTeX Action\n\nThere are issues with your code. 😔 "
            "Check the annotations under the **Files changed** tab.",
            event="REQUEST_CHANGES",
        )
    else:
        pull_request.create_review(body="## ChkTeX Action\n\nLGTM! 🚀", event="APPROVE")
