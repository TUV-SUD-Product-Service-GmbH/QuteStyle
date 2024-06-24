"""Tests for Icon."""

# pylint: disable=protected-access
from collections.abc import Iterator
from random import randint

import pytest
from PySide6.QtCore import QRect
from PySide6.QtGui import QPainter, QPaintEvent, QPixmap
from pytestqt.qtbot import QtBot

from qute_style.dev.mocks import CallList, check_call
from qute_style.widgets.icon import Icon


@pytest.fixture(name="radius", scope="session")
def fixture_radius() -> int:
    """Return a random radius for an Icon."""
    return randint(32, 128)


@pytest.fixture(name="scale", scope="session")
def fixture_scale() -> float:
    """Return a scale factor for painting."""
    return randint(50, 250) / 100


@pytest.fixture(name="icon", scope="class")
def fixture_icon(qtbot: QtBot, color_name: str, radius: int) -> Icon:
    """Return an Icon."""
    icon = Icon(radius, color_name)
    qtbot.addWidget(icon)
    icon.show()
    qtbot.waitExposed(icon)
    return icon


class TestIconBasic:
    """Test basic functionality for Icon."""

    @staticmethod
    def test_radius(icon: Icon, radius: int) -> None:
        """Test that the radius is correctly set."""
        assert icon._radius == radius

    @staticmethod
    def test_color_name(icon: Icon, color_name: str) -> None:
        """Test that the color_name is correctly set."""
        assert icon._color_name == color_name

    @staticmethod
    def test_icon_path(icon: Icon) -> None:
        """Test that the Icon uses its default icon path."""
        assert icon._icon_path == Icon.DEFAULT_ICON_PATH


def test_set_icon(icon: Icon, icon_path: str) -> None:
    """Test that pixmap of icon is set correctly."""
    with check_call(Icon, "update"):
        icon.set_icon(icon_path)
    assert icon._icon_path == icon_path


@pytest.fixture(name="pixmap", scope="class")
def fixture_pixmap(icon: Icon, scale: float) -> QPixmap:
    """Test that the pixmap is correct for painting."""
    with check_call(Icon, "scale", scale, as_property=True, call_count=-1):
        return icon._get_pixmap()


class TestPixmap:
    """Test that the pixmap to paint is correctly created."""

    @staticmethod
    def test_pixmap_scale(pixmap: QPixmap, scale: float) -> None:
        """Test that the pixmap has the correct scale."""
        assert pixmap.devicePixelRatio() == scale

    @staticmethod
    def test_pixmap_width(pixmap: QPixmap, radius: int, scale: float) -> None:
        """Test that the pixmap has the correct width."""
        assert pixmap.width() == int(radius * scale)

    @staticmethod
    def test_pixmap_height(pixmap: QPixmap, radius: int, scale: float) -> None:
        """Test that the pixmap has the correct height."""
        assert pixmap.height() == int(radius * scale)


class TestDraw:
    """Test drawing an Icon."""

    @staticmethod
    @pytest.fixture(name="xy_pos", scope="class")
    def fixture_xy_pos(icon: Icon, pixmap: QPixmap) -> float:
        """Return the x/y position of the pixmap to paint."""
        return (icon.height() - pixmap.height()) // 2

    @staticmethod
    @pytest.fixture(name="draw_pixmap_call", scope="class")
    def fixture_draw_pixmap_call(
        icon: Icon, scale: float
    ) -> Iterator[CallList]:
        """Test that the QPixmap is drawn correctly."""
        with check_call(
            Icon, "scale", scale, as_property=True, call_count=-1
        ), check_call(QPainter, "drawPixmap") as calls:
            # Just pass None, the event isn't used.
            icon.paintEvent(QPaintEvent(QRect()))
        yield calls

    @staticmethod
    def test_x_pos(draw_pixmap_call: CallList, xy_pos: float) -> None:
        """Test that the QPixmap is drawn at the correct x position."""
        assert draw_pixmap_call[0][0][1] == xy_pos

    @staticmethod
    def test_y_pos(draw_pixmap_call: CallList, xy_pos: float) -> None:
        """Test that the QPixmap is drawn at the correct y position."""
        assert draw_pixmap_call[0][0][2] == xy_pos

    @staticmethod
    def test_image(draw_pixmap_call: CallList, pixmap: QPixmap) -> None:
        """Test that the pixmaps are identical."""
        assert draw_pixmap_call[0][0][3].width() == pixmap.width()
        assert draw_pixmap_call[0][0][3].height() == pixmap.height()
        assert draw_pixmap_call[0][0][3].toImage() == pixmap.toImage()
