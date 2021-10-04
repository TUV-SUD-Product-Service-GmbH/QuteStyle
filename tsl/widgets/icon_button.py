"""Simple button showing an icon."""
import logging
from typing import Optional, TypedDict

from PyQt5.QtCore import QEvent, QRect, Qt
from PyQt5.QtGui import QBrush, QColor, QMouseEvent, QPainter, QPaintEvent
from PyQt5.QtWidgets import QPushButton, QWidget

from tsl.style import get_color
from tsl.widgets.custom_icon_engine import PixmapStore

log = logging.getLogger(f"tsl.{__name__}")  # pylint: disable=invalid-name


class BackgroundColorNames(TypedDict):
    """Defines background colors used by the button."""

    hovering: str
    background: str
    pressed: str
    released: str


class IconButton(QPushButton):
    """Simple button showing an icon."""

    FIXED_HEIGHT: Optional[int] = 36
    FIXED_WIDTH: Optional[int] = 36

    def __init__(  # pylint: disable=too-many-arguments
        self,
        parent: QWidget = None,
        icon_path: str = ":/svg_icons/no_icon.svg",
        bgs: BackgroundColorNames = None,
        text: str = None,
        margin: float = 0.6,
    ) -> None:
        """Create a new IconButton."""
        if text:
            super().__init__(text=text, parent=parent)
        else:
            super().__init__(parent=parent)
        if bgs:
            self._bgs = bgs
        else:
            self._bgs = BackgroundColorNames(
                hovering="dark_three",
                background="bg_one",
                pressed="dark_four",
                released="dark_three",
            )

        self._set_icon_path = icon_path

        if self.FIXED_WIDTH:
            self.setFixedWidth(self.FIXED_WIDTH)
        if self.FIXED_HEIGHT:
            self.setFixedHeight(self.FIXED_HEIGHT)

        self.setCursor(Qt.PointingHandCursor)

        self._is_active: bool = False

        self._bg_color = self._bgs["background"]
        self._icon_color = "icon_color"
        self._margin = margin

    def set_active(self, active: bool) -> None:
        """
        Set the button active/inactive.

        A button is active, when the widget which is shown by pressing on the
        button is visible (i.e. right or left widget).
        """
        log.debug("Setting button '%s' active: %s.", self.objectName(), active)
        self._is_active = active
        self.update()

    def paintEvent(  # pylint: disable=invalid-name
        self, _: QPaintEvent
    ) -> None:
        """Customize painting of the button and icon."""
        paint = QPainter()
        paint.begin(self)
        paint.setRenderHint(QPainter.Antialiasing)
        paint.setPen(Qt.NoPen)
        paint.setBrush(QBrush(QColor(get_color(self._bg_color))))
        paint.drawRoundedRect(self.rect(), 8, 8)

        if self.isEnabled():
            color = get_color(self._icon_color)
        else:
            color = get_color("fg_disabled")
        self.icon_paint(paint, color)

        paint.end()

    def enterEvent(self, _: QEvent) -> None:  # pylint: disable=invalid-name
        """Change style on mouse entering the button area."""
        if self.isEnabled() and not self._is_active:
            self._bg_color = self._bgs["hovering"]
            self._icon_color = "icon_hover"
            self.update()

    def leaveEvent(self, _: QEvent) -> None:  # pylint: disable=invalid-name
        """Change style on mouse leaving the button area."""
        if not self._is_active:
            self._bg_color = self._bgs["background"]
            self._icon_color = "icon_color"
            self.update()

    def mousePressEvent(  # pylint: disable=invalid-name
        self, event: QMouseEvent
    ) -> None:
        """Event triggered on mouse button press."""
        if event.button() == Qt.LeftButton:
            self._bg_color = self._bgs["pressed"]
            self._icon_color = "icon_pressed"
            self.update()
            self.setFocus()
            self.clicked.emit()

    def mouseReleaseEvent(  # pylint: disable=invalid-name
        self, event: QMouseEvent
    ) -> None:
        """Event triggered on mouse button release."""
        if event.button() == Qt.LeftButton:
            self._bg_color = self._bgs["released"]
            self._icon_color = "icon_hover"
            self.update()
            self.released.emit()

    def icon_paint(
        self,
        root_painter: QPainter,
        color: str,
        rect: QRect = None,
    ) -> None:
        """Draw svg icon shape in custom color."""
        if not rect:
            # If the button is a square button only showing an icon, the rect()
            # is sufficient, if showing also i.e. a text, a custom rect is
            # necessary.
            rect = self.rect()
        # Define size of pixmap dependent on rect and devicePixelRatio
        scale_factor = root_painter.device().devicePixelRatio()
        width = int(rect.width() * self._margin * scale_factor)
        height = int(rect.height() * self._margin * scale_factor)
        # Get scaled pixmap from store
        pixmap = PixmapStore.inst().get_pixmap(
            self._set_icon_path, width, height, color
        )
        # Set pixmap in the middle of rect with formula
        # x = (rect.width - pixmap width)/2
        # y = (rect.height - pixmap height)/2
        # Define width/height of target rect dependent on scale_factor
        root_painter.drawPixmap(
            int((rect.width() - pixmap.width() / scale_factor) / 2),
            int((rect.height() - pixmap.height() / scale_factor) / 2),
            int(pixmap.width() / scale_factor),
            int(pixmap.height() / scale_factor),
            pixmap,
        )
        # For example rect = 50x50, scale_factor = 2, svg = 1x10
        # --> width, height = 40, pixmap = 4x40, x = 23, y = 5,
        # target rect = 2x20

    def set_icon(self, icon_path: str) -> None:
        """Set the icon to the given path."""
        log.debug("Setting active icon path to %s", icon_path)
        self._set_icon_path = icon_path
        self.update()
