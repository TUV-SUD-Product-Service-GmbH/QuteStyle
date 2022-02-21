"""Configuration for ChemUp unit tests with pytest."""
import logging
import os
import sys
from pathlib import Path

import pytest
from _pytest.config import Config
from _pytest.python import Function
from PyQt5.QtCore import QCoreApplication, QSettings, qInstallMessageHandler

# ensure that the resources are loaded
import tsl.resources_rc  # pylint: disable=unused-import  # noqa: F401
from tests.test_tsl_style_main_window import EmptyWindow
from tsl import style
from tsl.dev.mocks import check_call
from tsl.init import qt_message_handler
from tsl.style import Themes
from tsl.tsl_application import TslApplication
from tsl.update_window import AppData

log = logging.getLogger(  # pylint: disable=invalid-name
    ".".join(["tsl", __name__])
)

TFPATH = Path("tests") / "test_files"


def pytest_configure(config: Config) -> None:
    """Configure the tests."""
    markers = [
        "style: Test for styling which will reset global default style.",
        "pse_db: Configure the PSE Db for usage.",
        "edoc_db: Configure the eDOC Db for usage.",
    ]
    for marker in markers:
        config.addinivalue_line("markers", marker)


def pytest_runtest_setup(item: Function) -> None:
    """Execute this function before every test case."""
    qInstallMessageHandler(qt_message_handler)

    # raise an exception if the database path isn't configured correctly
    # see https://pswiki.tuev-sued.com/display/TSL/Unit-Tests

    if "edoc_db" in [mark.name for mark in item.iter_markers()]:
        # pylint: disable=import-outside-toplevel
        from tsl.edoc_database import (
            ENGINE,
            Base,
            Staff,
            _fetch_user_id,
            session_scope,
        )

        # pylint: enable=import-outside-toplevel

        assert os.getenv("EDOC_ENV") == "DEV"
        assert "test_db" in ENGINE.url.query["odbc_connect"]
        Base.metadata.drop_all()
        Base.metadata.create_all()

        with session_scope() as session:
            edoc_user = Staff(
                ST_WINDOWSID=os.getlogin(),
                ST_SURNAME="TSL-Toolbox",
                ST_ACTIVE=True,
                ST_TYPE=1,
                ST_SKILLGROUP="00000000",
                ST_FORENAME="Klaus",
            )
            session.add(edoc_user)
        _fetch_user_id()

    QCoreApplication.setOrganizationName("TÜV SÜD Product Service GmbH")
    QCoreApplication.setOrganizationDomain("tuvsud.com")
    QCoreApplication.setApplicationName("tsl-lib")

    # Remove the settings stored with QSettings in the registry.
    QSettings().clear()


def pytest_runtest_teardown(item: Function) -> None:
    """Execute this function after every test case."""
    # Remove the settings stored with QSettings in the registry.
    QSettings().clear()

    if "style" in [mark.name for mark in item.iter_markers()]:
        # Reset the stored style after a style test case.
        style.CURRENT_STYLE = Themes.DARCULA


class TSLTestApplication(TslApplication):
    """TSL Test Application."""

    MAIN_WINDOW_CLASS = EmptyWindow

    APP_DATA = AppData("TSL-APP", "2.3.4")


@pytest.fixture(scope="session")
def qapp():  # type: ignore
    """
    Overwrite pytest's qapp fixture.

    This is required because a custom QApplication is used and there can
    only be one QApplication during the tests (qtbot also creates one).
    """
    with check_call(TslApplication, "show_main_window", None, call_count=-1):
        yield TSLTestApplication(sys.argv, False)
