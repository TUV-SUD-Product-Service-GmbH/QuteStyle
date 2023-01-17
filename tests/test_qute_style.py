"""Tests for qute_style."""
# pylint: disable=protected-access
from __future__ import annotations

import contextlib
from random import randint
from typing import Generator

import pytest
from _pytest.fixtures import SubRequest
from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QBrush, QImage, QPainter, QPalette, QPen
from PySide6.QtWidgets import (
    QCheckBox,
    QProxyStyle,
    QStyle,
    QStyleOption,
    QStyleOptionButton,
    QStyleOptionViewItem,
    QWidget,
)
from pytestqt.qtbot import QtBot

from qute_style.dev.mocks import CallList, check_call, check_call_str
from qute_style.qute_style import QuteStyle, ToggleOptionButton

# Create a QApplication for all tests as we're using QPainter objects.
from qute_style.style import get_color

pytestmark = pytest.mark.usefixtures("qapp")


@pytest.mark.parametrize(
    "element",
    (
        QuteStyle.CE_Toggle,
        QuteStyle.ControlElement.CE_CheckBoxLabel,
        QuteStyle.ControlElement.CE_CheckBox,
        QuteStyle.ControlElement.CE_ItemViewItem,
    ),
    ids=(
        "QuteStyle.CE_Toggle",
        "QuteStyle.CE_CheckBoxLabel",
        "QuteStyle.CE_CheckBox",
        "QuteStyle.CE_ItemViewItem",
    ),
)
def test_draw_control(element: QStyle.ControlElement) -> None:
    """Test that drawControl calls the correct sub functions."""
    if method_name := {
        QuteStyle.CE_Toggle: "_draw_toggle",
        QuteStyle.ControlElement.CE_CheckBoxLabel: "_draw_check_box_label",
        QuteStyle.ControlElement.CE_CheckBox: "_draw_checkbox",
        QuteStyle.ControlElement.CE_ItemViewItem: None,
    }[element]:
        with check_call(QuteStyle, method_name):
            option = (
                ToggleOptionButton
                if element == QuteStyle.CE_Toggle
                else QStyleOptionButton
            )
            widget = (
                QCheckBox()
                if element == QuteStyle.ControlElement.CE_CheckBox
                else None
            )
            QuteStyle().drawControl(element, option(), QPainter(), widget)
    else:
        with check_call(QProxyStyle, "drawControl"):
            QuteStyle().drawControl(element, QStyleOption(), QPainter(), None)


def test_draw_check_box(style_option_button: QStyleOptionButton) -> None:
    """Test that drawing a QCheckBox draws the indicator and the label."""
    with check_call(QuteStyle, "_draw_indicator_checkbox"):
        with check_call(QuteStyle, "drawControl") as draw_control_calls:
            QuteStyle()._draw_checkbox(
                style_option_button, QPainter(), QCheckBox()
            )
    assert (
        draw_control_calls[0][0][1] == QStyle.ControlElement.CE_CheckBoxLabel
    )


def test_draw_checkbox_label(
    style_option_button: QStyleOptionButton, state: QStyle.StateFlag
) -> None:
    """Test that the Checkbox label is drawn with the correct color."""
    with check_call(QProxyStyle, "drawControl") as calls:
        QuteStyle()._draw_check_box_label(
            style_option_button, QPainter(), None
        )
    option = calls[0][0][2]
    role = QPalette.WindowText
    disabled_color = option.palette.color(QPalette.Disabled, role).name()
    if state & QStyle.StateFlag.State_Enabled:
        assert (
            disabled_color
            == QuteStyle()
            .standardPalette()
            .color(QPalette.Disabled, role)
            .name()
        )
    else:
        assert (
            disabled_color
            == option.palette.color(QPalette.Normal, role).name()
        )


@pytest.fixture(name="rect", scope="class")
def fixture_rect() -> QRect:
    """Return a randomly created QRect."""
    return QRect(
        randint(0, 10), randint(0, 10), randint(20, 40), randint(20, 40)
    )


