"""Tests for CustomIconEngine and PixmapStore"""
import filecmp

from _pytest.monkeypatch import MonkeyPatch
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QIcon, QPainter, QPixmap
from pytestqt.qtbot import QtBot

from tests.test_update_window import create_new_tsl_main_window
from tsl.style import DEFAULT_STYLE, get_color, set_current_style
from tsl.widgets.custom_icon_engine import CustomIconEngine, PixmapStore


# qbot is necessary for QPixmap
def test_get_new_pixmap(  # pylint: disable=unused-argument
    qtbot: QtBot,
) -> None:
    """Test that correct pixmap is return when it was not stored before."""
    set_current_style(DEFAULT_STYLE)
    store = PixmapStore.inst()
    new_pixmap = store.get_pixmap(
        "tests/test_images/test_icon.svg", 16, 16, get_color("yellow")
    )
    # If the color code of "yellow" in default theme is changed,
    # change color of default_icon in svg
    default_pixmap = QPixmap("tests/test_images/default_icon.svg")
    default_pixmap.save("tests/test_images/default_pixmap.ppm")
    new_pixmap.save("tests/test_images/new_pixmap.ppm")
    assert filecmp.cmp(
        "tests/test_images/default_pixmap.ppm",
        "tests/test_images/new_pixmap.ppm",
    )


# qbot is necessary for QPixmap
def test_get_old_pixmap(  # pylint: disable=unused-argument
    qtbot: QtBot,
) -> None:
    """Test that already stored pixmap is returned when it was used before."""
    store = PixmapStore.inst()
    old_pixmap = store.get_pixmap(
        "tests/test_images/test_icon.svg", 18, 18, "yellow"
    )
    new_pixmap = store.get_pixmap(
        "tests/test_images/test_icon.svg", 18, 18, "yellow"
    )
    assert old_pixmap is new_pixmap


def test_custom_icon_engine_paint(
    qtbot: QtBot, monkeypatch: MonkeyPatch
) -> None:
    """Test that drawPixmap method inside is called correctly."""
    widget = create_new_tsl_main_window(qtbot)
    engine = CustomIconEngine("tests/test_images/test_icon.svg", "yellow")
    painter = QPainter(widget)
    rect = QRect(0, 0, 40, 16)

    def mock_draw(
        _: QPainter, target: QRect, pixmap: QPixmap, source: QRect
    ) -> None:
        """Mock draw Pixmap method"""
        new_rect = QRect(0, 0, 16, 16)
        assert new_rect == target
        store = PixmapStore.inst()
        new_pixmap = store.get_pixmap(
            "tests/test_images/test_icon.svg", 16, 16, get_color("yellow")
        )
        assert new_pixmap == pixmap
        assert new_pixmap.rect() == source

    monkeypatch.setattr(QPainter, "drawPixmap", mock_draw)
    engine.paint(painter, rect, _=QIcon.Normal, __=QIcon.Off)
