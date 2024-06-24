"""BackgroundFrame for the App."""

from __future__ import annotations

from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QWidget,
)


class BackgroundFrame(QFrame):
    """BackgroundFrame for the App."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a new BackgroundFrame."""
        super().__init__(parent=parent)
        self.setObjectName("app_background")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.setGraphicsEffect(shadow)

    def set_stylesheet(self, border_radius: int, border_size: int) -> None:
        """Set the stylesheet with custom border radius and size."""
        self.setStyleSheet(
            f"""
            #app_background {{
                border-radius: {border_radius};
                border: {border_size}px;
                }}
            """
        )
