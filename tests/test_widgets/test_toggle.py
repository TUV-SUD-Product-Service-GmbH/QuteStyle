"""Tests for homepage."""
# pylint: disable=protected-access
from typing import Any, cast

import PyQt5
import pytest
from _pytest.fixtures import SubRequest
from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtGui import QColor, QFontMetrics, QPainter, QPalette
from PyQt5.QtWidgets import QStyle, QStyleOption, QStyleOptionButton
from pytestqt.qtbot import QtBot

from tsl.dev.mocks import check_call
from tsl.style import get_color
from tsl.widgets.toggle import Toggle, ToggleStyle


def test_x_pos(option: QStyleOption, direction: Qt.LayoutDirection) -> None:
    """Test position and size of the UpdateWindow are stored and loaded."""
    if direction == Qt.LeftToRight:
        assert ToggleStyle._toggle_x(option) == 0
    else:
        assert (
            ToggleStyle._toggle_x(option)
            == option.rect.width() - ToggleStyle.ToggleOptions.BOX_WIDTH
        )


def test_x_pos_label(
    option: QStyleOption, direction: Qt.LayoutDirection
) -> None:
    """Test position and size of the UpdateWindow are stored and loaded."""
    if direction == Qt.LeftToRight:
        expected = (
            ToggleStyle.ToggleOptions.BOX_WIDTH
            + ToggleStyle.ToggleOptions.SPACER
        )
    else:
        expected = 0

    assert ToggleStyle._label_x(option) == expected


@pytest.fixture(name="option")
def fixture_option(
    direction: Qt.LayoutDirection, state: PyQt5.QtWidgets.QStyle
) -> QStyleOptionButton:
    """Create an option for testing."""
    option = QStyleOptionButton()
    option.direction = direction
    option.state = state  # type: ignore
    return option


@pytest.fixture(
    name="direction",
    params=(Qt.LeftToRight, Qt.RightToLeft),
    ids=("Qt.LeftToRight", "Qt.RightToLeft"),
)
def fixture_direction(
    request: SubRequest,
) -> Any:
    """Return the request.param to set the state at the fixture_option."""
    return request.param


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
)
def fixture_state(
    request: SubRequest,
) -> Any:
    """Return the request.param to set the state at the fixture_option."""
    return request.param


def test_background_color(option: QStyleOptionButton) -> None:
    """Test that the ToggleStyle.background_color() works correctly."""
    toggle_style = ToggleStyle()
    expected = toggle_style.standardPalette().color(
        QPalette.Normal, QPalette.Base
    )
    if not option.state & QStyle.State_Enabled:
        expected = toggle_style.standardPalette().color(
            QPalette.Inactive, QPalette.Base
        )
    elif option.state & QStyle.State_On:
        expected = QColor(get_color("context_color"))
    assert toggle_style.background_color(option) == expected


def test_toggle_color(option: QStyleOptionButton) -> None:
    """Test that the ToggleStyle.toggle_color() works correctly."""
    if option.state & QStyle.State_Enabled:
        assert ToggleStyle.toggle_color(option) == get_color("foreground")
    else:
        assert ToggleStyle.toggle_color(option) == get_color("fg_disabled")


def test_draw_control(qtbot: QtBot, option: QStyleOption) -> None:
    """Test that the ToggleStyle.drawControl() works correctly."""
    with qtbot.captureExceptions() as exceptions:

        toggle_style = ToggleStyle()
        painter = QPainter()
        widget = Toggle()

        with check_call(QPainter, "drawRoundedRect") as draw_rounded_rect_call:
            with check_call(QPainter, "drawEllipse") as draw_ellipse_call:
                toggle_style.drawControl(
                    QStyle.CE_CheckBox, option, painter, widget
                )
                assert draw_rounded_rect_call[0][0][1] == QRect(
                    toggle_style._toggle_x(option),
                    0,
                    toggle_style.ToggleOptions.BOX_WIDTH,
                    toggle_style.ToggleOptions.BOX_HEIGHT,
                )
                assert draw_rounded_rect_call[0][0][2] == 12
                assert draw_rounded_rect_call[0][0][3] == 12
                assert draw_ellipse_call[0][0][1] == toggle_style._toggle_x(
                    option
                ) + cast(int, widget.position)
                assert (
                    draw_ellipse_call[0][0][2]
                    == toggle_style.ToggleOptions.CIRCLE_OFFSET
                )
                assert (
                    draw_ellipse_call[0][0][3]
                    == toggle_style.ToggleOptions.CIRCLE_SIZE
                )
                assert (
                    draw_ellipse_call[0][0][4]
                    == toggle_style.ToggleOptions.CIRCLE_SIZE
                )
        assert not exceptions


def test_size_hint(qtbot: QtBot) -> None:
    """Test that the Toggle.sizeHint() works correctly."""
    with qtbot.captureExceptions() as exceptions:
        toggle = Toggle()
        width = ToggleStyle.ToggleOptions.BOX_WIDTH
        assert toggle.sizeHint() == QSize(
            width, ToggleStyle.ToggleOptions.BOX_HEIGHT
        )
        toggle.setText("Test")
        assert toggle.sizeHint() == QSize(
            width
            + QFontMetrics(toggle.font()).horizontalAdvance(toggle.text())
            + ToggleStyle.ToggleOptions.SPACER,
            ToggleStyle.ToggleOptions.BOX_HEIGHT,
        )
    assert not exceptions
