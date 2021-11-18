"""Icon that can be painted in any given color."""
from typing import Union, cast

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtWidgets import QApplication, QLabel

from tsl.style import get_color
from tsl.widgets.custom_icon_engine import PixmapStore


class Icon(QLabel):
    """Icon that can be painted in any given color."""

    def __init__(
        self, radius: int = 20, color_name: Union[str, None] = "foreground"
    ) -> None:
        """Create a new Icon."""
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setAlignment(Qt.AlignCenter)
        # Radius needs to be set
        self.radius = radius
        self.setFixedSize(int(1.5 * radius), int(1.5 * radius))
        self._icon_path = ":/svg_icons/no_icon.svg"
        self._color_name = color_name

    def set_icon(self, icon_path: str) -> None:
        """Set the given icon path."""
        self._icon_path = icon_path
        self.update()

    def _set_icon_pixmap(self) -> None:
        """Set pixmap in correct color and Pixelratio"""
        # target rect for pixmap is fixed to 20x20, since rect = 30x30
        scale_factor = cast(
            QApplication, QGuiApplication.instance()
        ).devicePixelRatio()
        radius = int(self.radius * scale_factor)

        # Get pixmap from store
        if self._color_name:
            pixmap = PixmapStore.inst().get_pixmap(
                self._icon_path, radius, radius, get_color(self._color_name)
            )
        else:
            pixmap = PixmapStore.inst().get_pixmap(
                self._icon_path, radius, radius
            )
        # Set the scale_factor -> displayed pixmap fits into target
        pixmap.setDevicePixelRatio(scale_factor)
        self.setPixmap(pixmap)

        # For example: scale_factor = 2, svg = 1x10 --> pixmap = 4x40,
        # target rect = 2x20

    def paintEvent(  # pylint: disable=invalid-name
        self, event: QtGui.QPaintEvent
    ) -> None:
        """Override method of QLabel"""
        # Set correct pixmap in update
        self._set_icon_pixmap()
        super().paintEvent(event)
