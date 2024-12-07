""""""

from _pytest.capture import CaptureFixture

from chktex_action.logger import Log


def test_notice(capfd: CaptureFixture[str]) -> None:
    """"""

    Log.notice("This is a test.")
    out, _err = capfd.readouterr()

    assert out == "::notice ::ChkTeX Action: This is a test.\n"


def test_debug(capfd: CaptureFixture[str]) -> None:
    """"""

    Log.debug("This is a test.")
    out, _err = capfd.readouterr()

    assert out == "::debug ::ChkTeX Action: This is a test.\n"


def test_error(capfd: CaptureFixture[str]) -> None:
    """"""

    Log.error("This is a test.")
    out, _err = capfd.readouterr()

    assert out == "::error ::ChkTeX Action: This is a test.\n"
