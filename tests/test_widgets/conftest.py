"""Configuration for widget tests."""
from random import choice, randint
from typing import Dict

import pytest
from _pytest.fixtures import SubRequest
from PyQt5.QtWidgets import QApplication
from pytestqt.qtbot import QtBot

from tsl.style import THEMES


@pytest.fixture(scope="class", name="qtbot")
def fixture_qtbot(
    qapp: QApplication, request: SubRequest  # pylint: disable=unused-argument
) -> QtBot:
    """Override QtBot default fixture for use with class scope."""
    return QtBot(request)


@pytest.fixture(name="theme_name", scope="session")
def fixture_theme_name() -> str:
    """Return a random theme name."""
    return list(THEMES)[randint(0, len(THEMES) - 1)]


@pytest.fixture(name="theme", scope="session")
def fixture_theme(theme_name: str) -> Dict[str, str]:
    """Return a random theme."""
    return THEMES[theme_name]


@pytest.fixture(name="color_name", scope="session")
def fixture_color_name(theme: Dict[str, str]) -> str:
    """Return a random color name."""
    return choice(list(theme))


@pytest.fixture(name="icon_path", scope="session")
def fixture_icon_path() -> str:
    """Return an icon path for a test icon."""
    return "tests/test_images/test_icon.svg"
