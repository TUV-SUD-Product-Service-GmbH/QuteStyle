"""Container widget."""

from PySide6.QtWidgets import QFrame, QHBoxLayout, QWidget


class Div(QWidget):
    """Container widget."""

    def __init__(self) -> None:
        """Create a new div."""
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)
        frame_line = QFrame()
        frame_line.setObjectName("div")
        frame_line.setFixedHeight(20)
        layout.addWidget(frame_line)
        self.setFixedHeight(6)
