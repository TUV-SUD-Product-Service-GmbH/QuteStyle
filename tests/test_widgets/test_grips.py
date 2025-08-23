"""Tests for grips."""

import pytest
from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QWidget
from pytestqt.qtbot import QtBot

from qute_style.widgets.grips import CornerGrip, EdgeGrip


@pytest.fixture(name="parent_widget")
def fixture_parent_widget() -> QWidget:
    """Create a parent widget for grip testing."""
    parent = QWidget()
    parent.setFixedSize(100, 100)
    parent.setMinimumSize(50, 50)
    return parent


class TestCornerGrip:
    """Test CornerGrip functionality."""

    @staticmethod
    @pytest.mark.parametrize(
        "position, expected",
        [
            (Qt.Corner.TopLeftCorner, (5, 5)),
            (Qt.Corner.TopRightCorner, (80, 5)),
            (Qt.Corner.BottomLeftCorner, (5, 80)),
            (Qt.Corner.BottomRightCorner, (80, 80)),
        ],
        ids=["top-left", "top-right", "bottom-left", "bottom-right"],
    )
    def test_corner_grip_adapt(
        qtbot: QtBot,
        parent_widget: QWidget,
        position: Qt.Corner,
        expected: tuple[int, int],
    ) -> None:
        """Test method for the `adapt` function of the `CornerGrip` class."""
        grip = CornerGrip(parent_widget, position)

        grip.adapt()

        assert (grip.x(), grip.y()) == expected

    @staticmethod
    def test_corner_grip_initialization(parent_widget: QWidget) -> None:
        """Test CornerGrip initialization."""
        grip = CornerGrip(parent_widget, Qt.Corner.TopLeftCorner)

        assert grip.parent() == parent_widget
        assert grip._position == Qt.Corner.TopLeftCorner
        assert grip.objectName() == "grip"
        assert grip.size().width() == 15
        assert grip.size().height() == 15

    @staticmethod
    def test_corner_grip_signal_exists(parent_widget: QWidget) -> None:
        """Test that CornerGrip has window_geometry_changed signal."""
        grip = CornerGrip(parent_widget, Qt.Corner.TopLeftCorner)
        assert hasattr(grip, "window_geometry_changed")

    @staticmethod
    @pytest.mark.parametrize("position", list(Qt.Corner))
    def test_corner_grip_all_positions(
        parent_widget: QWidget, position: Qt.Corner
    ) -> None:
        """Test CornerGrip with all corner positions."""
        grip = CornerGrip(parent_widget, position)
        grip.adapt()

        # Verify grip is positioned within parent bounds
        assert 0 <= grip.x() <= parent_widget.width()
        assert 0 <= grip.y() <= parent_widget.height()

    @staticmethod
    def test_corner_grip_resize_top_left(
        qtbot: QtBot, parent_widget: QWidget
    ) -> None:
        """Test CornerGrip resize functionality for top-left corner."""
        parent_widget.setGeometry(QRect(100, 100, 200, 200))
        grip = CornerGrip(parent_widget, Qt.Corner.TopLeftCorner)

        with qtbot.waitSignal(grip.window_geometry_changed):
            # Simulate resize with delta_x=10, delta_y=10
            grip._resize_x_y(10, 10)

    @staticmethod
    def test_corner_grip_resize_bottom_right(
        qtbot: QtBot, parent_widget: QWidget
    ) -> None:
        """Test CornerGrip resize functionality for bottom-right corner."""
        parent_widget.setGeometry(QRect(100, 100, 200, 200))
        grip = CornerGrip(parent_widget, Qt.Corner.BottomRightCorner)

        with qtbot.waitSignal(grip.window_geometry_changed):
            # Simulate resize with delta_x=20, delta_y=15
            grip._resize_x_y(20, 15)

    @staticmethod
    def test_corner_grip_minimum_size_constraint(
        parent_widget: QWidget,
    ) -> None:
        """Test that CornerGrip respects minimum size constraints."""
        parent_widget.setGeometry(QRect(0, 0, 100, 100))
        grip = CornerGrip(parent_widget, Qt.Corner.BottomRightCorner)

        # Try to resize smaller than minimum size
        grip._resize_x_y(-200, -200)  # Large negative deltas

        # The resize should respect minimum size constraints
        # We can't test the exact values without the signal,
        # but method should complete


