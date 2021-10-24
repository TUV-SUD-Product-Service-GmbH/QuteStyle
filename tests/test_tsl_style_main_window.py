"""Tests for the TSLStyledMainWindow."""
# pylint: disable=protected-access
from typing import List, Type, TypeVar, Union

import pytest
from _pytest.monkeypatch import MonkeyPatch
from pytestqt.qtbot import QtBot

from tsl import tsl_main_gui
from tsl.tsl_main_gui import TSLStyledMainWindow
from tsl.widgets.base_widgets import ColumnBaseWidget, MainWidget
from tsl.widgets.left_menu_button import LeftMenuButton
from tsl.widgets.title_button import TitleButton

# Store the constant for easier access
COL_W = TSLStyledMainWindow.MAX_COLUMN_WIDTH


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


class RightColumn(ColumnBaseWidget):
    """Test widget for the right column frame."""

    NAME = "TestRightColumnWidget"
    ICON = ":/svg_icons/heart_broken.svg"


class SecondRightColumn(ColumnBaseWidget):
    """Test widget for the right column frame."""

    NAME = "TestSecondRightColumnWidget"
    ICON = ":/svg_icons/heart_broken.svg"


class ColumnVisible(ColumnBaseWidget):
    """Column widget that is visible."""

    NAME = "ColumnVisible"
    ICON = ":/svg_icons/heart_broken.svg"
    GROUPS = ["RightTeam"]


class ColumnInvisible(ColumnBaseWidget):
    """Column widget that is invisible."""

    NAME = "ColumnInvisible"
    ICON = ":/svg_icons/heart_broken.svg"
    GROUPS = ["WrongTeam"]


class UpperLeftColumn(ColumnBaseWidget):
    """Upper test widget for the left column frame."""

    NAME = "LeftUpperRightColumnWidget"
    ICON = ":/svg_icons/heart_broken.svg"


class LowerLeftColumn(ColumnBaseWidget):
    """Lower test widget for the left column frame."""

    NAME = "LeftLowerRightColumnWidget"
    ICON = ":/svg_icons/heart_broken.svg"


class MainWindow(TSLStyledMainWindow):
    """Test implementation for TSLStyledMainWindow."""

    MAIN_WIDGET_CLASSES = [MainTest, MainVisible, MainInvisible]
    RIGHT_WIDGET_CLASSES = [RightColumn, SecondRightColumn]
    LEFT_WIDGET_CLASSES = [UpperLeftColumn, LowerLeftColumn]


class ColumnVisibleWindow(TSLStyledMainWindow):
    """TSLStyledMainWindow with visible and invisible columns."""

    MAIN_WIDGET_CLASSES = [MainTest, MainVisible, MainInvisible]
    RIGHT_WIDGET_CLASSES = [ColumnVisible, ColumnInvisible]
    LEFT_WIDGET_CLASSES = [ColumnVisible, ColumnInvisible]


class LeftColumnEmptyWindow(TSLStyledMainWindow):
    """TSLStyledMainWindow without left column widgets."""

    MAIN_WIDGET_CLASSES = [MainTest, MainVisible, MainInvisible]
    RIGHT_WIDGET_CLASSES = [RightColumn, SecondRightColumn]
    LEFT_WIDGET_CLASSES: List[Type[ColumnBaseWidget]] = []


class RightColumnEmptyWindow(TSLStyledMainWindow):
    """TSLStyledMainWindow without right column widgets."""

    MAIN_WIDGET_CLASSES = [MainTest, MainVisible, MainInvisible]
    RIGHT_WIDGET_CLASSES: List[Type[ColumnBaseWidget]] = []
    LEFT_WIDGET_CLASSES = [UpperLeftColumn, LowerLeftColumn]


class EmptyWindow(TSLStyledMainWindow):
    """TSLStyledMainWindow without any column widgets."""

    MAIN_WIDGET_CLASSES = [MainTest, MainVisible, MainInvisible]
    RIGHT_WIDGET_CLASSES: List[Type[ColumnBaseWidget]] = []
    LEFT_WIDGET_CLASSES: List[Type[ColumnBaseWidget]] = []


WindowT = TypeVar("WindowT", bound=TSLStyledMainWindow)


def create_new_main_window(
    qtbot: QtBot,
    monkeypatch: MonkeyPatch,
    window_class: Type[WindowT],
) -> WindowT:
    """Create and show a new TSLMainWindow."""

    def mock_get_user() -> str:
        return "RightTeam"

    monkeypatch.setattr(tsl_main_gui, "get_user_group_name", mock_get_user)
    widget = window_class(False, "", "", "1.0.0")
    qtbot.addWidget(widget)
    widget.show()
    qtbot.waitUntil(widget.isVisible)
    return widget


def test_opening_left(qtbot: QtBot, monkeypatch: MonkeyPatch) -> None:
    """Test opening and closing of left columns."""
    window = create_new_main_window(qtbot, monkeypatch, MainWindow)

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


@pytest.mark.parametrize("window_type", (MainWindow, LeftColumnEmptyWindow))
def test_opening_right(
    qtbot: QtBot,
    monkeypatch: MonkeyPatch,
    window_type: Type[TSLStyledMainWindow],
) -> None:
    """Test opening and closing of right columns."""
    window = create_new_main_window(qtbot, monkeypatch, window_type)

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


def test_switch_left_column(qtbot: QtBot, monkeypatch: MonkeyPatch) -> None:
    """Test switching the left column."""
    window = create_new_main_window(qtbot, monkeypatch, MainWindow)

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


@pytest.mark.parametrize("window_type", (MainWindow, RightColumnEmptyWindow))
def test_close_left_column(
    qtbot: QtBot,
    monkeypatch: MonkeyPatch,
    window_type: Type[TSLStyledMainWindow],
) -> None:
    """Test closing the column with the close button."""
    window = create_new_main_window(qtbot, monkeypatch, window_type)

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
    "window_type", (MainWindow, RightColumnEmptyWindow, LeftColumnEmptyWindow)
)
def test_no_widget_on_column(
    qtbot: QtBot,
    monkeypatch: MonkeyPatch,
    window_type: Type[
        Union[MainWindow, RightColumnEmptyWindow, LeftColumnEmptyWindow]
    ],
) -> None:
    """Test that TSLStyledMainWindow works with empty left or right column."""
    window = create_new_main_window(qtbot, monkeypatch, window_type)

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


def test_display_main_widgets(qtbot: QtBot, monkeypatch: MonkeyPatch) -> None:
    """Test display of widgets dependent on user group."""
    window = create_new_main_window(qtbot, monkeypatch, MainWindow)

    # Check that MainWidget and GroupTestRight are visible
    assert window._content.widget(0).__class__ is MainTest
    assert window._content.widget(1).__class__ is MainVisible
    # Check that GroupTestWrong is not visible
    assert window._content.count() == 2


def test_display_column_widgets(
    qtbot: QtBot, monkeypatch: MonkeyPatch
) -> None:
    """Test display of widgets dependent on user group."""
    window = create_new_main_window(qtbot, monkeypatch, ColumnVisibleWindow)

    # Check that one column widget is visible, the other not
    assert window._left_column.widget(ColumnVisible)
    with pytest.raises(ValueError):
        window._left_column.widget(ColumnInvisible)
    assert window._left_column._stacked_widget.count() == 1

    assert window._right_content.widget(0).__class__ is ColumnVisible
    assert window._right_content.count() == 1
