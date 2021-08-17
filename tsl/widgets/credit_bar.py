"""Credit bar with copyright text on the left and version on the right."""
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QWidget,
)


class CreditBar(QWidget):
    """Credit bar with copyright text on the left and version on the right."""

    def __init__(self, version: str) -> None:
        """Create a new CreditBar."""
        super().__init__()

        self.setFixedHeight(26)

        widget_layout = QHBoxLayout(self)
        widget_layout.setContentsMargins(0, 0, 0, 0)

        bg_frame = QFrame()
        bg_frame.setObjectName("bg_frame")
        widget_layout.addWidget(bg_frame)

        bg_layout = QHBoxLayout(bg_frame)
        bg_layout.setContentsMargins(0, 0, 0, 0)

        copyright_label = QLabel("By: Technical Support Local")
        copyright_label.setAlignment(Qt.AlignVCenter)

        version_label = QLabel(version)
        version_label.setAlignment(Qt.AlignVCenter)

        separator = QSpacerItem(
            20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        bg_layout.addWidget(copyright_label)
        bg_layout.addSpacerItem(separator)
        bg_layout.addWidget(version_label)
