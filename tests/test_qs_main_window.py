"""Tests for the QuteStyleMainWindow."""
# pylint: disable=protected-access
import logging
from typing import List, Type, Union, cast

import pytest
from PySide6 import QtWidgets
from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication
from pytestqt.qtbot import QtBot

from qute_style.dev.mocks import check_call
from qute_style.qs_main_window import AppData, QuteStyleMainWindow
from qute_style.widgets.base_widgets import BaseWidget, MainWidget
from qute_style.widgets.left_column import LeftColumn
from qute_style.widgets.left_menu_button import LeftMenuButton
from qute_style.widgets.title_button import TitleButton

log = logging.getLogger(f"tests.{__name__}")  # pylint: disable=invalid-name

# Store the constant for easier access
COL_W = QuteStyleMainWindow.MAX_COLUMN_WIDTH


class MainTest(MainWidget):
    """Test widget for the Main content area."""

    NAME = "TestMainWidget"
    ICON = ":/svg_icons/heart_broken.svg"


class MainVisible(MainWidget):
    """MainWidget that is visible."""

    NAME = "MainVisible"
    ICON = ":/svg_icons/heart_broken.svg"
    GROUPS = ["RightTeam"]


class MainInvisible(MainWidget):
    """MainWidget that is invisible."""

    NAME = "MainInvisible"
    ICON = ":/svg_icons/heart_broken.svg"
    GROUPS = ["WrongTeam"]


class RightColumn(BaseWidget):
    """Test widget for the right column frame."""

    NAME = "TestRightColumnWidget"
    ICON = ":/svg_icons/heart_broken.svg"


class SecondRightColumn(BaseWidget):
    """Test widget for the right column frame."""

    NAME = "TestSecondRightColumnWidget"
    ICON = ":/svg_icons/heart_broken.svg"


class ColumnVisible(BaseWidget):
    """Column widget that is visible."""

    NAME = "ColumnVisible"
    ICON = ":/svg_icons/heart_broken.svg"
    GROUPS = ["RightTeam"]


class ColumnInvisible(BaseWidget):
    """Column widget that is invisible."""

    NAME = "ColumnInvisible"
    ICON = ":/svg_icons/heart_broken.svg"
    GROUPS = ["WrongTeam"]


class UpperLeftColumn(BaseWidget):
    """Upper test widget for the left column frame."""

    NAME = "LeftUpperRightColumnWidget"
    ICON = ":/svg_icons/heart_broken.svg"


class LowerLeftColumn(BaseWidget):
    """Lower test widget for the left column frame."""

    NAME = "LeftLowerRightColumnWidget"
    ICON = ":/svg_icons/heart_broken.svg"


class StyledMainWindow(QuteStyleMainWindow):
    """Test implementation for QuteStyleMainWindow."""

    MAIN_WIDGET_CLASSES = [MainTest, MainVisible, MainInvisible]
    RIGHT_WIDGET_CLASSES = [RightColumn, SecondRightColumn]
    LEFT_WIDGET_CLASSES = [UpperLeftColumn, LowerLeftColumn]


class ColumnVisibleWindowStyled(QuteStyleMainWindow):
    """QuteStyleMainWindow with visible and invisible columns."""

    MAIN_WIDGET_CLASSES = [MainTest, MainVisible, MainInvisible]
    RIGHT_WIDGET_CLASSES = [ColumnVisible, ColumnInvisible]
    LEFT_WIDGET_CLASSES = [ColumnVisible, ColumnInvisible]


class LeftColumnEmptyWindowStyled(QuteStyleMainWindow):
    """QuteStyleMainWindow without left column widgets."""

    MAIN_WIDGET_CLASSES = [MainTest, MainVisible, MainInvisible]
    RIGHT_WIDGET_CLASSES = [RightColumn, SecondRightColumn]
    LEFT_WIDGET_CLASSES: List[Type[BaseWidget]] = []


