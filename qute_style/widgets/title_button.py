"""Button on the custom TitleBar."""

from __future__ import annotations

import logging

from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QWidget

from qute_style.widgets.base_widgets import BaseWidget
from qute_style.widgets.icon_button import BackgroundColorNames
from qute_style.widgets.icon_tooltip_button import IconTooltipButton

log = logging.getLogger(
    "qute_style.title_button"
)  # pylint: disable=invalid-name


class TitleButton(IconTooltipButton[BaseWidget]):
    """Button on the custom TitleBar (LeftColumnButton with other colors)."""

    FIXED_WIDTH = 30
    FIXED_HEIGHT = 30

    def __init__(  # noqa: PLR0913
        self,
        app_parent: QWidget,
        tooltip_text: str,
        icon_path: str,
        parent: QWidget | None = None,
        bgs: BackgroundColorNames | None = None,
        widget_class: type[BaseWidget] | None = None,
        margin: float = 0.5,
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
            app_parent,
            tooltip_text,
            icon_path,
            bgs,
            parent=parent,
            widget_class=widget_class,
            margin=margin,
        )

    def _get_tooltip_coords(self, pos: QPoint) -> tuple[int, int]:
        """Return the tooltip coords from the global position."""
        pos_x = (pos.x() - self._tooltip.width()) + self.width() + 5
        pos_y = pos.y() + self.height() + 6
        return pos_x, pos_y
