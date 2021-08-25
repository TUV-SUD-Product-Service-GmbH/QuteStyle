"""Button for the LeftMenu."""
import logging
from typing import Optional, Tuple, Type, Union

from PyQt5.QtCore import QEvent, QPoint, QRect, Qt
from PyQt5.QtGui import QColor, QMouseEvent, QPainter, QPaintEvent, QPixmap
from PyQt5.QtWidgets import QWidget

from tsl.style import get_color
from tsl.widgets.base_widgets import ColumnBaseWidget, MainWidget
from tsl.widgets.icon_button import BackgroundColors
from tsl.widgets.icon_tooltip_button import IconTooltipButton

log = logging.getLogger(f"tsl.{__name__}")  # pylint: disable=invalid-name


class LeftMenuButton(IconTooltipButton):
    """Button for the LeftMenu."""

    FIXED_WIDTH = None
    FIXED_HEIGHT = 50

    def __init__(  # pylint: disable=too-many-arguments
        self,
        app_parent: QWidget,
        text: str,
        tooltip_text: str,
        icon_path: str,
        widget_class: Union[Type[ColumnBaseWidget], Type[MainWidget], None],
    ) -> None:
        """Create a new LeftMenuButton."""
        bgs = BackgroundColors(
            hovering=get_color("dark_three"),
            no_hovering=get_color("dark_one"),
            pressed=get_color("dark_four"),
            released=get_color("dark_three"),
        )
        super().__init__(app_parent, tooltip_text, icon_path, bgs, text)

        # This can't be a class variable because it get's garbage collected
        # and the app crashes. It should be in the pixmap store of baumg-mi.
        self.active_menu = QPixmap(":/svg_icons/active_menu.svg")

        self._widget_class = widget_class

        self._is_active_tab = False
        self._is_toggle_active = False

    def __repr__(self) -> str:
        """Return a representation for the LeftMenuButton."""
        name = self.widget_class.__name__ if self.widget_class else None
        return f"<LeftMenuButton '{self.text()} {name}'>"

    @property
    def widget_class(
        self,
    ) -> Optional[Union[Type[ColumnBaseWidget], Type[MainWidget]]]:
        """Return the widget class the button will trigger."""
        return self._widget_class

    def paintEvent(self, _: QPaintEvent) -> None:
        """Handle a paint event for the MenuButton."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # set NoPen so that no borders are drawn.
        painter.setPen(Qt.NoPen)

        if self._is_active or self._is_active_tab:
            if self._is_active:
                indicator_color = get_color("context_color")
            else:
                indicator_color = self._bgs["pressed"]
            painter.setBrush(QColor(indicator_color))
            rect_blue = QRect(4, 5, 20, self.height() - 10)
            painter.drawRoundedRect(rect_blue, 8, 8)
            painter.setBrush(QColor(get_color("bg_one")))
            rect_inside_active = QRect(7, 5, self.width(), self.height() - 10)
            painter.drawRoundedRect(rect_inside_active, 8, 8)
            self._paint_active_icon(painter)

        else:
            # If the button is neither active (i.e. left column is shown) nor
            # does it belong to the active tab, we draw the hover effect.
            painter.setBrush(QColor(self._bg_color))
            rect_inside = QRect(4, 5, self.width() - 8, self.height() - 10)
            painter.drawRoundedRect(rect_inside, 8, 8)

        if self.width() != self.height():
            # Draw the text. If the button is active or if the button
            # represents the active tab, we'll use color text_active (brighter)
            if self._is_active or self._is_active_tab:
                text_color = get_color("text_active")
            else:
                text_color = get_color("text_foreground")
            painter.setPen(QColor(text_color))
            painter.setFont(self.font())
            rect_text = QRect(45, 0, self.width() - 50, self.height())
            painter.drawText(rect_text, Qt.AlignVCenter, self.text())

        # Draw the icon depending of the hover/click state. If the button is
        # toggled (currently menu button), we always draw context_color.
        if self._is_toggle_active:
            color = get_color("context_color")
        else:
            color = self._icon_color

        # The height of the button defines the rectangle in which the icon is
        # painted, independent of the button's width.
        paint_rect = QRect(0, 0, self.height(), self.height())
        self.icon_paint(painter, color, paint_rect)

    def set_active_tab(self, is_active: bool) -> None:
        """
        Set the active tab flag.

        This is set for menu buttons which trigger display of a tab. Set this
        when the triggered tab is active/visible.
        """
        self._is_active_tab = is_active
        if not is_active:
            self._icon_color = get_color("icon_color")
            self._bg_color = self._bgs["no_hovering"]

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
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(self.active_menu.rect(), QColor(get_color("bg_one")))
        root_painter.drawPixmap(self.width() - 5, 0, self.active_menu)
        painter.end()

    def enterEvent(  # pylint: disable=invalid-name
        self, event: QEvent
    ) -> None:
        """Change style on mouse entering the button area."""
        if self.width() == 50 and self._tooltip.text() and not self._is_active:
            self.move_tooltip()
        super().enterEvent(event)

    def mousePressEvent(  # pylint: disable=invalid-name
        self, event: QMouseEvent
    ) -> None:
        """Event triggered on mouse button press."""
        self._tooltip.hide()
        super().mousePressEvent(event)

    def _get_tooltip_coords(self, pos: QPoint) -> Tuple[int, int]:
        """Return the tooltip coords from the global position."""
        pos_x = pos.x() + self.width() + 5
        pos_y = pos.y() + (self.width() - self._tooltip.height()) // 2
        return pos_x, pos_y
