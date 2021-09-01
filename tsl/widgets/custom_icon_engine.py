"""IconEngine to paint icons in any given color."""
from __future__ import annotations

import logging
from collections import defaultdict
from typing import Dict, Optional

from PyQt5.QtCore import QRect, QSize, Qt
from PyQt5.QtGui import QColor, QIcon, QIconEngine, QPainter, QPixmap

from tsl.style import get_color

# pylint: disable=invalid-name
log = logging.getLogger(__name__)
# pylint: enable=invalid-name


class CustomIconEngine(QIconEngine):  # pylint: disable=too-few-public-methods
    """
    Global CustomIconEngine handler for drawing icons.

    To use, create engine and pass it to a QIcon.
    """

    def __init__(self, path: str, color: str):
        super().__init__()
        self._path = path
        self._color_name = color

    def paint(
        self,
        painter: QPainter,
        rect: QRect,
        _: QIcon.Mode,
        __: QIcon.State,
    ) -> None:
        """Override method of QIconEngine"""
        store = PixmapStore.inst()
        radius = min(rect.width(), rect.height())
        rect.setSize(QSize(radius, radius))
        # Scale Icon (not rect) according to DevicePixelRatio
        radius = int(radius * painter.device().devicePixelRatioF())
        pixmap = store.get_pixmap(
            self._path, radius, get_color(self._color_name)
        )
        painter.drawPixmap(rect, pixmap, pixmap.rect())


class PixmapStore:
    """
    Global Pixmap handler for commonly used icons.

    To use, get the current instance with PixmapStore.inst() and call
    get_pixmap for the desired icon.
    """

    INST: Optional[PixmapStore] = None
    # _pixmap[path][radius][color]
    _pixmaps: Dict[str, Dict[int, Dict[str, QPixmap]]] = defaultdict(
        lambda: defaultdict(dict)
    )

    def __init__(self) -> None:
        """Create a new DatabaseCache."""
        assert not PixmapStore.INST

    @classmethod
    def inst(cls) -> PixmapStore:
        """Return the current instance of the PixmapStore."""
        if not PixmapStore.INST:
            PixmapStore.INST = PixmapStore()
        return PixmapStore.INST

    def get_pixmap(self, path: str, radius: int, color: str) -> QPixmap:
        """Return the desired pixmap from the PixmapStore."""
        try:
            return self._pixmaps[path][radius][color]
        # Pixmap has not been created so far
        except KeyError:
            log.debug(
                "Creating QPixmap for path '%s' "
                "with radius '%s' and color '%s'",
                path,
                radius,
                color,
            )
            # Editing the svg is slower than drawing the icon new
            icon = QPixmap(path)
            painter = QPainter(icon)
            painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
            painter.fillRect(icon.rect(), QColor(color))
            pixmap = icon.scaled(
                radius, radius, Qt.IgnoreAspectRatio, Qt.SmoothTransformation
            )
            painter.end()
            self._pixmaps[path][radius][color] = pixmap
            return pixmap
