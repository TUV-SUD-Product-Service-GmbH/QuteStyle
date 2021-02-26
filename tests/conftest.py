"""Configuration for ChemUp unit tests with pytest."""
import os
import logging

from PyQt5.QtCore import QSettings, QCoreApplication, qInstallMessageHandler
from tsl.edoc_database import ENGINE, Base, session_scope, Staff
from tsl.pse_database import Base as PSE_Base, ENGINE as PSE_ENGINE
from tsl.init import qt_message_handler


# pylint: disable=invalid-name
log = logging.getLogger(".".join(["tsl", __name__]))
# pylint: enable=invalid-name

TFPATH = os.path.join("tests", "test_files")


def init_user() -> None:
    """Create a new dummy user for use in the tests."""
    with session_scope() as session:
        user = Staff(ST_WINDOWSID=os.getlogin(), ST_SURNAME="TSL-Toolbox",
                     ST_ACTIVE=True, ST_TYPE=1, ST_SKILLGROUP="00000000",
                     ST_FORENAME="Klaus")
        session.add(user)


def pytest_runtest_setup() -> None:
    """Execute this function before every test case."""
    qInstallMessageHandler(qt_message_handler)

    # raise an exception if the database path isn't configured correctly
    # see https://pswiki.tuev-sued.com/display/TSL/Unit-Tests
    assert "test_db" in PSE_ENGINE.url.database
    assert "test_db" in ENGINE.url.database

    QCoreApplication.setOrganizationName("TÜV SÜD Product Service GmbH")
    QCoreApplication.setOrganizationDomain("tuvsud.com")
    QCoreApplication.setApplicationName("tsl-lib")

    # remove the old personal settings file
    delete_settings()

    log.debug("Using db path for pse: %s", os.getenv("PSE_DB_PATH"))
    PSE_Base.metadata.create_all()

    log.debug("Using db path for edoc: %s", os.getenv("EDOC_DB_PATH"))
    Base.metadata.create_all()

    # add the current user to the database
    init_user()


def pytest_runtest_teardown() -> None:
    """Execute this function after every test case."""
    # raise the same exception as in setup. if those functions hit the real
    # database, we're done
    assert "test_db" in PSE_ENGINE.url.database
    assert "test_db" in ENGINE.url.database

    Base.metadata.drop_all()
    PSE_Base.metadata.drop_all()


def delete_settings() -> None:
    """Remove the personal settings file on X drive."""
    settings = QSettings()
    settings.clear()
