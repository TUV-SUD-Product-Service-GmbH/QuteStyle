"""Tests for CustomIconEngine and PixmapStore."""
from _pytest.monkeypatch import MonkeyPatch
from PySide6.QtCore import QRect, QSize
from PySide6.QtGui import QColor, QIcon, QPainter, QPixmap
from pytestqt.qtbot import QtBot

from qute_style.qs_main_window import AppData, CustomMainWindow
from qute_style.style import DEFAULT_STYLE, get_color, set_current_style
from qute_style.widgets.custom_icon_engine import CustomIconEngine, PixmapStore


def test_get_new_pixmap(  # pylint: disable=unused-argument
    qtbot: QtBot,
) -> None:
    """Test that correct pixmap is return when it was not stored before."""
    set_current_style(DEFAULT_STYLE)
    store = PixmapStore.inst()
    new_pixmap = store.get_pixmap(
        "tests/test_images/square.svg", 16, 16, get_color("yellow")
    )
    assert new_pixmap.size() == QSize(16, 16)
    # due to transformation effects color of pixels is not correct everywhere
    new_color = new_pixmap.toImage().pixel(9, 9)
    assert new_color == QColor(get_color("yellow")).rgb()


# qtbot is necessary for QPixmap
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


def create_new_main_window(qtbot: QtBot) -> CustomMainWindow:
    """Create and show a new QuteStyleMainWindow."""
    widget = CustomMainWindow(AppData("", "1.0.0"))
    qtbot.addWidget(widget)
    widget.show()
    qtbot.waitUntil(widget.isVisible)
    return widget


def test_custom_icon_engine_paint(
    qtbot: QtBot, monkeypatch: MonkeyPatch
) -> None:
    """Test that drawPixmap method inside is called correctly."""
    widget = create_new_main_window(qtbot)
    engine = CustomIconEngine("tests/test_images/test_icon.svg", "yellow")
    painter = QPainter(widget)
    rect = QRect(0, 0, 40, 16)

    def mock_draw(
        _: QPainter, target: QRect, pixmap: QPixmap, source: QRect
    ) -> None:
        """Mock draw Pixmap method."""
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
