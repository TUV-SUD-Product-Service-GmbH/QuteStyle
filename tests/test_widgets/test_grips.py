"""Tests for grips."""

import pytest
from PySide6.QtCore import Qt
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
