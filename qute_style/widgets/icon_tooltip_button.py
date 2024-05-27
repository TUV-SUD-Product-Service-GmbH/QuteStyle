"""IconButton that provides a tooltip."""

from __future__ import annotations

import logging
from typing import Generic, TypeVar

from PySide6.QtCore import QEvent, QPoint
from PySide6.QtWidgets import QWidget

from qute_style.widgets.base_widgets import BaseWidget
from qute_style.widgets.icon_button import BackgroundColorNames, IconButton
from qute_style.widgets.tooltip import ToolTip

log = logging.getLogger(
    f"qute_style.{__name__}"
)  # pylint: disable=invalid-name

BaseWidgetType = TypeVar(  # pylint: disable=invalid-name
    "BaseWidgetType", bound=BaseWidget | None
)


class IconTooltipButton(IconButton, Generic[BaseWidgetType]):
    """IconButton that provides a tooltip."""

    def __init__(  # noqa: PLR0913
        self,
        app_parent: QWidget,
        tooltip_text: str,
        icon_path: str,
        bgs: BackgroundColorNames | None = None,
        text: str | None = None,
        widget_class: type[BaseWidgetType] | None = None,
        margin: float = 0.4,
        parent: QWidget | None = None,
    ) -> None:
        """Create a new IconTooltipButton."""
        super().__init__(parent, icon_path, bgs, text, margin)

        # App is needed to show the tooltip outside the button's rect.
        self._app_parent = app_parent

        self._widget_class: type[BaseWidgetType] | None = widget_class

        self._tooltip = ToolTip(
            app_parent,
            tooltip_text,
        )
        self._tooltip.hide()

    def __repr__(self) -> str:
        """Return a str representation of the object."""
        class_name = (
            self._widget_class.__name__ if self._widget_class else "None"
        )
        return f"<{self.__class__.__name__} for widget {class_name}>"

    @property
    def tooltip_text(self) -> str:
        """Get the tooltip text."""
        return self._tooltip.text()

    @tooltip_text.setter
    def tooltip_text(self, text: str) -> None:
        """Set the tooltip text."""
        self._tooltip.setText(text)

    @property
    def widget_class(
        self,
    ) -> type[BaseWidgetType] | None:
        """Return the widget class the button will trigger."""
        return self._widget_class

    def _get_tooltip_coords(self, pos: QPoint) -> tuple[int, int]:
        """Get the tooltip coordinates from the given position."""
        raise NotImplementedError("Child class must implement this")

    def enterEvent(self, event: QEvent) -> None:  # noqa: N802
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

    def leaveEvent(self, event: QEvent) -> None:  # noqa: N802
        """Change style on mouse entering the button area."""
        self._tooltip.hide()
        super().leaveEvent(event)
