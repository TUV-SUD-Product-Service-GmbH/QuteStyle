"""IconButton that provides a tooltip."""
import logging
from typing import Tuple

from PyQt5.QtCore import QEvent, QPoint
from PyQt5.QtWidgets import QWidget

from tsl.widgets.icon_button import BackgroundColorNames, IconButton
from tsl.widgets.tooltip import ToolTip

log = logging.getLogger(f"tsl.{__name__}")  # pylint: disable=invalid-name


class IconTooltipButton(IconButton):
    """IconButton that provides a tooltip."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        app_parent: QWidget,
        tooltip_text: str,
        icon_path: str,
        bgs: BackgroundColorNames = None,
        text: str = None,
        parent: QWidget = None,
    ) -> None:
        """Create a new IconTooltipButton."""
        super().__init__(parent, icon_path, bgs, text)

        # App is needed to show the tooltip outside of the button's rect.
        self._app_parent = app_parent

        self._tooltip = ToolTip(
            app_parent,
            tooltip_text,
        )
        self._tooltip.hide()

    def _get_tooltip_coords(self, pos: QPoint) -> Tuple[int, int]:
        """Get the tooltip coordinates from the given position."""
        raise NotImplementedError("Child class must implement this")

    def enterEvent(  # pylint: disable=invalid-name
        self, event: QEvent
    ) -> None:
        """Change style on mouse entering the button area."""
        self.move_tooltip()
        super().enterEvent(event)

    def move_tooltip(self) -> None:
        """Move the button tooltip to the correct position and show it."""
        # GET MAIN WINDOW PARENT
        global_pos = self.mapToGlobal(QPoint(0, 0))
        # SET WIDGET TO GET POSTION
        # Return absolute position of widget inside app
        pos = self._app_parent.mapFromGlobal(global_pos)
        # FORMAT POSITION
        # Adjust _tooltip position with offset
        pos_x, pos_y = self._get_tooltip_coords(pos)
        # SET POSITION TO WIDGET
        # Move _tooltip position
        self._tooltip.move(pos_x, pos_y)
        self._tooltip.show()

    def leaveEvent(  # pylint: disable=invalid-name
        self, event: QEvent
    ) -> None:
        """Change style on mouse entering the button area."""
        self._tooltip.hide()
        super().leaveEvent(event)
