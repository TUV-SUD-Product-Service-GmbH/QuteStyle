"""Simple button showing an icon."""

from __future__ import annotations

import logging
from typing import TypedDict

from PySide6.QtCore import QEvent, QRect, Qt
from PySide6.QtGui import QBrush, QColor, QMouseEvent, QPainter, QPaintEvent
from PySide6.QtWidgets import QPushButton, QWidget

from qute_style.style import get_color
from qute_style.widgets.custom_icon_engine import PixmapStore

log = logging.getLogger(
    f"qute_style.{__name__}"
)  # pylint: disable=invalid-name

# todo: QWIDGETSIZE_MAX is a constant in C++ but not available in PySide6.
#  What now?
QWIDGETSIZE_MAX = (1 << 24) - 1


class BackgroundColorNames(TypedDict):
    """Defines background colors used by the button."""

    hovering: str
    background: str
    pressed: str
    released: str


class IconButton(QPushButton):
    """Simple button showing an icon."""

    FIXED_HEIGHT: int = 36
    FIXED_WIDTH: int | None = 36

    def __init__(  # noqa: PLR0913
        self,
        parent: QWidget | None = None,
        icon_path: str = ":/svg_icons/no_icon.svg",
        bgs: BackgroundColorNames | None = None,
        text: str | None = None,
        margin: float = 0.6,
    ) -> None:
        """Create a new IconButton."""
        if text:
            super().__init__(text, parent)
        else:
            super().__init__(parent)
        self._bgs = bgs or BackgroundColorNames(
            hovering="bg_elements",
            background="transparent",
            pressed="dark_two",
            released="bg_elements",
        )

        self._set_icon_path = icon_path

        self.set_sizes()

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._is_active: bool = False

        self._bg_color = self._bgs["background"]
        self._icon_color = "foreground"
        self._text_color = "foreground"
        self._margin = margin

    def set_sizes(self) -> None:
        """
        Set the size of the button.

        The button normally has a fixed height (it's untested without).
        The width is fixed if set and if not text was set.
        """
        if self.FIXED_WIDTH and not self.text():
            self.setFixedWidth(self.FIXED_WIDTH)
        else:
            self.setFixedWidth(QWIDGETSIZE_MAX)
        self.setFixedHeight(self.FIXED_HEIGHT)

    def setText(self, text: str) -> None:  # noqa: N802
        """Set the text on the button."""
        super().setText(text)
        self.set_sizes()
        self.update()

    def set_active(self, active: bool) -> None:
        """
        Set the button active/inactive.

        A button is active, when the widget which is shown by pressing on the
        button is visible (i.e. right or left widget).
        """
        log.debug("Setting button '%s' active: %s.", self, active)
        self._is_active = active
        self.update()

    def paintEvent(self, _: QPaintEvent) -> None:  # noqa: N802
        """Customize painting of the button and icon."""
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        if self._bg_color == "transparent":
            painter.setBrush(QBrush(QColor(self._bg_color)))
        else:
            painter.setBrush(QBrush(QColor(get_color(self._bg_color))))
        painter.drawRoundedRect(self.rect(), 8, 8)

        if self.isEnabled():
            color = get_color(self._icon_color)
            text_color = get_color(self._text_color)
        else:
            color = get_color("fg_disabled")
            text_color = get_color("fg_disabled")
        self._icon_paint(painter, QColor(color))
        self._text_paint(painter, QColor(text_color))
        painter.end()

    def enterEvent(self, _: QEvent) -> None:  # noqa: N802
        """Change style on mouse entering the button area."""
        if self.isEnabled() and not self._is_active:
            self._bg_color = self._bgs["hovering"]
            self._icon_color = "active"
            self._text_color = "foreground"
            self.update()

    def leaveEvent(self, _: QEvent) -> None:  # noqa: N802
        """Change style on mouse leaving the button area."""
        if not self._is_active:
            self._bg_color = self._bgs["background"]
            self._icon_color = "foreground"
            self._text_color = "foreground"
            self.update()

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        """Event triggered on mouse button press."""
        if event.button() is Qt.MouseButton.LeftButton:
            self._bg_color = self._bgs["pressed"]
            self._icon_color = "context_pressed"
            self._text_color = "context_pressed"
            self.update()
            self.setFocus()
            self.clicked.emit()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        """Event triggered on mouse button release."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._bg_color = self._bgs["released"]
            self._icon_color = "active"
            self._text_color = "foreground"
            self.update()
            self.released.emit()

    def _icon_paint(
        self,
        root_painter: QPainter,
        color: QColor,
    ) -> None:
        """
        Draw svg icon shape in custom color.

        The icon is always drawn at the top left corner of the button, with a
        square that has a side length of self.FIXED_HEIGHT.
        """
        # Define size of pixmap dependent on FIXED_HEIGHT and devicePixelRatio
        scale_factor = root_painter.device().devicePixelRatio()
        length = int(self.FIXED_HEIGHT * self._margin * scale_factor)

        # Get scaled pixmap from store
        pixmap = PixmapStore.inst().get_pixmap(
            self._set_icon_path, length, length, color.name()
        )
        # Set pixmap in the middle of rect (length FIXED_HEIGHT) with formula
        # x = (FIXED_HEIGHT - pixmap width)/2
        # y = (FIXED_HEIGHT - pixmap height)/2
        # Define width/height of target rect dependent on scale_factor
        root_painter.drawPixmap(
            int((self.FIXED_HEIGHT - pixmap.width() / scale_factor) / 2),
            int((self.FIXED_HEIGHT - pixmap.height() / scale_factor) / 2),
            int(pixmap.width() / scale_factor),
            int(pixmap.height() / scale_factor),
            pixmap,
        )
        # For example rect = 50x50, scale_factor = 2, svg = 1x10
        # --> width, height = 40, pixmap = 4x40, x = 23, y = 5,
        # target rect = 2x20

    def _text_paint(self, root_painter: QPainter, text_color: QColor) -> None:
        """Paint the text in the given color."""
        if not self.text():
            return
        root_painter.setPen(text_color)

        # Create a rect from the button's total rect without the rect for the
        # icon. This means, the rect is shifted to the left by FIXED_HEIGHT
        # and then cut of so it isn't larger than self.rect().
        rect_text = QRect(
            self.rect().x() + self.FIXED_HEIGHT,
            0,
            self.width() - self.FIXED_HEIGHT,
            self.height(),
        )
        root_painter.drawText(
            rect_text, Qt.AlignmentFlag.AlignVCenter, self.text()
        )

    def set_icon(self, icon_path: str) -> None:
        """Set the icon to the given path."""
        log.debug("Setting active icon path to %s", icon_path)
        self._set_icon_path = icon_path
        self.update()
