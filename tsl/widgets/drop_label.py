"""
Labels to show information about a file drop area.

The label is shown as long as no files have been dragged
onto the underlying widget.
"""
from typing import cast

from PyQt5.QtCore import QEvent, QObject, Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import (
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from tsl.widgets.icon import Icon


class DropLabel(QWidget):
    """Widget that shows an image and a text at the same time."""

    def __init__(self, text: str, parent: QWidget) -> None:
        """Create a new DropLabel."""
        super().__init__(parent)
        # Define Custom Icon
        icon = Icon(56)
        icon.set_icon(":/svg_icons/cloud_upload.svg")
        icon.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setAlignment(Qt.AlignCenter)
        self.setLayout(QVBoxLayout())
        exp = QSizePolicy.Expanding
        self.layout().addItem(QSpacerItem(40, 20, exp, exp))
        self.layout().addWidget(icon)
        self.layout().setAlignment(icon, Qt.AlignHCenter)
        self.layout().addWidget(text_label)
        self.layout().addItem(QSpacerItem(40, 20, exp, exp))

        self.setFixedSize(parent.size())
        parent.installEventFilter(self)

    def eventFilter(  # pylint: disable=invalid-name
        self, obj: QObject, event: QEvent
    ) -> bool:
        """Handle QResizeEvents from the parent widget."""
        if event.type() == QEvent.Resize and obj is self.parent():
            self.setFixedSize(cast(QResizeEvent, event).size())
        return False
