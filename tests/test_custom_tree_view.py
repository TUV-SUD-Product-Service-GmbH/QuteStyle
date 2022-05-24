"""Tests for CustomTreeView."""
import pytest
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter, QStandardItem, QStandardItemModel
from pytestqt.qtbot import QtBot

from qute_style.dev.mocks import check_call
from qute_style.style import get_color
from qute_style.widgets.custom_icon_engine import PixmapStore
from qute_style.widgets.custom_tree_view import CustomTreeView


@pytest.fixture(name="treeview")
def fixture_cb_items() -> CustomTreeView:
    """Create several test items."""
    treeview = CustomTreeView()
    treeview_model = QStandardItemModel()
    deutschland_item = QStandardItem("Deutschland")
    deutschland_item.appendRow(QStandardItem("Berlin"))

    treeview_model.invisibleRootItem().appendRow(deutschland_item)
    treeview.setModel(treeview_model)
    return treeview


def test_draw_branches(qtbot: QtBot, treeview: CustomTreeView) -> None:
    """Test the drawBranches Funktion."""
    with qtbot.captureExceptions() as exceptions:
        with check_call(QPainter, "drawPixmap") as calls:
            treeview.drawBranches(
                QPainter(), QRect(0, 0, 20, 17), treeview.model().index(0, 0)
            )
            assert calls[0][0][0].__eq__(
                PixmapStore.inst().get_pixmap(
                    ":/svg_icons/chevron_down.svg",
                    16,
                    16,
                    get_color("foreground"),
                )
            )
    assert not exceptions


def test_draw_branches_expanded_arrow(
    qtbot: QtBot, treeview: CustomTreeView
) -> None:
    """Test the drawBranches Funktion."""
    with qtbot.captureExceptions() as exceptions:
        with check_call(QPainter, "drawPixmap") as calls:
            treeview.expand(treeview.model().index(0, 0))
            treeview.drawBranches(
                QPainter(), QRect(0, 0, 20, 17), treeview.model().index(0, 0)
            )
            assert calls[0][0][0].__eq__(
                PixmapStore.inst().get_pixmap(
                    ":/svg_icons/chevron_right.svg",
                    16,
                    16,
                    get_color("foreground"),
                )
            )
    assert not exceptions
