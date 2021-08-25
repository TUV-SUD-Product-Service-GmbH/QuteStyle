"""Configuration for ChemUp unit tests with pytest."""
import logging
import os

from _pytest.config import Config
from _pytest.python import Function
from PyQt5.QtCore import QCoreApplication, QSettings, qInstallMessageHandler

from tsl import style
from tsl.edoc_database import (
    ENGINE,
    Base,
    Staff,
    _fetch_user_id,
    session_scope,
)
from tsl.init import qt_message_handler
from tsl.pse_database import ENGINE as PSE_ENGINE
from tsl.pse_database import Base as PSE_Base
from tsl.pse_database import Staff as PseStaff
from tsl.pse_database import _fetch_user_id as _pse_fetch_user_id
from tsl.pse_database import session_scope as pse_session_scope

# pylint: disable=invalid-name
log = logging.getLogger(".".join(["tsl", __name__]))
# pylint: enable=invalid-name

TFPATH = os.path.join("tests", "test_files")


def pytest_configure(config: Config) -> None:
    """Configure the tests."""
    markers = [
        "style: Test for styling which will reset global default style.",
    ]
    for marker in markers:
        config.addinivalue_line("markers", marker)


def init_user() -> None:
    """Create a new dummy user for use in the tests in PSE and EDOC db."""
    for scope, fetch, staff in (
        (session_scope, _fetch_user_id, Staff),
        (pse_session_scope, _pse_fetch_user_id, PseStaff),
    ):
        with scope() as session:
            user = staff(
                ST_WINDOWSID=os.getlogin(),
                ST_SURNAME="TSL-Toolbox",
                ST_ACTIVE=True,
                ST_TYPE=1,
                ST_SKILLGROUP="00000000",
                ST_FORENAME="Klaus",
            )
            session.add(user)
        # Init the user variables before creating test data for tests.
        fetch()


def pytest_runtest_setup() -> None:
    """Execute this function before every test case."""
    qInstallMessageHandler(qt_message_handler)

    # raise an exception if the database path isn't configured correctly
    # see https://pswiki.tuev-sued.com/display/TSL/Unit-Tests
    assert os.getenv("PSE_ENV") == "DEV"
    assert os.getenv("EDOC_ENV") == "DEV"
    assert "test_db" in PSE_ENGINE.url.query["odbc_connect"]
    assert "test_db" in ENGINE.url.query["odbc_connect"]

    QCoreApplication.setOrganizationName("TÜV SÜD Product Service GmbH")
    QCoreApplication.setOrganizationDomain("tuvsud.com")
    QCoreApplication.setApplicationName("tsl-lib")

    # Remove the settings stored with QSettings in the registry.
    QSettings().clear()

    PSE_Base.metadata.create_all()
    Base.metadata.create_all()

    # add the current user to the database
    init_user()


def pytest_runtest_teardown(item: Function) -> None:
    """Execute this function after every test case."""
    # raise the same exception as in setup. if those functions hit the real
    # database, we're done because everything gets deleted
    assert os.getenv("PSE_ENV") == "DEV"
    assert os.getenv("EDOC_ENV") == "DEV"
    assert "test_db" in PSE_ENGINE.url.query["odbc_connect"]
    assert "test_db" in ENGINE.url.query["odbc_connect"]

    Base.metadata.drop_all()
    PSE_Base.metadata.drop_all()

    # Remove the settings stored with QSettings in the registry.
    QSettings().clear()

    if "style" in [mark.name for mark in item.iter_markers()]:
        # Reset the stored style after a style test case.
        style.CURRENT_STYLE = "Darcula"
