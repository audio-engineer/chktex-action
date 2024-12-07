"""
Contains various helper functions, classes, and methods.
"""

import os


class Environment:
    """
    Loads all environment variables on initialization and stores them in as instance
    attributes.
    """

    def __init__(self) -> None:
        self.github_workspace = self._get_required_environment_variable(
            "GITHUB_WORKSPACE"
        )
        self.github_token = self._get_required_environment_variable(
            "INPUT_GITHUB-TOKEN"
        )
        self.github_event_path = self._get_required_environment_variable(
            "GITHUB_EVENT_PATH"
        )
        self.github_repository = self._get_required_environment_variable(
            "GITHUB_REPOSITORY"
        )
        self.github_event_name = self._get_required_environment_variable(
            "GITHUB_EVENT_NAME"
        )
        self.lint_all = "true" == self._get_required_environment_variable(
            "INPUT_LINT-ALL"
        )
        self.step_summary = self._get_required_environment_variable(
            "GITHUB_STEP_SUMMARY"
        )
        self.head_ref = os.environ.get("GITHUB_REF_NAME", "") or os.environ.get(
            "GITHUB_HEAD_REF", ""
        )

    @staticmethod
    def _get_required_environment_variable(key: str) -> str:
        value = os.environ.get(key)

        if not value:
            raise ValueError(f"Required environment variable {key} is missing.")
        return value

    def is_push(self) -> bool:
        """
        Returns True if the workflow was triggered by a push event.
        """

        return "push" == self.github_event_name

    def is_pull_request(self) -> bool:
        """
        Returns True if the workflow was triggered by a pull_request event.
        """

        return "pull_request" == self.github_event_name
