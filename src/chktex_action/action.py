"""
Main module for finding `.tex` files and running ChkTeX on them.

Includes logic to parse files, run ChkTeX, analyze errors, and write a Markdown summary
for GitHub Actions.
"""

import glob
import importlib
import importlib.metadata
import os

from github import Auth, Github
from github.File import File
from github.PaginatedList import PaginatedList

from chktex_action.chktex import Analysis, run_chktex
from chktex_action.environment import Environment
from chktex_action.logger import Log
from chktex_action.pull_request_review import (
    get_pull_request_number,
    process_pull_request,
)
from chktex_action.step_summary import build_markdown_step_summary, write_step_summary

# Only enable debugging when not running on GitHub Actions
if "true" == os.environ.get("DEBUG", "false"):
    try:
        pydevd_pycharm = importlib.import_module("pydevd_pycharm")
        pydevd_pycharm.settrace(
            "host.docker.internal",
            port=4567,
            stdoutToServer=True,
            stderrToServer=True,
            suspend=False,
        )
    except ImportError:
        print("pydevd_pycharm is not installed. Debugging is disabled.")


def get_tex_files(all_files: PaginatedList[File]) -> list[str]:
    """
    Filters out the .tex files from a list of files.
    """

    return [file.filename for file in all_files if file.filename.endswith(".tex")]


def run() -> int:
    """
    Entry point for the ChkTeX GitHub Action.

    Finds `.tex` files, runs ChkTeX, analyzes results, and writes a Markdown summary.
    """

    Log.notice(
        "Running ChkTeX Action version " + importlib.metadata.version("chktex-action")
    )

    env = Environment()

    if not (env.is_push() or env.is_pull_request()):
        Log.error("Only pull_request or push triggers are supported.")

        return 1

    token = Auth.Token(env.get_token())
    github = Github(auth=token)
    repository = github.get_repo(env.get_repository())
    latest_commit = repository.get_branch(env.get_ref()).commit

    pull_request = None

    if env.is_pull_request() and not env.is_lint_all():
        pull_request = repository.get_pull(
            get_pull_request_number(env.get_event_path())
        )

        files = get_tex_files(pull_request.get_files())
    elif env.is_push() and not env.is_lint_all():
        files = get_tex_files(latest_commit.files)
    else:
        files = glob.glob("**/*.tex", root_dir=env.get_workspace(), recursive=True)

    if not files:
        Log.notice("No .tex files found.")
        write_step_summary(env.get_step_summary(), "No .tex files found.")

        if pull_request:
            pull_request.create_review(
                body="## ChkTeX Action\n\nNo .tex files found.", event="APPROVE"
            )

        return 0

    Log.notice("Running ChkTeX version 1.7.9")
    errors = run_chktex(env.get_workspace(), files)
    analysis = Analysis(errors)
    analysis_string = str(analysis)

    if env.is_pull_request() and pull_request and not env.is_lint_all():
        check_run = latest_commit.get_check_runs()[0]
        process_pull_request(pull_request, check_run, errors, analysis_string)

    step_summary = build_markdown_step_summary(errors, analysis_string)
    write_step_summary(env.get_step_summary(), step_summary)

    if 0 == analysis.number_of_files:
        Log.notice("No errors or warnings found.")

        return 0

    Log.error(analysis_string)

    return 1
