"""
Contains various helper functions, classes, and methods.
"""

import os
from dataclasses import dataclass


@dataclass
class GitHub:
    # pylint: disable=too-many-arguments,too-many-positional-arguments

    """
    Contains GitHub environment variables.
    """

    def __init__(
        self,
        github_ref: str,
        github_workspace: str,
        github_event_path: str,
        github_repository: str,
        github_event_name: str,
        github_step_summary: str,
    ) -> None:
        self.github_ref = github_ref
        self.github_workspace = github_workspace
        self.github_event_path = github_event_path
        self.github_repository = github_repository
        self.github_event_name = github_event_name
        self.github_step_summary = github_step_summary


class Environment:
    """
    Loads all environment variables on initialization and stores them in as instance
    attributes.
    """

    def __init__(self) -> None:
        self.__github_token = self._get_required_environment_variable(
            "INPUT_GITHUB-TOKEN"
        )
        self.__lint_all = "true" == self._get_required_environment_variable(
            "INPUT_LINT-ALL"
        )
        self.__github = GitHub(
            (
                os.environ.get("GITHUB_REF_NAME", "")
                or os.environ.get("GITHUB_HEAD_REF", "")
            ),
            self._get_required_environment_variable("GITHUB_WORKSPACE"),
            self._get_required_environment_variable("GITHUB_EVENT_PATH"),
            self._get_required_environment_variable("GITHUB_REPOSITORY"),
            self._get_required_environment_variable("GITHUB_EVENT_NAME"),
            self._get_required_environment_variable("GITHUB_STEP_SUMMARY"),
        )

    @staticmethod
    def _get_required_environment_variable(key: str) -> str:
        value = os.environ.get(key)

        if not value:
            raise ValueError(f"Required environment variable {key} is missing.")
        return value

    def get_token(self) -> str:
        """
        Returns the GitHub token for authentication.
        """

        return self.__github_token

    def is_lint_all(self) -> bool:
        """
        Returns whether the `lint-all` input is set to `true`.
        """

        return self.__lint_all

    def get_ref(self) -> str:
        """
        Returns the branch name.
        """

        return self.__github.github_ref

    def get_workspace(self) -> str:
        """
        Returns the workspace path.
        """

        return self.__github.github_workspace

    def get_event_path(self) -> str:
        """
        Returns the event path.
        """

        return self.__github.github_event_path

    def get_repository(self) -> str:
        """
        Returns the repository name.
        """

        return self.__github.github_repository

    def get_step_summary(self) -> str:
        """
        Returns the step summary.
        """

        return self.__github.github_step_summary

    def is_push(self) -> bool:
        """
        Returns True if the workflow was triggered by a push event.
        """

        return "push" == self.__github.github_event_name

    def is_pull_request(self) -> bool:
        """
        Returns True if the workflow was triggered by a pull_request event.
        """

        return "pull_request" == self.__github.github_event_name
