"""Tests for grips."""

# pylint: disable=protected-access

import pytest
from PySide6.QtCore import QPointF, QRect, Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QWidget
from pytestqt.qtbot import QtBot

from qute_style.widgets.grips import CornerGrip, EdgeGrip


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
    qtbot: QtBot, position: Qt.Corner, expected: tuple[int, int]
) -> None:
    """Test method for the `adapt` function of the `CornerGrip` class."""
    parent = QWidget()
    parent.setFixedSize(100, 100)
    grip = CornerGrip(parent, position)

    grip.adapt()

    assert (grip.x(), grip.y()) == expected


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
    qtbot: QtBot, position: Qt.Edge, expected: tuple[int, int, int, int]
) -> None:
    """Test method for the `adapt` function of the `EdgeGrip` class."""
    parent = QWidget()
    parent.setFixedSize(100, 100)
    grip = EdgeGrip(parent, position)

    grip.adapt()

    assert (grip.x(), grip.y(), grip.width(), grip.height()) == expected


def _make_parent(qtbot: QtBot) -> QWidget:
    """Create a parent widget with known geometry and minimum size."""
    parent = QWidget()
    parent.setMinimumSize(50, 50)
    parent.setGeometry(100, 100, 200, 200)
    qtbot.addWidget(parent)
    return parent


def _mouse_event(event_type: QMouseEvent.Type, x: int, y: int) -> QMouseEvent:
    """Create a QMouseEvent at the given local position."""
    return QMouseEvent(
        event_type,
        QPointF(x, y),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )


@pytest.mark.parametrize(
    "position, delta, expected_width",
    [
        (Qt.Edge.LeftEdge, 10, 191),  # +1 due to QRect inclusive coords
        (Qt.Edge.RightEdge, 10, 210),
        (Qt.Edge.LeftEdge, 200, 51),  # clamped to minimum (+1)
    ],
    ids=["left-shrink", "right-grow", "left-clamp-minimum"],
)
def test_edge_grip_resize_x(
    qtbot: QtBot,
    position: Qt.Edge,
    delta: int,
    expected_width: int,
) -> None:
    """Test that _resize_x computes the correct geometry."""
    parent = _make_parent(qtbot)
    grip = EdgeGrip(parent, position)
    original_right = parent.geometry().right()

    with qtbot.waitSignal(grip.window_geometry_changed) as blocker:
        grip._resize_x(delta)

    geo: QRect = blocker.args[0]
    assert geo.width() == expected_width
    if position == Qt.Edge.LeftEdge:
        assert geo.right() == original_right


@pytest.mark.parametrize(
    "position, delta, expected_height",
    [
        (Qt.Edge.TopEdge, 10, 191),  # +1 due to QRect inclusive coords
        (Qt.Edge.BottomEdge, 10, 210),
        (Qt.Edge.TopEdge, 200, 51),  # clamped to minimum (+1)
    ],
    ids=["top-shrink", "bottom-grow", "top-clamp-minimum"],
)
def test_edge_grip_resize_y(
    qtbot: QtBot,
    position: Qt.Edge,
    delta: int,
    expected_height: int,
) -> None:
    """Test that _resize_y computes the correct geometry."""
    parent = _make_parent(qtbot)
    grip = EdgeGrip(parent, position)
    original_bottom = parent.geometry().bottom()

    with qtbot.waitSignal(grip.window_geometry_changed) as blocker:
        grip._resize_y(delta)

    geo: QRect = blocker.args[0]
    assert geo.height() == expected_height
    if position == Qt.Edge.TopEdge:
        assert geo.bottom() == original_bottom


@pytest.mark.parametrize(
    "position",
    [Qt.Edge.TopEdge, Qt.Edge.BottomEdge, Qt.Edge.LeftEdge, Qt.Edge.RightEdge],
    ids=["top", "bottom", "left", "right"],
)
def test_edge_grip_mouse_move(qtbot: QtBot, position: Qt.Edge) -> None:
    """Test that mouseMoveEvent dispatches to the correct resize method."""
    parent = _make_parent(qtbot)
    grip = EdgeGrip(parent, position)

    # mousePressEvent must be called first to enable tracking
    grip.mousePressEvent(_mouse_event(QMouseEvent.Type.MouseButtonPress, 5, 5))

    with qtbot.waitSignal(grip.window_geometry_changed):
        grip.mouseMoveEvent(_mouse_event(QMouseEvent.Type.MouseMove, 10, 10))


@pytest.mark.parametrize(
    "position, delta_x, delta_y, expected_size",
    [
        (Qt.Corner.TopLeftCorner, 10, 10, (191, 191)),
        (Qt.Corner.TopRightCorner, 10, 10, (210, 191)),
        (Qt.Corner.BottomLeftCorner, 10, 10, (191, 210)),
        (Qt.Corner.BottomRightCorner, 10, 10, (210, 210)),
    ],
    ids=["top-left", "top-right", "bottom-left", "bottom-right"],
)
def test_corner_grip_resize_x_y(
    qtbot: QtBot,
    position: Qt.Corner,
    delta_x: int,
    delta_y: int,
    expected_size: tuple[int, int],
) -> None:
    """Test that _resize_x_y computes the correct geometry for each corner."""
    parent = _make_parent(qtbot)
    grip = CornerGrip(parent, position)
    original_geo = parent.geometry()

    with qtbot.waitSignal(grip.window_geometry_changed) as blocker:
        grip._resize_x_y(delta_x, delta_y)

    geo: QRect = blocker.args[0]
    assert (geo.width(), geo.height()) == expected_size

    # Anchored edges should remain fixed
    if position in (Qt.Corner.TopRightCorner, Qt.Corner.BottomRightCorner):
        assert geo.left() == original_geo.left()
    if position in (Qt.Corner.TopLeftCorner, Qt.Corner.BottomLeftCorner):
        assert geo.right() == original_geo.right()
    if position in (Qt.Corner.BottomLeftCorner, Qt.Corner.BottomRightCorner):
        assert geo.top() == original_geo.top()
    if position in (Qt.Corner.TopLeftCorner, Qt.Corner.TopRightCorner):
        assert geo.bottom() == original_geo.bottom()


def test_corner_grip_mouse_move(qtbot: QtBot) -> None:
    """Test that mouseMoveEvent calls _resize_x_y."""
    parent = _make_parent(qtbot)
    grip = CornerGrip(parent, Qt.Corner.BottomRightCorner)

    grip.mousePressEvent(_mouse_event(QMouseEvent.Type.MouseButtonPress, 5, 5))

    with qtbot.waitSignal(grip.window_geometry_changed):
        grip.mouseMoveEvent(_mouse_event(QMouseEvent.Type.MouseMove, 15, 15))
