"""Test for style handling."""
import re

import pytest
from PySide6.QtCore import QSettings
from PySide6.QtWidgets import QWidget
from pytestqt.qtbot import QtBot

from qute_style.style import (
    DEFAULT_STYLE,
    THEMES,
    get_color,
    get_current_style,
    get_style,
    set_current_style,
)


@pytest.mark.style
def test_get_current_style() -> None:
    """Test that default style is returned when nothing is stored."""
    assert get_current_style() == DEFAULT_STYLE


@pytest.mark.style
def test_set_and_get_current_style() -> None:
    """Test setting and getting the current style."""
    style = next(iter(THEMES.keys()))
    set_current_style(style)
    assert get_current_style() == style


@pytest.mark.style
def test_get_current_style_fallback() -> None:
    """Check that the default style is returned when the stored is invalid."""
    QSettings().setValue("style", "INVALID_STYLE")
    assert QSettings().value("style") not in THEMES
    assert get_current_style() == DEFAULT_STYLE


@pytest.mark.style
@pytest.mark.parametrize("style", tuple(THEMES.keys()))
def test_get_style(qtbot: QtBot, style: str) -> None:
    """Test that a valid stylesheet is returned for every theme."""
    set_current_style(style)
    widget = QWidget()
    qtbot.addWidget(widget)
    style_sheet = get_style()
    widget.setStyleSheet(style_sheet)
    assert widget.styleSheet() == style_sheet


@pytest.mark.style
def test_get_color() -> None:
    """Test that every theme contains a valid color for every color key."""
    for theme, color_names in THEMES.items():
        set_current_style(theme)
        for color_name in color_names:
            color = get_color(color_name)
            assert re.match(r"^#(?:[0-9a-fA-F]{3}){1,2}$", color)
