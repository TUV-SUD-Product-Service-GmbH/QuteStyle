"""Tests for homepage."""
# pylint: disable=protected-access
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFontMetrics
from PyQt5.QtWidgets import QStyleOption
from pytestqt.qtbot import QtBot

from qute_style.qute_style import QuteStyle
from qute_style.widgets.toggle import Toggle


def test_toggle_x(
    style_option_button: QStyleOption, direction: Qt.LayoutDirection
) -> None:
    """Test position and size of the UpdateWindow are stored and loaded."""
    if direction == Qt.LeftToRight:
        assert QuteStyle.ToggleOptions.toggle_x(style_option_button) == 0
    else:
        assert (
            QuteStyle.ToggleOptions.toggle_x(style_option_button)
            == style_option_button.rect.width()
            - QuteStyle.ToggleOptions.BOX_WIDTH
        )


def test_label_x(
    style_option_button: QStyleOption, direction: Qt.LayoutDirection
) -> None:
    """Test position and size of the UpdateWindow are stored and loaded."""
    if direction == Qt.LeftToRight:
        expected = (
            QuteStyle.ToggleOptions.BOX_WIDTH + QuteStyle.ToggleOptions.SPACER
        )
    else:
        expected = 0

    assert QuteStyle.ToggleOptions.label_x(style_option_button) == expected


def test_size_hint(qtbot: QtBot) -> None:
    """Test that the Toggle.sizeHint() works correctly."""
    with qtbot.captureExceptions() as exceptions:
        toggle = Toggle()
        width = QuteStyle.ToggleOptions.BOX_WIDTH
        assert toggle.sizeHint() == QSize(
            width, QuteStyle.ToggleOptions.BOX_HEIGHT
        )
        toggle.setText("Test")
        assert toggle.sizeHint() == QSize(
            width
            + QFontMetrics(toggle.font()).horizontalAdvance(toggle.text())
            + QuteStyle.ToggleOptions.SPACER,
            QuteStyle.ToggleOptions.BOX_HEIGHT,
        )
    assert not exceptions
