"""Icon that can be painted in any given color."""
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QPixmap
from PyQt5.QtWidgets import QLabel

from tsl.style import get_color


class Icon(QLabel):
    """Icon that can be painted in any given color."""

    def __init__(self) -> None:
        """Create a new Icon."""
        super().__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setAlignment(Qt.AlignCenter)
        self.setFixedSize(30, 30)

    def set_icon(self, icon_path: str) -> None:
        """Set the given icon in the given color."""
        icon = QPixmap(icon_path)
        painter = QPainter(icon)
        painter.setCompositionMode(QPainter.CompositionMode_SourceIn)
        painter.fillRect(icon.rect(), QColor(get_color("icon_color")))
        painter.end()

        self.setPixmap(icon)