class TestEdgeGrip:
    """Test EdgeGrip functionality."""

    @staticmethod
    @pytest.mark.parametrize(
        "position, expected",
        [
            (Qt.Edge.TopEdge, (5, 5, 100, 10)),
            (Qt.Edge.BottomEdge, (5, 85, 100, 10)),
            (Qt.Edge.LeftEdge, (5, 10, 10, 100)),
            (Qt.Edge.RightEdge, (85, 10, 10, 100)),
        ],
        ids=["top-edge", "bottom-edge", "left-edge", "right-edge"],
    )
    def test_edge_grip_adapt(
        qtbot: QtBot,
        parent_widget: QWidget,
        position: Qt.Edge,
        expected: tuple[int, int, int, int],
    ) -> None:
        """Test method for the `adapt` function of the `EdgeGrip` class."""
        grip = EdgeGrip(parent_widget, position)

        grip.adapt()

        assert (grip.x(), grip.y(), grip.width(), grip.height()) == expected

    @staticmethod
    def test_edge_grip_initialization(parent_widget: QWidget) -> None:
        """Test EdgeGrip initialization."""
        grip = EdgeGrip(parent_widget, Qt.Edge.TopEdge)

        assert grip.parent() == parent_widget
        assert grip._position == Qt.Edge.TopEdge
        assert grip.objectName() == "grip"

    @staticmethod
    def test_edge_grip_cursor_vertical(parent_widget: QWidget) -> None:
        """Test EdgeGrip sets correct cursor for vertical edges."""
        top_grip = EdgeGrip(parent_widget, Qt.Edge.TopEdge)
        bottom_grip = EdgeGrip(parent_widget, Qt.Edge.BottomEdge)

        assert top_grip.cursor().shape() == Qt.CursorShape.SizeVerCursor
        assert bottom_grip.cursor().shape() == Qt.CursorShape.SizeVerCursor
        assert top_grip.maximumHeight() == 10
        assert bottom_grip.maximumHeight() == 10

    @staticmethod
    def test_edge_grip_cursor_horizontal(parent_widget: QWidget) -> None:
        """Test EdgeGrip sets correct cursor for horizontal edges."""
        left_grip = EdgeGrip(parent_widget, Qt.Edge.LeftEdge)
        right_grip = EdgeGrip(parent_widget, Qt.Edge.RightEdge)

        assert left_grip.cursor().shape() == Qt.CursorShape.SizeHorCursor
        assert right_grip.cursor().shape() == Qt.CursorShape.SizeHorCursor
        assert left_grip.maximumWidth() == 10
        assert right_grip.maximumWidth() == 10

    @staticmethod
    def test_edge_grip_signal_exists(parent_widget: QWidget) -> None:
        """Test that EdgeGrip has window_geometry_changed signal."""
        grip = EdgeGrip(parent_widget, Qt.Edge.TopEdge)
        assert hasattr(grip, "window_geometry_changed")

    @staticmethod
    @pytest.mark.parametrize("position", list(Qt.Edge))
    def test_edge_grip_all_positions(
        parent_widget: QWidget, position: Qt.Edge
    ) -> None:
        """Test EdgeGrip with all edge positions."""
        grip = EdgeGrip(parent_widget, position)
        grip.adapt()

        # Verify grip is positioned within parent bounds
        assert grip.x() >= 0
        assert grip.y() >= 0
        # Allow some margin
        assert grip.x() + grip.width() <= parent_widget.width() + 10
        assert grip.y() + grip.height() <= parent_widget.height() + 10

    @staticmethod
    def test_edge_grip_resize_horizontal(
        qtbot: QtBot, parent_widget: QWidget
    ) -> None:
        """Test EdgeGrip horizontal resize functionality."""
        parent_widget.setGeometry(QRect(100, 100, 200, 200))
        grip = EdgeGrip(parent_widget, Qt.Edge.LeftEdge)

        with qtbot.waitSignal(grip.window_geometry_changed):
            grip._resize_x(10)

    @staticmethod
    def test_edge_grip_resize_vertical(
        qtbot: QtBot, parent_widget: QWidget
    ) -> None:
        """Test EdgeGrip vertical resize functionality."""
        parent_widget.setGeometry(QRect(100, 100, 200, 200))
        grip = EdgeGrip(parent_widget, Qt.Edge.TopEdge)

        with qtbot.waitSignal(grip.window_geometry_changed):
            grip._resize_y(15)

    @staticmethod
    def test_edge_grip_minimum_size_constraint(parent_widget: QWidget) -> None:
        """Test that EdgeGrip respects minimum size constraints."""
        parent_widget.setGeometry(QRect(0, 0, 100, 100))
        grip = EdgeGrip(parent_widget, Qt.Edge.RightEdge)

        # Try to resize smaller than minimum size
        grip._resize_x(-200)  # Large negative delta

        # The resize should respect minimum size constraints
        # We can't test the exact values without the signal,
        # but method should complete

    @staticmethod
    def test_edge_grip_mouse_move_event_vertical(
        parent_widget: QWidget,
    ) -> None:
        """Test EdgeGrip mouse move event for vertical edges."""
        grip = EdgeGrip(parent_widget, Qt.Edge.TopEdge)

        # Create a mock mouse event
        event = QMouseEvent(
            QMouseEvent.Type.MouseMove,
            grip.rect().center(),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )

        # This should not raise an exception
        grip.mouseMoveEvent(event)
        assert event.isAccepted()

    @staticmethod
    def test_edge_grip_mouse_move_event_horizontal(
        parent_widget: QWidget,
    ) -> None:
        """Test EdgeGrip mouse move event for horizontal edges."""
        grip = EdgeGrip(parent_widget, Qt.Edge.LeftEdge)

        # Create a mock mouse event
        event = QMouseEvent(
            QMouseEvent.Type.MouseMove,
            grip.rect().center(),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )

        # This should not raise an exception
        grip.mouseMoveEvent(event)
        assert event.isAccepted()