class RightColumnEmptyWindowStyled(QuteStyleMainWindow):
    """QuteStyleMainWindow without right column widgets."""

    MAIN_WIDGET_CLASSES = [MainTest, MainVisible, MainInvisible]
    RIGHT_WIDGET_CLASSES: List[Type[BaseWidget]] = []
    LEFT_WIDGET_CLASSES = [UpperLeftColumn, LowerLeftColumn]


class EmptyWindowStyled(QuteStyleMainWindow):
    """QuteStyleMainWindow without any column widgets."""

    MAIN_WIDGET_CLASSES = [MainTest, MainVisible, MainInvisible]
    RIGHT_WIDGET_CLASSES: List[Type[BaseWidget]] = []
    LEFT_WIDGET_CLASSES: List[Type[BaseWidget]] = []


def create_new_main_window(
    qtbot: QtBot,
    window_class: Type[QuteStyleMainWindow],
) -> QuteStyleMainWindow:
    """Create and show a new QuteStyleMainWindow."""
    widget = window_class(
        AppData("TestApp", "1.0.0", ":/svg_icons/no_icon.svg")
    )
    qtbot.addWidget(widget)
    widget.show()
    qtbot.waitUntil(widget.isVisible)
    return widget


def test_opening_left(qtbot: QtBot) -> None:
    """Test opening and closing of left columns."""
    window = create_new_main_window(qtbot, StyledMainWindow)

    # Initially, nothing is in progress.
    assert window._check_is_opening(window._left_column_frame) is None

    # When calling the slot to open the left column, animation is in progress
    # and column is opening (True)
    with qtbot.waitSignal(window._group.finished):
        window.on_left_column(UpperLeftColumn)
        assert window._check_is_opening(window._left_column_frame) is True
    assert window._left_column_frame.width() == COL_W
    assert window._left_menu._button(UpperLeftColumn)._is_active
    assert not window._title_bar._button(RightColumn)._is_active

    # After the animation has finished, again nothing is in progress.
    assert window._check_is_opening(window._left_column_frame) is None

    # When closing the column (by opening the right column), the animation is
    # in progress but it's closing (False)
    with qtbot.waitSignal(window._group.finished):
        window.on_right_column(RightColumn)
        assert window._check_is_opening(window._left_column_frame) is False
    assert window._left_column_frame.width() == 0
    assert not window._left_menu._button(UpperLeftColumn)._is_active
    assert window._title_bar._button(RightColumn)._is_active

    # After the animation has finished, again nothing is in progress.
    assert window._check_is_opening(window._left_column_frame) is None


@pytest.mark.parametrize(
    "window_type", (StyledMainWindow, LeftColumnEmptyWindowStyled)
)
def test_opening_right(
    qtbot: QtBot,
    window_type: Type[QuteStyleMainWindow],
) -> None:
    """Test opening and closing of right columns."""
    window = create_new_main_window(qtbot, window_type)

    # Initially, nothing is in progress.
    assert window._check_is_opening(window._right_column_frame) is None

    # When calling the slot to open the left column, animation is in progress
    # and column is opening (True)
    with qtbot.waitSignal(window._group.finished):
        window.on_right_column(RightColumn)
        assert window._check_is_opening(window._right_column_frame) is True
    assert window._right_column_frame.width() == COL_W
    assert window._title_bar._button(RightColumn)._is_active

    # After the animation has finished, again nothing is in progress.
    assert window._check_is_opening(window._right_column_frame) is None

    # When closing the column (by opening the right column), the animation is
    # in progress but it's closing (False)
    with qtbot.waitSignal(window._group.finished):
        window.on_right_column(RightColumn)
        assert window._check_is_opening(window._right_column_frame) is False
    assert window._right_column_frame.width() == 0
    assert not window._title_bar._button(RightColumn)._is_active

    # After the animation has finished, again nothing is in progress.
    assert window._check_is_opening(window._right_column_frame) is None


