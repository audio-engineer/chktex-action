"""
Logger.
"""

import os


class Log:
    """
    Contains static methods for logging to the GitHub workflow console.
    """

    prefix = " ::ChkTeX Action: "

    @staticmethod
    def error(message: str) -> None:
        """
        Logs an error.
        """

        print("::error" + Log.prefix + message)

    @staticmethod
    def notice(message: str) -> None:
        """
        Logs a notice.
        """

        print("::notice" + Log.prefix + message)

    @staticmethod
    def debug(message: str) -> None:
        """
        Logs a debug message if debugging is enabled.
        """

        if "1" == os.environ.get("RUNNER_DEBUG", ""):
            print("::debug" + Log.prefix + message)
