"""
Contains tests of the logger module.
"""

from _pytest.capture import CaptureFixture

from chktex_action.logger import Log


def test_notice(capfd: CaptureFixture[str]) -> None:
    """
    Tests the notice method.
    """

    Log.notice("This is a test.")
    out, _err = capfd.readouterr()

    assert out == "::notice ::ChkTeX Action: This is a test.\n"


def test_debug(capfd: CaptureFixture[str]) -> None:
    """
    Tests the debug method.
    """

    Log.debug("This is a test.")
    out, _err = capfd.readouterr()

    assert out == "::debug ::ChkTeX Action: This is a test.\n"


def test_error(capfd: CaptureFixture[str]) -> None:
    """
    Tests the error method.
    """

    Log.error("This is a test.")
    out, _err = capfd.readouterr()

    assert out == "::error ::ChkTeX Action: This is a test.\n"
