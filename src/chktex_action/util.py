"""

"""

import json
import os


def is_pull_request() -> bool:
    """"""

    if "pull_request" == os.environ.get("GITHUB_EVENT_NAME", ""):
        return True

    return False


def is_debugging_enabled() -> bool:
    """"""

    if "1" == os.environ.get("RUNNER_DEBUG", ""):
        return True

    return False


class Log:
    prefix = " ::ChkTeX Action: "

    @staticmethod
    def error(message: str) -> None:
        print("::error" + Log.prefix + message)

    @staticmethod
    def notice(message: str) -> None:
        print("::notice" + Log.prefix + message)

    @staticmethod
    def debug(message: str) -> None:
        print("::debug" + Log.prefix + message)


def get_pull_request_number() -> int | None:
    """
    Retrieves the pull request number from the GitHub Actions event payload.

    Returns:
        int: The pull request number if available, or None if not a pull request event.
    """
    github_event_path = os.environ.get("GITHUB_EVENT_PATH", "")

    try:
        with open(github_event_path, "r") as event_file:
            event_data = json.load(event_file)

            return event_data.get("pull_request", {}).get("number")

    except Exception as e:
        Log.error(f"Error reading event data: {e}")

        return None