class TestDrawIndicatorCheckbox:
    """Test drawing an indicator checkbox."""

    @staticmethod
    @pytest.fixture(name="calls", autouse=True, scope="class")
    def calls(
        rect: QRect, style_option_button: QStyleOptionButton
    ) -> CallList:
        """Call the method and return the calls to drawPrimitive."""
        with check_call(QProxyStyle, "subElementRect", rect):
            with check_call(QuteStyle, "drawPrimitive") as calls:
                QuteStyle()._draw_indicator_checkbox(
                    style_option_button, QPainter(), QWidget()
                )
        return calls

    @staticmethod
    def test_element(calls: CallList) -> None:
        """Test that the correct element is used."""
        assert calls[0][0][1] == QStyle.PrimitiveElement.PE_IndicatorCheckBox

    @staticmethod
    def test_rect(calls: CallList, rect: QRect) -> None:
        """Test the QRect is set correctly."""
        assert calls[0][0][2].rect == rect


@pytest.fixture(name="qute_style")
def fixture_qute_style() -> QuteStyle:
    """Generate a QuteStyle."""
    return QuteStyle()


@pytest.fixture(
    name="option",
    params=(True, False),
    ids=("With Children", "Without Children"),
)
def fixture_option(request: SubRequest) -> QStyleOption:
    """Generate a QStyleOption."""
    option = QStyleOption()
    option.state = (
        QStyle.StateFlag.State_Children
        if request.param
        else QStyle.StateFlag.State_Open
    )
    option.rect.Y = 5
    option.rect.X = 5
    return option


def test_get_branch_color(
    qute_style: QuteStyle, option: QStyleOption, painter: QPainter
) -> None:
    """Test _get_branch_color."""
    if option.state == option.state & QStyle.StateFlag.State_Children:
        assert qute_style._get_branch_color(option) == get_color("foreground")
        option.state = QStyle.StateFlag.State_MouseOver
        assert qute_style._get_branch_color(option) == get_color(
            "context_hover"
        )
    else:
        with check_call(QPainter, "drawPixmap", call_count=0):
            qute_style._draw_branch(option, painter)


def test_get_branch_icon(
    qute_style: QuteStyle, option: QStyleOption, painter: QPainter
) -> None:
    """Test _get_branch_color."""
    if option.state == option.state & QStyle.StateFlag.State_Children:
        assert (
            qute_style._get_branch_icon(option)
            == ":/svg_icons/arrow_right.svg"
        )
        option.state = QStyle.StateFlag.State_Open
        assert (
            qute_style._get_branch_icon(option) == ":/svg_icons/arrow_down.svg"
        )
    else:
        with check_call(QPainter, "drawPixmap", call_count=0):
            qute_style._draw_branch(option, painter)


# pylint: disable=redefined-outer-name
def test_draw_branches(
    qtbot: QtBot,
    qute_style: QuteStyle,
    option: QStyleOption,
    painter: QPainter,
) -> None:
    """Test the drawBranches Funktion."""
    with qtbot.captureExceptions() as exceptions:
        if option.state == option.state & QStyle.StateFlag.State_Children:
            with check_call(
                QuteStyle,
                "_get_branch_color",
                call_count=1
                if option.state
                == option.state & QStyle.StateFlag.State_Children
                else 0,
            ):
                with check_call(
                    QuteStyle,
                    "draw_pixmap",
                    call_count=1
                    if option.state
                    == option.state & QStyle.StateFlag.State_Children
                    else 0,
                ):
                    qute_style._draw_branch(option, painter)
        assert not exceptions


def test_draw_toggle(
    toggle_option_button: ToggleOptionButton, text: str | None
) -> None:
    """Test that a Toggle is drawn correctly."""
    with check_call(QuteStyle, "_draw_toggle_background"):
        with check_call(QuteStyle, "_draw_toggle_circle"):
            with check_call(
                QProxyStyle, "drawControl", call_count=1 if text else 0
            ):
                QuteStyle()._draw_toggle(
                    toggle_option_button, QPainter(), None
                )


@pytest.fixture(name="toggle_x", scope="class")
def fixture_toggle_x() -> int:
    """Return a fake x position for the toggle."""
    return randint(0, 10)


@pytest.fixture(scope="class")
def qtbot(request: SubRequest) -> QtBot:
    """Override qtbot fixture to allow class scope."""
    return QtBot(request)


@pytest.fixture(name="painter", scope="class")
def fixture_painter() -> Generator[QPainter, None, None]:
    """
    Create a QPainter with a 100x100 QImage to paint on.

    Since the QPainter does not take ownership of the QImage, it must be set
    into its own variable (so that it lives long enough).
    """
    image = QImage(100, 100, QImage.Format_RGB32)
    painter = QPainter(image)
    yield painter
    painter.end()


