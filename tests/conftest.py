"""Configuration for ChemUp unit tests with pytest."""
from __future__ import annotations

import logging
import os
import string
import sys
from pathlib import Path
from random import choice, randint
from typing import Optional, cast

import PyQt5
import pytest
from _pytest.config import Config
from _pytest.fixtures import SubRequest
from _pytest.python import Function
from PyQt5.QtCore import (
    QCoreApplication,
    QSettings,
    Qt,
    qInstallMessageHandler,
)
from PyQt5.QtWidgets import QStyle, QStyleOptionButton, QStyleOptionViewItem

# ensure that the resources are loaded
import tsl.resources_rc  # pylint: disable=unused-import  # noqa: F401
from tests.test_tsl_style_main_window import EmptyWindow
from tsl import style
from tsl.dev.mocks import check_call
from tsl.init import qt_message_handler
from tsl.tsl_application import TslApplication
from tsl.tsl_style import ToggleOptionButton, TSLStyle
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
        style.CURRENT_STYLE = "Darcula"


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


def random_string(
    length: int = 5, allow_space: bool = False, new_line: bool = False
) -> str:
    """Generate a random string that is length long."""
    # todo: this is used in ChemUp and Toolbox, but implemented there also,
    # it should be imported and used from library.
    characters = string.ascii_lowercase + string.ascii_uppercase
    if allow_space:
        characters += " "
    if new_line:
        characters += "\n"
    return "".join(choice(characters) for _ in range(length))


@pytest.fixture(
    name="text",
    scope="class",
    params=(random_string(), None),
    ids=("text", "no text"),
)
def fixture_text(request: SubRequest) -> str | None:
    """Return the text for a QStyleOptionButton."""
    return cast(Optional[str], request.param)


@pytest.fixture(name="style_option_button", scope="class")
def fixture_style_option_button(
    direction: Qt.LayoutDirection,
    state: PyQt5.QtWidgets.QStyle,
    text: str | None,
) -> QStyleOptionButton:
    """Create an QStyleOptionButton for testing."""
    option = QStyleOptionButton()
    option.direction = direction
    option.state = state  # type: ignore
    option.palette = TSLStyle().standardPalette()
    # todo: Fix this in the PyQt5/6 stubs
    option.text = text  # type: ignore
    return option


@pytest.fixture(name="position", scope="class")
def fixture_position() -> int:
    """Provide a position for testing."""
    return randint(0, 10)


@pytest.fixture(name="toggle_option_button", scope="class")
def fixture_toggle_option_button(
    style_option_button: QStyleOptionButton, position: int
) -> ToggleOptionButton:
    """Create a ToggleOptionButton for testing."""
    option = ToggleOptionButton()
    option.direction = style_option_button.direction
    option.state = style_option_button.state
    option.palette = style_option_button.palette
    option.text = style_option_button.text
    option.position = position
    return option


@pytest.fixture(name="style_option_view_item", scope="class")
def fixture_style_option_view_item() -> QStyleOptionViewItem:
    """Create a QStyleOptionViewItem for testing."""
    return QStyleOptionViewItem()


@pytest.fixture(
    name="direction",
    params=(Qt.LeftToRight, Qt.RightToLeft),
    ids=("Qt.LeftToRight", "Qt.RightToLeft"),
    scope="class",
)
def fixture_direction(
    request: SubRequest,
) -> Qt.LayoutDirection:
    """Return the request.param to set the state at the fixture_option."""
    return cast(Qt.LayoutDirection, request.param)


@pytest.fixture(
    name="state",
    params=(
        QStyle.State_On | QStyle.State_Enabled,
        QStyle.State_On,
        QStyle.State_Enabled,
        QStyle.State_None,
    ),
    ids=(
        "QStyle.State_On | QStyle.State_Enabled",
        "QStyle.State_On",
        "QStyle.State_Enabled",
        "QStyle.State_None",
    ),
    scope="class",
)
def fixture_state(
    request: SubRequest,
) -> QStyle.State:
    """Return the request.param to set the state at the fixture_option."""
    return cast(QStyle.State, request.param)
