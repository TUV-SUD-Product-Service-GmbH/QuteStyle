"""
Labels to show information about a file drop area.

The label is shown as long as no files have been dragged
onto the underlying widget.
"""

from typing import cast

from PySide6.QtCore import QEvent, QObject, Qt
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import (
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from qute_style.widgets.icon import Icon


class DropLabel(QWidget):
    """Widget that shows an image and a text at the same time."""

    def __init__(self, text: str, parent: QWidget) -> None:
        """Create a new DropLabel."""
        super().__init__(parent)
        # Define Custom Icon
        icon = Icon(56)
        icon.set_icon(":/svg_icons/cloud_upload.svg")
        icon.setSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum
        )
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(QVBoxLayout())
        exp = QSizePolicy.Policy.Expanding
        self.layout().addItem(QSpacerItem(40, 20, exp, exp))
        self.layout().addWidget(icon)
        self.layout().setAlignment(icon, Qt.AlignmentFlag.AlignHCenter)
        self.layout().addWidget(text_label)
        self.layout().addItem(QSpacerItem(40, 20, exp, exp))

        self.setFixedSize(parent.size())
        parent.installEventFilter(self)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:  # noqa: N802
        """Handle QResizeEvents from the parent widget."""
        if event.type() == QEvent.Type.Resize and obj is self.parent():
            self.setFixedSize(cast(QResizeEvent, event).size())
        return False
