"""Button on the custom TitleBar."""
import logging
from typing import Tuple

from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QWidget

from tsl.widgets.icon_button import BackgroundColorNames
from tsl.widgets.icon_tooltip_button import IconTooltipButton

log = logging.getLogger("tsl.title_button")  # pylint: disable=invalid-name


class TitleButton(IconTooltipButton):
    """Button on the custom TitleBar (LeftColumnButton with other colors)."""

    FIXED_WIDTH = 30
    FIXED_HEIGHT = 30

    def __init__(  # pylint: disable=too-many-arguments
        self,
        app_parent: QWidget,
        tooltip_text: str,
        icon_path: str,
        parent: QWidget = None,
        bgs: BackgroundColorNames = None,
    ) -> None:
        """Create a new TitleButton."""

        if bgs is None:
            bgs = BackgroundColorNames(
                hovering="bg_three",
                background="bg_two",
                pressed="bg_one",
                released="bg_three",
            )

        super().__init__(
            app_parent, tooltip_text, icon_path, bgs, parent=parent
        )

    def _get_tooltip_coords(self, pos: QPoint) -> Tuple[int, int]:
        """Return the tooltip coords from the global position."""
        pos_x = (pos.x() - self._tooltip.width()) + self.width() + 5
        pos_y = pos.y() + self.height() + 6
        return pos_x, pos_y
