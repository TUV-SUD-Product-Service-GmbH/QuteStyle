"""Icon that can be painted in any given color."""

from typing import cast

from PySide6 import QtGui
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtWidgets import QApplication, QWidget

from qute_style.style import get_color
from qute_style.widgets.custom_icon_engine import PixmapStore


class Icon(QWidget):
    """Icon that can be painted in any given color."""

    DEFAULT_ICON_PATH = ":/svg_icons/no_icon.svg"

    def __init__(
        self, radius: int = 20, color_name: str | None = "foreground"
    ) -> None:
        """Create a new Icon."""
        super().__init__()

        # Radius needs to be set
        self._radius = radius
        self.setFixedSize(int(1.5 * radius), int(1.5 * radius))
        self._icon_path = self.DEFAULT_ICON_PATH
        self._color_name = color_name

    def set_icon(self, icon_path: str) -> None:
        """Set the given icon path."""
        self._icon_path = icon_path
        self.update()

    @property
    def scale(self) -> float:
        """Return the current scale for painting."""
        # At this point, there must be a QApplication
        return cast(QApplication, QApplication.instance()).devicePixelRatio()

    def paintEvent(self, _: QtGui.QPaintEvent) -> None:  # noqa: N802
        """Override QWidget.paintEvent to draw pixmap."""
        pixmap = self._get_pixmap()
        xy_pos = (self.height() - pixmap.height()) // 2

        painter = QPainter(self)
        painter.drawPixmap(xy_pos, xy_pos, pixmap)
        painter.end()

    def _get_pixmap(self) -> QPixmap:
        """Return the pixmap for painting."""
        color = get_color(self._color_name) if self._color_name else None
        radius = int(self._radius * self.scale)

        # Get the pixmap from store.
        pixmap = PixmapStore.inst().get_pixmap(
            self._icon_path, radius, radius, color
        )

        # Set the scale_factor -> displayed pixmap fits into target
        pixmap.setDevicePixelRatio(self.scale)
        return pixmap
