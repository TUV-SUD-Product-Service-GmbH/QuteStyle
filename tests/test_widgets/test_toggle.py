"""Tests for homepage."""
# pylint: disable=protected-access
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QStyleOption
from pytestqt.qtbot import QtBot

from tsl.tsl_style import TSLStyle
from tsl.widgets.toggle import Toggle


def test_toggle_x(
    style_option_button: QStyleOption, direction: Qt.LayoutDirection
) -> None:
    """Test position and size of the UpdateWindow are stored and loaded."""
    if direction == Qt.LeftToRight:
        assert TSLStyle.ToggleOptions.toggle_x(style_option_button) == 0
    else:
        assert (
            TSLStyle.ToggleOptions.toggle_x(style_option_button)
            == style_option_button.rect.width()
            - TSLStyle.ToggleOptions.BOX_WIDTH
        )


def test_label_x(
    style_option_button: QStyleOption, direction: Qt.LayoutDirection
) -> None:
    """Test position and size of the UpdateWindow are stored and loaded."""
    if direction == Qt.LeftToRight:
        expected = (
            TSLStyle.ToggleOptions.BOX_WIDTH + TSLStyle.ToggleOptions.SPACER
        )
    else:
        expected = 0

    assert TSLStyle.ToggleOptions.label_x(style_option_button) == expected


def test_size_hint(qtbot: QtBot) -> None:
    """Test that the Toggle.sizeHint() works correctly."""
    with qtbot.captureExceptions() as exceptions:
        toggle = Toggle()
        width = TSLStyle.ToggleOptions.BOX_WIDTH
        assert toggle.sizeHint() == QSize(
            width, TSLStyle.ToggleOptions.BOX_HEIGHT
        )
        toggle.setText("Test")
        assert toggle.sizeHint() == QSize(
            width
            + QFontMetrics(toggle.font()).horizontalAdvance(toggle.text())
            + TSLStyle.ToggleOptions.SPACER,
            TSLStyle.ToggleOptions.BOX_HEIGHT,
        )
    assert not exceptions