def test_switch_left_column(qtbot: QtBot) -> None:
    """Test switching the left column."""
    window = create_new_main_window(qtbot, StyledMainWindow)

    # Open the LeftColumn for the first widget
    with qtbot.waitSignal(window._group.finished):
        window.on_left_column(UpperLeftColumn)
        assert window._check_is_opening(window._left_column_frame) is True
    assert window._left_column_frame.width() == COL_W
    assert window._left_column._title_label.text() == UpperLeftColumn.NAME

    # Switch to the second widget (no animation is shown, column is open).
    with qtbot.assertNotEmitted(window._group.finished):
        window.on_left_column(LowerLeftColumn)
    assert window._left_column._title_label.text() == LowerLeftColumn.NAME

    # Close the LeftColumn with the button for the second widget.
    with qtbot.waitSignal(window._group.finished):
        window.on_left_column(LowerLeftColumn)
        assert window._check_is_opening(window._left_column_frame) is False
    assert window._left_column_frame.width() == 0

    # Now switch the widget AND open the left column again
    with qtbot.waitSignal(window._group.finished):
        window.on_left_column(UpperLeftColumn)
        assert window._check_is_opening(window._left_column_frame) is True
    assert window._left_column_frame.width() == COL_W
    assert window._left_column._title_label.text() == UpperLeftColumn.NAME


@pytest.mark.parametrize(
    "window_type", (StyledMainWindow, RightColumnEmptyWindowStyled)
)
def test_close_left_column(
    qtbot: QtBot,
    window_type: Type[QuteStyleMainWindow],
) -> None:
    """Test closing the column with the close button."""
    window = create_new_main_window(qtbot, window_type)

    # Open the LeftColumn for the first widget
    with qtbot.waitSignal(window._group.finished):
        window.on_left_column(UpperLeftColumn)
    assert window._left_column_frame.width() == COL_W

    # Close the LeftColumn by pressing the close button (call the slot)
    with qtbot.waitSignal(window._group.finished):
        window.on_close_left_column()
    assert window._left_column_frame.width() == 0
    assert not window._left_menu._button(UpperLeftColumn)._is_active


@pytest.mark.parametrize(
    "window_type",
    (
        StyledMainWindow,
        RightColumnEmptyWindowStyled,
        LeftColumnEmptyWindowStyled,
    ),
)
def test_no_widget_on_column(
    qtbot: QtBot,
    window_type: Type[
        Union[
            StyledMainWindow,
            RightColumnEmptyWindowStyled,
            LeftColumnEmptyWindowStyled,
        ]
    ],
) -> None:
    """Test that QuteStyleMainWindow works with empty left or right column."""
    window = create_new_main_window(qtbot, window_type)

    if not window.RIGHT_WIDGET_CLASSES:
        for title_button in window._title_bar.findChildren(TitleButton):
            assert title_button.widget_class is None

    if not window.LEFT_WIDGET_CLASSES:
        assert window._left_menu._bottom_layout.count() == 0
        for left_button in window._left_menu.findChildren(LeftMenuButton):
            assert (
                left_button.widget_class is None
                or left_button.widget_class in window.MAIN_WIDGET_CLASSES
            )


def test_title_bar_text(qtbot: QtBot) -> None:
    """Test title bar text."""
    window = create_new_main_window(qtbot, StyledMainWindow)
    assert window._title_bar.title_bar_text == "TestApp - TestMainWidget"
    window._title_bar.title_bar_text = "Test - App"
    assert window._title_bar.title_bar_text == "Test - App"


def test_maximize_mode_setting_after_restart(qtbot: QtBot) -> None:
    """Test correct storage of maximize setting."""
    window = create_new_main_window(qtbot, StyledMainWindow)
    window.showMaximized()
    window.close()

    window = create_new_main_window(qtbot, StyledMainWindow)
    assert window.isMaximized()

    window.showNormal()
    window.close()

    window = create_new_main_window(qtbot, StyledMainWindow)
    assert not window.isMaximized()


