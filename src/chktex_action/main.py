"""
Main module for finding `.tex` files and running ChkTeX on them.

Includes logic to parse files, run ChkTeX, analyze errors, and write a Markdown summary
for GitHub Actions.
"""

import glob
import os
import sys
from collections import Counter
from chktex import run_chktex, Error
from util import Log, is_pull_request, get_pull_request_number
from step_summary import (
    write_step_summary,
    build_markdown_step_summary,
)
from github import Github, Auth

# Only enable debugging when not running on GitHub Actions
if not os.environ.get("GITHUB_ACTIONS"):
    try:
        import pydevd_pycharm

        pydevd_pycharm.settrace(
            "host.docker.internal",
            port=4567,
            stdoutToServer=True,
            stderrToServer=True,
        )
    except ImportError:
        print("pydevd_pycharm is not installed. Debugging is disabled.")


def find_tex_files(github_workspace_path: str) -> list[str]:
    """
    Finds all `.tex` files in the specified GitHub workspace.
    """

    return glob.glob("**/*.tex", root_dir=github_workspace_path, recursive=True)


def analyze_errors(errors: list[Error]) -> tuple[int, int, int]:
    """
    Analyzes the list of ChkTeX errors and warnings.

    Returns the number of unique files, errors, and warnings.
    """

    unique_files = set(error.file for error in errors)
    type_counts = Counter(error.type for error in errors)

    number_of_files = len(unique_files)
    number_of_errors = type_counts.get("Error", 0)
    number_of_warnings = type_counts.get("Warning", 0)

    return number_of_files, number_of_errors, number_of_warnings


def main():
    """
    Entry point for the ChkTeX GitHub Action.

    Finds `.tex` files, runs ChkTeX, analyzes results, and writes a Markdown summary.
    """

    github_workspace_path = os.environ.get("GITHUB_WORKSPACE")

    if not github_workspace_path:
        print("No GITHUB_WORKSPACE environment variable set.")

        sys.exit(1)

    print("lint-all: " + os.environ.get("INPUT_LINT-ALL", "empty"))
    print("token: " + os.environ.get("GITHUB_TOKEN", "empty"))

    if not is_pull_request():
        token = Auth.Token(os.environ.get("GITHUB_TOKEN"))
        github = Github(auth=token)

        print(
            github.get_repo(os.environ.get("GITHUB_REPOSITORY"))
            .get_pull(get_pull_request_number())
            .get_files()
        )

    tex_files = find_tex_files(github_workspace_path)

    if not tex_files:
        Log.error("No .tex files found.")

        write_step_summary("## ChkTeX Action Summary\nNo .tex files found.")

        sys.exit(0)

    Log.notice("Running ChkTeX version 1.7.9")

    errors = run_chktex(github_workspace_path, tex_files)

    number_of_files, number_of_errors, number_of_warnings = analyze_errors(errors)

    step_summary = build_markdown_step_summary(
        errors, number_of_files, number_of_errors, number_of_warnings
    )

    write_step_summary(step_summary)

    if 0 == number_of_files:
        Log.notice("No errors or warnings found.")

        sys.exit(0)

    Log.error(
        "Errors: " + str(number_of_errors) + ", warnings: " + str(number_of_warnings)
    )

    sys.exit(1)


if __name__ == "__main__":
    main()
