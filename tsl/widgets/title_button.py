"""Button on the custom TitleBar."""
import logging
from typing import Tuple

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QWidget

from tsl.style import get_color
from tsl.widgets.icon_button import BackgroundColors
from tsl.widgets.icon_tooltip_button import IconTooltipButton

log = logging.getLogger("tsl.title_button")  # pylint: disable=invalid-name


class TitleButton(IconTooltipButton):
    """Button on the custom TitleBar (LeftColumnButton with other colors)."""

    FIXED_WIDTH = 30
    FIXED_HEIGHT = 30

    def __init__(
        self,
        app_parent: QWidget,
        tooltip_text: str,
        icon_path: str,
        parent: QWidget = None,
    ) -> None:
        """Create a new TitleButton."""
        bgs = BackgroundColors(
            hovering=get_color("bg_three"),
            no_hovering=get_color("bg_two"),
            pressed=get_color("bg_one"),
            released=get_color("bg_three"),
        )
        super().__init__(
            app_parent, tooltip_text, icon_path, bgs, parent=parent
        )

    def _get_tooltip_coords(self, pos: QPoint) -> Tuple[int, int]:
        """Return the tooltip coords from the global position."""
        pos_x = (pos.x() - self._tooltip.width()) + self.width() + 5
        pos_y = pos.y() + self.height() + 6
        return pos_x, pos_y
