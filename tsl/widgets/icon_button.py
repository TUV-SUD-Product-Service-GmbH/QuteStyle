"""Simple button showing an icon."""
import logging
from typing import Optional, TypedDict

from PyQt5.QtCore import QEvent, QRect, Qt
from PyQt5.QtGui import (QBrush, QColor, QMouseEvent, QPainter, QPaintEvent,
                         QPixmap)
from PyQt5.QtWidgets import QPushButton, QWidget

from tsl.style import get_color

log = logging.getLogger(f"tsl.{__name__}")  # pylint: disable=invalid-name


class BackgroundColors(TypedDict):
    """Defines background colors used by the button."""

    hovering: str
    no_hovering: str
    pressed: str
    released: str


class IconButton(QPushButton):
    """Simple button showing an icon."""

    FIXED_HEIGHT: Optional[int] = 36
    FIXED_WIDTH: Optional[int] = 36

    def __init__(
        self,
        parent: QWidget = None,
        icon_path: str = ":/svg_icons/no_icon.svg",
        bgs: BackgroundColors = None,
        text: str = None,
    ) -> None:
        """Create a new IconButton."""
        if text:
            super().__init__(text=text, parent=parent)
        else:
            super().__init__(parent=parent)
        if not bgs:
            self._bgs = BackgroundColors(
                hovering=get_color("dark_three"),
                no_hovering=get_color("bg_one"),
                pressed=get_color("dark_four"),
                released=get_color("dark_three"),
            )
        else:
            self._bgs = bgs

        self._set_icon_path = icon_path

        if self.FIXED_WIDTH:
            self.setFixedWidth(self.FIXED_WIDTH)
        if self.FIXED_HEIGHT:
            self.setFixedHeight(self.FIXED_HEIGHT)

        self.setCursor(Qt.PointingHandCursor)

        self._is_active: bool = False

        self._bg_color = self._bgs["no_hovering"]
        self._icon_color = get_color("icon_color")

    def set_active(self, active: bool) -> None:
        """
        Set the button active/inactive.

        A button is active, when the widget which is shown by pressing on the
        button is visible (i.e. right or left widget).
        """
        log.debug("Setting button %s active: %s.", self.objectName(), active)
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
        color = get_color("bg_one") if self._is_active else self._bg_color
        paint.setBrush(QBrush(QColor(color)))
        paint.drawRoundedRect(self.rect(), 8, 8)

        if self.isEnabled():
            color = self._icon_color
        else:
            color = get_color("fg_disabled")
        self.icon_paint(paint, self._set_icon_path, color)

        paint.end()

    def enterEvent(self, _: QEvent) -> None:  # pylint: disable=invalid-name
        """Change style on mouse entering the button area."""
        if self.isEnabled() and not self._is_active:
            self._bg_color = self._bgs["hovering"]
            self._icon_color = get_color("icon_hover")
            self.update()

    def leaveEvent(self, _: QEvent) -> None:  # pylint: disable=invalid-name
        """Change style on mouse leaving the button area."""
        if not self._is_active:
            self._bg_color = self._bgs["no_hovering"]
            self._icon_color = get_color("icon_color")
            self.update()

    def mousePressEvent(  # pylint: disable=invalid-name
        self, event: QMouseEvent
    ) -> None:
        """Event triggered on mouse button press."""
        if event.button() == Qt.LeftButton:
            self._bg_color = self._bgs["pressed"]
            self._icon_color = get_color("icon_pressed")
            self.update()
            self.setFocus()
            self.clicked.emit()

    def mouseReleaseEvent(  # pylint: disable=invalid-name
        self, event: QMouseEvent
    ) -> None:
        """Event triggered on mouse button release."""
        if event.button() == Qt.LeftButton:
            self._bg_color = self._bgs["released"]
            self._icon_color = get_color("icon_hover")
            self.update()
            self.released.emit()

    def icon_paint(
        self,
        root_painter: QPainter,
        image: str,
        color: str,
        rect: QRect = None,
    ) -> None:
        """Draw svg icon shape in custom color."""
        if not rect:
            # If the button is a square button only showing an icon, the rect()
            # is sufficient, if showing also i.e. a text, a custom rect is
            # necessary.
            rect = self.rect()
        icon = QPixmap(image)
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        painter.fillRect(icon.rect(), QColor(color))
        root_painter.drawPixmap(
            int((rect.width() - icon.width()) / 2),
            int((rect.height() - icon.height()) / 2),
            icon,
        )
        painter.end()

    def set_icon(self, icon_path: str) -> None:
        """Set the icon to the given path."""
        log.debug("Setting active icon path to %s", icon_path)
        self._set_icon_path = icon_path
        self.update()
