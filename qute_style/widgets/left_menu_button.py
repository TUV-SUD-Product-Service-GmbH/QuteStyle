"""Button for the LeftMenu."""

from __future__ import annotations

import logging
from typing import Generic

from PySide6.QtCore import QEvent, QPoint, QRect, Qt
from PySide6.QtGui import QColor, QMouseEvent, QPainter, QPaintEvent, QPixmap
from PySide6.QtWidgets import QWidget

from qute_style.style import get_color
from qute_style.widgets.icon_button import BackgroundColorNames, IconButton
from qute_style.widgets.icon_tooltip_button import (
    BaseWidgetType,
    IconTooltipButton,
)

log = logging.getLogger(
    f"qute_style.{__name__}"
)  # pylint: disable=invalid-name


class LeftMenuButton(
    IconTooltipButton[BaseWidgetType], Generic[BaseWidgetType]
):
    """Button for the LeftMenu."""

    FIXED_WIDTH = None
    FIXED_HEIGHT = 50

    def __init__(  # noqa: PLR0913
        self,
        app_parent: QWidget,
        text: str,
        tooltip_text: str,
        icon_path: str,
        widget_class: type[BaseWidgetType] | None,
        margin: float = 0.4,
    ) -> None:
        """Create a new LeftMenuButton."""
        bgs = BackgroundColorNames(
            hovering="bg_one",
            background="dark_one",
            pressed="dark_two",
            released="bg_one",
        )
        super().__init__(
            app_parent,
            tooltip_text,
            icon_path,
            bgs,
            text,
            widget_class,
            margin,
        )

        # This can't be a class variable because it gets garbage collected
        # and the app crashes. It should be in the pixmap store.
        self.active_menu = QPixmap(":/svg_icons/active_menu.svg")

        self._is_active_tab = False
        self._is_toggle_active = False

    def __repr__(self) -> str:
        """Return a representation for the LeftMenuButton."""
        name = self.widget_class.__name__ if self.widget_class else None
        return f"<LeftMenuButton '{self.text()} {name}'>"

    def paintEvent(self, _: QPaintEvent) -> None:  # noqa: N802
        """Handle a paint event for the MenuButton."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        # set NoPen so that no borders are drawn.
        painter.setPen(Qt.PenStyle.NoPen)

        if self._is_active:
            indicator_color = get_color("context_color")
            self._draw_button_rect(painter, indicator_color)
        elif self._is_active_tab:
            indicator_color = self._bgs["pressed"]
            self._draw_button_rect(painter, indicator_color)
        else:
            # If the button is neither active (i.e. left column is shown) nor
            # does it belong to the active tab, we draw the hover effect.
            if self._bg_color == "transparent":
                painter.setBrush(QColor(self._bg_color))
            else:
                painter.setBrush(QColor(get_color(self._bg_color)))
            painter.setBrush(QColor(get_color(self._bg_color)))
            rect_inside = QRect(
                4, 5, self.visible_width() - 8, self.height() - 10
            )
            painter.drawRoundedRect(rect_inside, 8, 8)

        if self.visible_width() != self.height():
            # Draw the text. If the button is active or if the button
            # represents the active tab, we'll use color text_active (brighter)
            if self._is_active or self._is_active_tab:
                text_color = get_color("active")
            else:
                text_color = get_color("foreground")
            self._text_paint(painter, QColor(text_color))

        # Draw the icon depending on the hover/click state. If the button is
        # toggled (current menu button), we always draw context_color.
        if self._is_toggle_active:
            color = get_color("context_color")
        else:
            color = get_color(self._icon_color)

        self._icon_paint(painter, QColor(color))

    def _draw_button_rect(
        self, painter: QPainter, indicator_color: str
    ) -> None:
        """Draw the rectangle of the menu button with the given color."""
        painter.setBrush(QColor(indicator_color))
        rect_blue = QRect(4, 5, 20, self.height() - 10)
        painter.drawRoundedRect(rect_blue, 8, 8)
        painter.setBrush(QColor(get_color("bg_one")))
        rect_inside_active = QRect(
            7, 5, self.visible_width(), self.height() - 10
        )
        painter.drawRoundedRect(rect_inside_active, 8, 8)
        self._paint_active_icon(painter)

    def set_active_tab(self, is_active: bool) -> None:
        """
        Set the active tab flag.

        This is set for menu buttons which trigger display of a tab. Set this
        when the triggered tab is active/visible.
        """
        self._is_active_tab = is_active
        if not is_active:
            self._icon_color = "foreground"
            self._bg_color = self._bgs["background"]

        self.update()

    def set_active_toggle(self, active: bool) -> None:
        """Set the toggle active for Buttons that display a different icon."""
        self._is_toggle_active = active

    def _paint_active_icon(self, root_painter: QPainter) -> None:
        """
        Paint a curvy border to the background to the button/icon.

        This is used, when the button is either active or represents the
        active tab.

        Hint: One can use white color for painting to understand fully what
        this method does.
        """
        painter = QPainter(self.active_menu)
        painter.setCompositionMode(
            QPainter.CompositionMode.CompositionMode_SourceIn
        )
        painter.fillRect(self.active_menu.rect(), QColor(get_color("bg_one")))
        root_painter.drawPixmap(self.visible_width() - 5, 0, self.active_menu)
        painter.end()

    def enterEvent(self, event: QEvent) -> None:  # noqa: N802
        """Change style on mouse entering the button area."""
        if (
            self.visible_width() == LeftMenuButton.FIXED_HEIGHT
            and self._tooltip.text()
            and not self._is_active
        ):
            self.move_tooltip()
        IconButton.enterEvent(self, event)

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        """Event triggered on mouse button press."""
        self._tooltip.hide()
        super().mousePressEvent(event)

    def _get_tooltip_coords(self, pos: QPoint) -> tuple[int, int]:
        """Return the tooltip coords from the global position."""
        pos_x = pos.x() + self.visible_width() + 5
        pos_y = pos.y() + (self.visible_width() - self._tooltip.height()) // 2
        return pos_x, pos_y

    def visible_width(self) -> int:
        """
        Return the visible width of self.

        If the LeftMenuButton is part of the ScrollArea, the button-width
        is independent of the menu animation. Several methods of LeftMenuButton
        depend on the visible width of the button and can use this method.
        """
        return self.visibleRegion().boundingRect().width()
