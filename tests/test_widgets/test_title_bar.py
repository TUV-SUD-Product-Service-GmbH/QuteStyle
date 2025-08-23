"""Tests for TitleBar."""

import pytest
from PySide6.QtCore import QEvent, QPoint, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QWidget
from pytestqt.qtbot import QtBot

from qute_style.widgets.base_widgets import BaseWidget
from qute_style.widgets.title_bar import TitleBar
from qute_style.widgets.title_button import TitleButton


# Mock widget class for testing
class MockRightWidget(BaseWidget):
    """Mock widget for testing right column buttons."""

    NAME = "Mock Widget"
    ICON = ":/svg_icons/info.svg"

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize mock widget."""
        super().__init__(parent)


def test_title_bar_initialization(qtbot: QtBot) -> None:
    """Test TitleBar initialization."""
    parent = QWidget()
    app_parent = QWidget()
    qtbot.addWidget(parent)
    qtbot.addWidget(app_parent)

    title_bar = TitleBar(
        parent=parent,
        app_parent=app_parent,
        right_widget_classes=[MockRightWidget],
        name="Test Application",
        logo=":/svg_images/logo_qute_style.svg",
        debug_text="Debug",
    )
    qtbot.addWidget(title_bar)

    # Test basic properties
    assert title_bar.height() == 40
    assert title_bar.objectName() == "bg_two_frame"
    assert title_bar.title_bar_text == "Test Application"


def test_title_bar_text_property(qtbot: QtBot) -> None:
    """Test title_bar_text property getter and setter."""
    parent = QWidget()
    app_parent = QWidget()
    qtbot.addWidget(parent)
    qtbot.addWidget(app_parent)

    title_bar = TitleBar(
        parent=parent,
        app_parent=app_parent,
        right_widget_classes=[],
        name="Initial Title",
        logo=":/svg_images/logo_qute_style.svg",
    )
    qtbot.addWidget(title_bar)

    assert title_bar.title_bar_text == "Initial Title"
    title_bar.title_bar_text = "New Title"
    assert title_bar.title_bar_text == "New Title"


def test_title_bar_contains_buttons(qtbot: QtBot) -> None:
    """Test that TitleBar contains expected buttons."""
    parent = QWidget()
    app_parent = QWidget()
    qtbot.addWidget(parent)
    qtbot.addWidget(app_parent)

    title_bar = TitleBar(
        parent=parent,
        app_parent=app_parent,
        right_widget_classes=[MockRightWidget],
        name="Test Application",
        logo=":/svg_images/logo_qute_style.svg",
    )
    qtbot.addWidget(title_bar)

    buttons = title_bar.findChildren(TitleButton)

    # Should have: mock right widget button, minimize, maximize, close
    assert len(buttons) == 4

    # Check that maximize button is accessible
    assert hasattr(title_bar, "maximize_button")
    assert isinstance(title_bar.maximize_button, TitleButton)


def test_title_bar_event_filter_double_click(qtbot: QtBot) -> None:
    """Test that double-clicking the title label emits maximize signal."""
    parent = QWidget()
    app_parent = QWidget()
    qtbot.addWidget(parent)
    qtbot.addWidget(app_parent)

    title_bar = TitleBar(
        parent=parent,
        app_parent=app_parent,
        right_widget_classes=[],
        name="Test Application",
        logo=":/svg_images/logo_qute_style.svg",
    )
    qtbot.addWidget(title_bar)

    with qtbot.waitSignal(title_bar.maximize):
        event = QMouseEvent(
            QEvent.Type.MouseButtonDblClick,
            QPoint(10, 10),
            QPoint(100, 100),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )
        title_bar.eventFilter(title_bar._title_label, event)


def test_title_bar_event_filter_mouse_press(qtbot: QtBot) -> None:
    """Test that mouse press emits start_move signal."""
    parent = QWidget()
    app_parent = QWidget()
    qtbot.addWidget(parent)
    qtbot.addWidget(app_parent)

    title_bar = TitleBar(
        parent=parent,
        app_parent=app_parent,
        right_widget_classes=[],
        name="Test Application",
        logo=":/svg_images/logo_qute_style.svg",
    )
    qtbot.addWidget(title_bar)

    with qtbot.waitSignal(title_bar.start_move):
        event = QMouseEvent(
            QEvent.Type.MouseButtonPress,
            QPoint(10, 10),
            QPoint(100, 100),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )
        title_bar.eventFilter(title_bar._title_label, event)


def test_title_bar_event_filter_mouse_move(qtbot: QtBot) -> None:
    """Test that mouse move with button pressed emits move_window signal."""
    parent = QWidget()
    app_parent = QWidget()
    qtbot.addWidget(parent)
    qtbot.addWidget(app_parent)

    title_bar = TitleBar(
        parent=parent,
        app_parent=app_parent,
        right_widget_classes=[],
        name="Test Application",
        logo=":/svg_images/logo_qute_style.svg",
    )
    qtbot.addWidget(title_bar)

    # First simulate mouse press to reset double click state
    press_event = QMouseEvent(
        QEvent.Type.MouseButtonPress,
        QPoint(10, 10),
        QPoint(100, 100),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )
    title_bar.eventFilter(title_bar._title_label, press_event)

    with qtbot.waitSignal(title_bar.move_window):
        move_event = QMouseEvent(
            QEvent.Type.MouseMove,
            QPoint(15, 15),
            QPoint(105, 105),
            Qt.MouseButton.NoButton,
            Qt.MouseButton.LeftButton,  # Button is held down
            Qt.KeyboardModifier.NoModifier,
        )
        title_bar.eventFilter(title_bar._title_label, move_event)


def test_title_bar_event_filter_ignores_other_objects(qtbot: QtBot) -> None:
    """Test that event filter ignores events from other objects."""
    parent = QWidget()
    app_parent = QWidget()
    qtbot.addWidget(parent)
    qtbot.addWidget(app_parent)

    title_bar = TitleBar(
        parent=parent,
        app_parent=app_parent,
        right_widget_classes=[],
        name="Test Application",
        logo=":/svg_images/logo_qute_style.svg",
    )
    qtbot.addWidget(title_bar)

    other_widget = QWidget()
    qtbot.addWidget(other_widget)  # Ensure it's properly managed

    event = QMouseEvent(
        QEvent.Type.MouseButtonDblClick,
        QPoint(10, 10),
        QPoint(100, 100),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )

    # Should return False for objects that aren't the icon or title label
    result = title_bar.eventFilter(other_widget, event)
    assert result is False

    # Test with icon and title label to verify they are handled
    with qtbot.waitSignal(title_bar.maximize):
        title_result = title_bar.eventFilter(title_bar._title_label, event)

    with qtbot.waitSignal(title_bar.maximize):
        icon_result = title_bar.eventFilter(title_bar._icon, event)

    # Should handle events from these objects
    assert title_result is True
    assert icon_result is True


def test_title_bar_set_maximized_true(qtbot: QtBot) -> None:
    """Test that set_maximized(True) changes the maximize button icon."""
    parent = QWidget()
    app_parent = QWidget()
    qtbot.addWidget(parent)
    qtbot.addWidget(app_parent)

    title_bar = TitleBar(
        parent=parent,
        app_parent=app_parent,
        right_widget_classes=[],
        name="Test Application",
        logo=":/svg_images/logo_qute_style.svg",
    )
    qtbot.addWidget(title_bar)

    title_bar.set_maximized(True)

    # The tooltip should change to "Verkleinern"
    assert "Verkleinern" in title_bar.maximize_button.tooltip_text


def test_title_bar_set_maximized_false(qtbot: QtBot) -> None:
    """Test that set_maximized(False) changes the maximize button icon."""
    parent = QWidget()
    app_parent = QWidget()
    qtbot.addWidget(parent)
    qtbot.addWidget(app_parent)

    title_bar = TitleBar(
        parent=parent,
        app_parent=app_parent,
        right_widget_classes=[],
        name="Test Application",
        logo=":/svg_images/logo_qute_style.svg",
    )
    qtbot.addWidget(title_bar)

    title_bar.set_maximized(False)

    # The tooltip should change to "Maximieren"
    assert "Maximieren" in title_bar.maximize_button.tooltip_text


def test_title_bar_right_column_button_signal(qtbot: QtBot) -> None:
    """Test that clicking right column button emits signal."""
    parent = QWidget()
    app_parent = QWidget()
    qtbot.addWidget(parent)
    qtbot.addWidget(app_parent)

    title_bar = TitleBar(
        parent=parent,
        app_parent=app_parent,
        right_widget_classes=[MockRightWidget],
        name="Test Application",
        logo=":/svg_images/logo_qute_style.svg",
    )
    qtbot.addWidget(title_bar)

    # Find the mock widget button
    buttons = title_bar.findChildren(TitleButton)
    mock_button = None
    for button in buttons:
        if (
            hasattr(button, "widget_class")
            and button.widget_class == MockRightWidget
        ):
            mock_button = button
            break

    assert mock_button is not None

    with qtbot.waitSignal(title_bar.right_button_clicked) as blocker:
        mock_button.clicked.emit()

    # Check that the emitted signal contains the correct widget class
    assert blocker.args[0] == MockRightWidget


def test_title_bar_set_button_active(qtbot: QtBot) -> None:
    """Test setting button active/inactive state."""
    parent = QWidget()
    app_parent = QWidget()
    qtbot.addWidget(parent)
    qtbot.addWidget(app_parent)

    title_bar = TitleBar(
        parent=parent,
        app_parent=app_parent,
        right_widget_classes=[MockRightWidget],
        name="Test Application",
        logo=":/svg_images/logo_qute_style.svg",
    )
    qtbot.addWidget(title_bar)

    title_bar.set_button_active(MockRightWidget, True)
    button = title_bar._button(MockRightWidget)
    assert button is not None


def test_title_bar_button_lookup_error(qtbot: QtBot) -> None:
    """Test that looking up unknown widget raises ValueError."""
    parent = QWidget()
    app_parent = QWidget()
    qtbot.addWidget(parent)
    qtbot.addWidget(app_parent)

    title_bar = TitleBar(
        parent=parent,
        app_parent=app_parent,
        right_widget_classes=[MockRightWidget],
        name="Test Application",
        logo=":/svg_images/logo_qute_style.svg",
    )
    qtbot.addWidget(title_bar)

    class UnknownWidget(BaseWidget):
        NAME = "Unknown"
        ICON = "unknown.svg"

    with pytest.raises(ValueError, match="Could not find button for widget"):
        title_bar._button(UnknownWidget)


def test_title_bar_system_button_signals(qtbot: QtBot) -> None:
    """Test that system buttons emit their respective signals."""
    parent = QWidget()
    app_parent = QWidget()
    qtbot.addWidget(parent)
    qtbot.addWidget(app_parent)

    title_bar = TitleBar(
        parent=parent,
        app_parent=app_parent,
        right_widget_classes=[],
        name="Test Application",
        logo=":/svg_images/logo_qute_style.svg",
    )
    qtbot.addWidget(title_bar)

    # Test maximize button
    with qtbot.waitSignal(title_bar.maximize):
        title_bar.maximize_button.released.emit()

    # Find and test minimize button
    buttons = title_bar.findChildren(TitleButton)
    minimize_button = None
    close_button = None

    for button in buttons:
        if hasattr(button, "tooltip_text"):
            if "Minimieren" in button.tooltip_text:
                minimize_button = button
            elif "Schließen" in button.tooltip_text:
                close_button = button

    assert minimize_button is not None
    assert close_button is not None

    # Test minimize button
    with qtbot.waitSignal(title_bar.minimize):
        minimize_button.released.emit()

    # Test close button
    with qtbot.waitSignal(title_bar.close_app):
        close_button.released.emit()
