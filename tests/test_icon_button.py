"""Tests for IconButton and Icon"""
# pylint: disable=protected-access

from _pytest.monkeypatch import MonkeyPatch
from PyQt5.QtGui import (
    QColor,
    QGuiApplication,
    QPaintDevice,
    QPainter,
    QPixmap,
)
from pytestqt.qtbot import QtBot

from tsl.style import THEMES, Themes, get_color, set_current_style
from tsl.widgets.custom_icon_engine import PixmapStore
from tsl.widgets.icon import Icon
from tsl.widgets.icon_button import IconButton


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
        """Mock draw Pixmap method"""
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


def test_set_icon(qtbot: QtBot, monkeypatch: MonkeyPatch) -> None:
    """Test that pixmap of icon is set correctly"""
    monkeypatch.setattr(QGuiApplication, "devicePixelRatio", lambda _: 2.0)
    icon = Icon()
    qtbot.addWidget(icon)
    icon.set_icon("tests/test_images/test_icon.svg")
    icon._set_icon_pixmap()
    style = list(THEMES.keys())[0]
    set_current_style(style)
    icon.set_icon("tests/test_images/test_icon.svg")
    icon._set_icon_pixmap()
    set_current_style(Themes.DARCULA)
    assert icon.pixmap().height() == 40
    assert icon.pixmap().width() == 40
    # check that pixmap exists in two different colors

    assert (
        len(
            PixmapStore.inst()._pixmaps["tests/test_images/test_icon.svg"][
                40, 40
            ]
        )
        == 2
    )
