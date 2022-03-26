"""Tests for IconButton and Icon."""
# pylint: disable=protected-access

from _pytest.monkeypatch import MonkeyPatch
from PyQt5.QtGui import QColor, QPaintDevice, QPainter, QPixmap
from pytestqt.qtbot import QtBot

from qute_style.style import get_color
from qute_style.widgets.custom_icon_engine import PixmapStore
from qute_style.widgets.icon_button import IconButton


# qtbot is necessary for QPixmap
def test_icon_button_paint(  # pylint: disable=unused-argument
    qtbot: QtBot, monkeypatch: MonkeyPatch
) -> None:
    """Test that drawPixmap method inside is called correctly."""
    icon_button = IconButton(
        None, "tests/test_images/test_icon.svg", None, None
    )
    paint = QPainter(icon_button)

    def mock_draw(
        _: QPainter,
        pos_x: int,
        pos_y: int,
        width: int,
        height: int,
        pixmap: QPixmap,
    ) -> None:
        """Mock draw Pixmap method."""
        assert pos_x == 7
        assert pos_y == 7
        assert width == 21
        assert height == 21
        store = PixmapStore.inst()
        new_pixmap = store.get_pixmap(
            "tests/test_images/test_icon.svg", 43, 43, get_color("foreground")
        )
        assert new_pixmap == pixmap

    monkeypatch.setattr(QPainter, "drawPixmap", mock_draw)
    monkeypatch.setattr(QPaintDevice, "devicePixelRatio", lambda _: 2.0)

    icon_button._icon_paint(paint, QColor(get_color("foreground")))
    paint.end()
