"""Custom Tooltip for a TitleButton."""

import logging

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QLabel, QWidget

log = logging.getLogger("qute_style._tooltip")  # pylint: disable=invalid-name


class ToolTip(QLabel):
    """Custom Tooltip for a TitleButton."""

    def __init__(self, parent: QWidget, tooltip: str) -> None:
        """Create a new Tooltip."""
        super().__init__(text=tooltip, parent=parent)
        self.setObjectName("label_tooltip")
        self.setMinimumHeight(34)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(shadow)

    def show(self) -> None:
        """Show the tooltip and adjust the size before."""
        # Adjust the size. This must be done after the stylesheet was set,
        # because the font settings will change the size needed.
        self.adjustSize()
        super().show()
