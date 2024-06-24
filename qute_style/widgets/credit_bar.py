"""Credit bar with copyright text on the left and version on the right."""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
)


class CreditBar(QFrame):
    """Credit bar with copyright text on the left and version on the right."""

    def __init__(self, version: str) -> None:
        """Create a new CreditBar."""
        super().__init__()
        self.setObjectName("bg_two_frame")

        self.setFixedHeight(26)

        bg_layout = QHBoxLayout(self)
        bg_layout.setContentsMargins(0, 0, 0, 0)

        copyright_label = QLabel("By: Technical Support Local")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        version_label = QLabel(version)
        version_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        separator = QSpacerItem(
            20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        bg_layout.addWidget(copyright_label)
        bg_layout.addSpacerItem(separator)
        bg_layout.addWidget(version_label)