def test_maximize_mode(qtbot: QtBot) -> None:
    """Test maximize mode."""
    window = create_new_main_window(qtbot, StyledMainWindow)
    window.showMaximized()

    app = cast(QApplication, QtWidgets.QApplication.instance())
    screen = app.primaryScreen()
    rect = screen.availableGeometry()
    log.debug("Available Geometry: %d x %d", rect.width(), rect.height())

    assert window.isMaximized()
    assert window._title_bar.maximize_button.tooltip_text == "Verkleinern"
    assert window.width() == rect.width()
    assert window.height() == rect.height()
    for grip in window._grips:
        assert not grip.isEnabled()

    qtbot.mouseClick(
        window._title_bar.maximize_button, Qt.MouseButton.LeftButton
    )
    assert not window.isMaximized()
    assert window._title_bar.maximize_button.tooltip_text == "Maximieren"
    for grip in window._grips:
        assert grip.isEnabled()

    qtbot.mouseClick(
        window._title_bar.maximize_button, Qt.MouseButton.LeftButton
    )
    assert window.isMaximized()

    window.showFullScreen()
    assert window.isFullScreen()
    size = screen.size()
    log.debug("Screen size: %d x %d", rect.width(), rect.height())
    assert window.width() == size.width()
    assert window.height() == size.height()

    window.showNormal()
    assert window.windowState() == Qt.WindowState.WindowNoState
    assert window._title_bar.maximize_button.tooltip_text == "Maximieren"


def test_maximize_event_handling(qtbot: QtBot) -> None:
    """Test maximize mode event handling."""
    window = create_new_main_window(qtbot, StyledMainWindow)
    window.showNormal()
    with qtbot.waitSignal(window._title_bar.maximize) as signal:
        window._title_bar.eventFilter(
            window._title_bar._title_label,
            QEvent(QEvent.Type.MouseButtonDblClick),
        )
        assert signal.signal_triggered
    assert window.isMaximized()

    # try to send move event while mouse double click still not finished
    with qtbot.waitSignal(
        window._title_bar.move_window, timeout=1000, raising=False
    ) as signal:
        window._title_bar.eventFilter(
            window._title_bar._title_label,
            QMouseEvent(
                QEvent.Type.MouseMove,
                QPointF(1, 1),
                QPointF(1, 1),
                Qt.MouseButton.LeftButton,
                Qt.MouseButton.LeftButton,
                Qt.KeyboardModifier.NoModifier,
            ),
        )
        assert not signal.signal_triggered

    # complete mouse double click
    window._title_bar.eventFilter(
        window._title_bar._title_label, QEvent(QEvent.Type.MouseButtonRelease)
    )

    # test that moving is now possible
    with qtbot.waitSignal(window._title_bar.move_window) as signal:
        window._title_bar.eventFilter(
            window._title_bar._title_label,
            QMouseEvent(
                QEvent.Type.MouseMove,
                QPointF(1, 1),
                QPointF(1, 1),
                Qt.MouseButton.LeftButton,
                Qt.MouseButton.LeftButton,
                Qt.KeyboardModifier.NoModifier,
            ),
        )
        assert signal.signal_triggered


@pytest.mark.parametrize("visible", [True, False])
def test_on_main_widget_settings(qtbot: QtBot, visible: bool) -> None:
    """Test that settings are display when user clicked on main widget."""
    window = create_new_main_window(qtbot, StyledMainWindow)
    if visible:
        window._left_column_frame.setFixedWidth(
            StyledMainWindow.MAX_COLUMN_WIDTH
        )
    with check_call(
        LeftColumn, "handle_settings_display", call_count=1 if visible else 0
    ):
        window.on_main_widget(MainTest)


def test_on_left_column_settings(qtbot: QtBot) -> None:
    """Test that settings are display when user clicked on left column."""
    window = create_new_main_window(qtbot, StyledMainWindow)

    with check_call(LeftColumn, "handle_settings_display"):
        window.on_left_column(UpperLeftColumn)
