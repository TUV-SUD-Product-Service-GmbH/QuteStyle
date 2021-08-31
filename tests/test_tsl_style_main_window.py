"""Tests for the TSLStyledMainWindow."""
# pylint: disable=protected-access
from pytestqt.qtbot import QtBot

from tsl.tsl_main_gui import TSLStyledMainWindow
from tsl.widgets.base_widgets import ColumnBaseWidget, MainWidget

# Store the constant for easier access
COL_W = TSLStyledMainWindow.MAX_COLUMN_WIDTH


class MainTest(MainWidget):
    """Test widget for the Main content area."""

    NAME = "TestMainWidget"
    ICON = ":/svg_icons/icon_heart.svg"


class RightColumn(ColumnBaseWidget):
    """Test widget for the right column frame."""

    NAME = "TestRightColumnWidget"
    ICON = ":/svg_icons/icon_heart.svg"


class UpperLeftColumn(ColumnBaseWidget):
    """Upper test widget for the left column frame."""

    NAME = "LeftUpperRightColumnWidget"
    ICON = ":/svg_icons/icon_heart.svg"


class LowerLeftColumn(ColumnBaseWidget):
    """Lower test widget for the left column frame."""

    NAME = "LeftLowerRightColumnWidget"
    ICON = ":/svg_icons/icon_heart.svg"


class MainWindow(TSLStyledMainWindow):
    """Test implementation for TSLStyledMainWindow."""

    MAIN_WIDGET_CLASSES = [MainTest]
    RIGHT_WIDGET_CLASS = RightColumn
    LEFT_WIDGET_CLASSES = [
        UpperLeftColumn,
        LowerLeftColumn,
    ]


def create_new_main_window(qtbot: QtBot) -> TSLStyledMainWindow:
    """Create and show a new TSLMainWindow."""
    widget = MainWindow(False, "", "", "1.0.0")
    qtbot.addWidget(widget)
    widget.show()
    qtbot.waitUntil(widget.isVisible)
    return widget


def test_opening(qtbot: QtBot) -> None:
    """Test opening and closing of columns."""
    window = create_new_main_window(qtbot)

    # Initially, nothing is in progress.
    assert window._check_is_opening(window._left_column_frame) is None

    # When calling the slot to open the left column, animation is in progress
    # and column is opening (True)
    with qtbot.waitSignal(window._group.finished):
        window.on_left_column(UpperLeftColumn)
        assert window._check_is_opening(window._left_column_frame) is True
    assert window._left_column_frame.width() == COL_W
    assert window._left_menu._button(UpperLeftColumn)._is_active
    assert not window._title_bar._right_column_button._is_active

    # After the animation has finished, again nothing is in progress.
    assert window._check_is_opening(window._left_column_frame) is None

    # When closing the column (by opening the right column), the animation is
    # in progress but it's closing (False)
    with qtbot.waitSignal(window._group.finished):
        window.on_right_column()
        assert window._check_is_opening(window._left_column_frame) is False
    assert window._left_column_frame.width() == 0
    assert not window._left_menu._button(UpperLeftColumn)._is_active
    assert window._title_bar._right_column_button._is_active

    # After the animation has finished, again nothing is in progress.
    assert window._check_is_opening(window._left_column_frame) is None


def test_switch_left_column(qtbot: QtBot) -> None:
    """Test switching the left column."""
    window = create_new_main_window(qtbot)

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


def test_close_left_column(qtbot: QtBot) -> None:
    """Test closing the column with the close button."""
    window = create_new_main_window(qtbot)

    # Open the LeftColumn for the first widget
    with qtbot.waitSignal(window._group.finished):
        window.on_left_column(UpperLeftColumn)
    assert window._left_column_frame.width() == COL_W

    # Close the LeftColumn by pressing the close button (call the slot)
    with qtbot.waitSignal(window._group.finished):
        window.on_close_left_column()
    assert window._left_column_frame.width() == 0
    assert not window._left_menu._button(UpperLeftColumn)._is_active