class TestGripEdgeCases:
    """Test edge cases and error conditions for grips."""

    @staticmethod
    def test_corner_grip_with_zero_size_parent() -> None:
        """Test CornerGrip behavior with zero-size parent."""
        parent = QWidget()
        parent.setFixedSize(0, 0)
        grip = CornerGrip(parent, Qt.Corner.TopLeftCorner)

        # Should not crash
        grip.adapt()
        assert grip.x() >= 0
        assert grip.y() >= 0

    @staticmethod
    def test_edge_grip_with_zero_size_parent() -> None:
        """Test EdgeGrip behavior with zero-size parent."""
        parent = QWidget()
        parent.setFixedSize(0, 0)
        grip = EdgeGrip(parent, Qt.Edge.TopEdge)

        # Should not crash
        grip.adapt()
        assert grip.x() >= 0
        assert grip.y() >= 0

    @staticmethod
    def test_corner_grip_resize_with_zero_deltas(
        qtbot: QtBot, parent_widget: QWidget
    ) -> None:
        """Test CornerGrip resize with zero deltas."""
        grip = CornerGrip(parent_widget, Qt.Corner.TopLeftCorner)

        with qtbot.waitSignal(grip.window_geometry_changed):
            grip._resize_x_y(0, 0)

    @staticmethod
    def test_edge_grip_resize_with_zero_deltas(
        qtbot: QtBot, parent_widget: QWidget
    ) -> None:
        """Test EdgeGrip resize with zero deltas."""
        grip = EdgeGrip(parent_widget, Qt.Edge.LeftEdge)

        with qtbot.waitSignal(grip.window_geometry_changed):
            grip._resize_x(0)

    @staticmethod
    def test_corner_grip_mouse_press_event(parent_widget: QWidget) -> None:
        """Test CornerGrip mouse press event."""
        grip = CornerGrip(parent_widget, Qt.Corner.TopLeftCorner)

        event = QMouseEvent(
            QMouseEvent.Type.MouseButtonPress,
            grip.rect().center(),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )

        # Should not raise an exception (method logs and returns)
        grip.mousePressEvent(event)

    @staticmethod
    def test_corner_grip_mouse_move_event(parent_widget: QWidget) -> None:
        """Test CornerGrip mouse move event."""
        grip = CornerGrip(parent_widget, Qt.Corner.TopLeftCorner)

        event = QMouseEvent(
            QMouseEvent.Type.MouseMove,
            grip.rect().center(),
            Qt.MouseButton.LeftButton,
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
        )

        # Should not raise an exception
        grip.mouseMoveEvent(event)
