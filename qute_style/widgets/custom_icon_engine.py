"""IconEngine to paint icons in any given color."""

from __future__ import annotations

import logging
from collections import defaultdict

from PySide6.QtCore import QPoint, QRect, QSize, Qt
from PySide6.QtGui import QColor, QIcon, QIconEngine, QPainter, QPixmap

from qute_style.style import get_color

# pylint: disable=invalid-name
log = logging.getLogger(__name__)
# pylint: enable=invalid-name


class CustomIconEngine(QIconEngine):  # pylint: disable=too-few-public-methods
    """
    Global CustomIconEngine handler for drawing icons.

    To use, create engine and pass it to a QIcon.
    """

    def __init__(self, path: str, color: str):
        """Init function."""
        super().__init__()
        self._path = path
        self._color_name = color

    def pixmap(
        self, size: QSize, mode: QIcon.Mode, state: QIcon.State
    ) -> QPixmap:
        """
        Override method of QIconEngine.

        The reimplemented paint() is often called via the pixmap().
        Because the default painter in pixmap() has no alpha channel,
        the painter's pixmap must be set transparent to display icons with
        transparent backgrounds.
        """
        pixmap = QPixmap(size)
        pixmap.fill(Qt.GlobalColor.transparent)
        self.paint(QPainter(pixmap), QRect(QPoint(0, 0), size), mode, state)
        return pixmap

    def paint(
        self,
        painter: QPainter,
        rect: QRect,
        _: QIcon.Mode,
        __: QIcon.State,
    ) -> None:
        """Override method of QIconEngine."""
        store = PixmapStore.inst()
        radius = min(rect.width(), rect.height())
        rect.setSize(QSize(radius, radius))
        # Scale Icon (not rect) according to DevicePixelRatio
        radius = int(radius * painter.device().devicePixelRatio())
        pixmap = store.get_pixmap(
            self._path, radius, radius, get_color(self._color_name)
        )
        painter.drawPixmap(rect, pixmap, pixmap.rect())


class PixmapStore:
    """
    Global Pixmap handler for commonly used icons.

    To use, get the current instance with PixmapStore.inst() and call
    get_pixmap for the desired icon.
    """

    INST: PixmapStore | None = None
    # _pixmap[path][width, height][color]
    _pixmaps: dict[str, dict[tuple[int, int], dict[str | None, QPixmap]]] = (
        defaultdict(lambda: defaultdict(dict))
    )

    def __init__(self) -> None:
        """Create a new PixmapStore instance."""
        assert not PixmapStore.INST

    # make sure correct class is called --> maybe privat or something
    @classmethod
    def inst(cls) -> PixmapStore:
        """Return the current instance of the PixmapStore."""
        if not PixmapStore.INST:
            PixmapStore.INST = PixmapStore()
        return PixmapStore.INST

    def get_pixmap(
        self, path: str, width: int, height: int, color: str | None = None
    ) -> QPixmap:
        """
        Return the pixmap with width and height from the PixmapStore.

        The color is optional, if no color is given,
        the icon will keep its original colors.
        """
        # The original AspectRatio will be kept
        try:
            return self._pixmaps[path][width, height][color]
        # Pixmap has not been created so far
        except KeyError as exc:
            log.debug(
                "Creating QPixmap for path '%s' "
                "with width '%s', height '%s' and color '%s'",
                path,
                width,
                height,
                color,
            )
            # Editing the svg is slower than drawing the icon new
            icon = QPixmap(path)
            if icon.isNull():
                raise ValueError(  # pylint: disable=raise-missing-from
                    f"Could not load pixmap: {path}"
                ) from exc
            painter = QPainter(icon)
            painter.setCompositionMode(
                QPainter.CompositionMode.CompositionMode_SourceIn
            )
            if color:
                painter.fillRect(icon.rect(), QColor(color))
            painter.end()
            # Scaling works best if svg has dimensions ~56x56
            pixmap = icon.scaled(
                width,
                height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self._pixmaps[path][width, height][color] = pixmap
            return pixmap