class TestDrawToggleCircle:
    """Test drawing the Toggle's circle."""

    @staticmethod
    @pytest.fixture(name="calls", autouse=True, scope="class")
    def calls(
        toggle_option_button: ToggleOptionButton,
        painter: QPainter,
        toggle_x: int,
    ) -> CallList:
        """Call the method and return the calls to drawPrimitive."""
        with check_call(QuteStyle.ToggleOptions, "toggle_x", toggle_x):
            with check_call(QPainter, "drawEllipse") as calls:
                QuteStyle()._draw_toggle_circle(toggle_option_button, painter)
        return calls

    @staticmethod
    def test_painter_reset(painter: QPainter) -> None:
        """Test that the painter is reset to its old values after painting."""
        assert painter.brush().style() == Qt.NoBrush
        assert painter.pen().style() == Qt.SolidLine

    @staticmethod
    def test_x_pos(position: int, calls: CallList, toggle_x: int) -> None:
        """Test that the x position of the circle is calculated correctly."""
        assert calls[0][0][1] == toggle_x + position

    @staticmethod
    def test_y_pos(calls: CallList) -> None:
        """Test that the y position of the circle is calculated correctly."""
        assert calls[0][0][2] == QuteStyle.ToggleOptions.CIRCLE_OFFSET

    @staticmethod
    def test_radius(calls: CallList) -> None:
        """Test that the circle is drawn with correct radius."""
        assert (
            calls[0][0][3]
            == calls[0][0][4]
            == QuteStyle.ToggleOptions.CIRCLE_SIZE
        )


class TestDrawToggleBackground:
    """Test drawing the Toggle's background."""

    @staticmethod
    @pytest.fixture(name="calls", autouse=True, scope="class")
    def calls(
        rect: QRect,
        toggle_option_button: ToggleOptionButton,
        painter: QPainter,
    ) -> CallList:
        """Call the method and return the calls to drawPrimitive."""
        with check_call(QuteStyle.ToggleOptions, "toggle_rect", rect):
            with check_call(QPainter, "drawRoundedRect") as calls:
                QuteStyle()._draw_toggle_background(
                    toggle_option_button, painter
                )
        return calls

    @staticmethod
    def test_painter_reset(painter: QPainter) -> None:
        """Test that the painter is reset to its old values after painting."""
        assert painter.brush().style() == Qt.NoBrush
        assert painter.pen().style() == Qt.SolidLine

    @staticmethod
    def test_toggle_rect(calls: CallList, rect: QRect) -> None:
        """Test that drawRoundedRect is called with the correct rect."""
        assert calls[0][0][1] == rect

    @staticmethod
    def test_radius(calls: CallList) -> None:
        """Test that the rounded rect is drawn with correct radius."""
        assert (
            calls[0][0][2]
            == calls[0][0][3]
            == QuteStyle.ToggleOptions.BACKGROUND_RECT_RADIUS
        )


class TestDrawPrimitive:
    """Test drawing a primitive element with qute_style."""

    @staticmethod
    def test_frame_focus_rect() -> None:
        """Test that drawing is disabled for a PE_FrameFocusRect."""
        with check_call(QProxyStyle, "drawPrimitive", call_count=0):
            QuteStyle().drawPrimitive(
                QuteStyle.PrimitiveElement.PE_FrameFocusRect,
                QStyleOption(),
                QPainter(),
                None,
            )

    @staticmethod
    def test_draw_branch(option: QStyleOption) -> None:
        """Test that drawing an IndicatorBranch is calling _draw_branch."""
        with check_call(QuteStyle, "_draw_branch"):
            QuteStyle().drawPrimitive(
                QuteStyle.PrimitiveElement.PE_IndicatorBranch,
                option,
                QPainter(),
            )

    @staticmethod
    def test_panel_item_view_item(
        style_option_view_item: QStyleOptionViewItem,
    ) -> None:
        """Test drawing an ItemViewItem calls _panel_draw_item_view_item."""
        with check_call(QuteStyle, "_panel_draw_item_view_item"):
            QuteStyle().drawPrimitive(
                QuteStyle.PrimitiveElement.PE_PanelItemViewItem,
                style_option_view_item,
                QPainter(),
                None,
            )

    @staticmethod
    def test_draw_primitive_indicator_checkbox(
        style_option_view_item: QStyleOptionViewItem,
    ) -> None:
        """Test drawing a checkbox calls _draw_primitive_indicator_checkbox."""
        with check_call(QuteStyle, "_draw_primitive_indicator_checkbox"):
            QuteStyle().drawPrimitive(
                QuteStyle.PrimitiveElement.PE_IndicatorCheckBox,
                style_option_view_item,
                QPainter(),
                None,
            )


def test_draw_primitive_indicator_checkbox(
    style_option_button: QStyleOptionButton, state: QStyle.StateFlag
) -> None:
    """Test that primitive indicator checkbox is drawn correctly."""
    with check_call(QuteStyle, "_draw_checkbox_background"):
        with check_call(QuteStyle, "_draw_checkbox_frame"):
            draw_check = (
                state & QStyle.StateFlag.State_On
                or state & QStyle.StateFlag.State_NoChange
            )
            with check_call(
                QuteStyle,
                "_draw_checkbox_check",
                call_count=1 if draw_check else 0,
            ):
                QuteStyle._draw_primitive_indicator_checkbox(
                    style_option_button, QPainter()
                )


@contextlib.contextmanager
def painter_save_mock(_: QPainter) -> Generator[None, None, None]:
    """
    Mock to disable the context manager to disable save of QPainter.

    This is necessary so that we can check if the QPainter was configured
    correctly.
    """
    yield


class TestDrawCheckBoxFrame:
    """Test drawing a checkbox's frame."""

    @staticmethod
    @pytest.fixture(scope="class", autouse=True)
    def calls(
        style_option_button: QStyleOptionButton, painter: QPainter
    ) -> CallList:
        """Test drawing a checkbox's frame."""
        with check_call_str(
            "qute_style.qute_style.painter_save", painter_save_mock
        ):
            with check_call(QPainter, "drawRoundedRect") as calls:
                QuteStyle()._draw_checkbox_frame(style_option_button, painter)
        return calls

    @staticmethod
    def test_pen(
        painter: QPainter, style_option_button: QStyleOptionButton
    ) -> None:
        """Check that the QPen is set correctly."""
        assert painter.pen() == QPen(
            QuteStyle._cb_frame_color(style_option_button)
        )

    @staticmethod
    def test_brush(painter: QPainter) -> None:
        """Check that the QBrush is set correctly."""
        assert painter.brush().style() == Qt.NoBrush

    @staticmethod
    def test_anti_aliasing(painter: QPainter) -> None:
        """Test that Antialiasing is enabled."""
        assert painter.renderHints() & QPainter.Antialiasing

    @staticmethod
    def test_rect(
        calls: CallList, style_option_button: QStyleOptionButton
    ) -> None:
        """Test that the QRect is set correctly."""
        assert calls[0][0][1] == style_option_button.rect.adjusted(
            1, 1, -1, -1
        )

    @staticmethod
    def test_rect_radius(calls: CallList) -> None:
        """Test that the QRect is set correctly."""
        assert calls[0][0][2] == calls[0][0][3] == 1


class TestDrawCheckBackground:
    """Test drawing a checkbox's background."""

    @staticmethod
    @pytest.fixture(scope="class", autouse=True)
    def calls(
        style_option_button: QStyleOptionButton, painter: QPainter
    ) -> CallList:
        """Test drawing a checkbox's background."""
        with check_call_str(
            "qute_style.qute_style.painter_save", painter_save_mock
        ):
            with check_call(QPainter, "drawRoundedRect") as calls:
                QuteStyle()._draw_checkbox_background(
                    style_option_button, painter
                )
        return calls

    @staticmethod
    def test_pen(painter: QPainter) -> None:
        """Check that the QPen is set correctly."""
        assert painter.pen().style() == Qt.NoPen

    @staticmethod
    def test_brush(
        painter: QPainter, style_option_button: QStyleOptionButton
    ) -> None:
        """Check that the QBrush is set correctly."""
        assert painter.brush() == QBrush(
            QuteStyle._cb_background_color(style_option_button)
        )

    @staticmethod
    def test_anti_aliasing(painter: QPainter) -> None:
        """Test that Antialiasing is enabled."""
        assert painter.renderHints() & QPainter.Antialiasing

    @staticmethod
    def test_rect(
        calls: CallList, style_option_button: QStyleOptionButton
    ) -> None:
        """Test that the QRect is set correctly."""
        assert calls[0][0][1] == style_option_button.rect

    @staticmethod
    def test_rect_radius(calls: CallList) -> None:
        """Test that the QRect is set correctly."""
        assert calls[0][0][2] == calls[0][0][3] == 2
