"""Toggle button (custom checkbox)."""
from typing import Union

from PyQt5.QtCore import (  # type: ignore # for pyqtProperty
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    Qt,
    pyqtProperty,
    pyqtSlot,
)
from PyQt5.QtGui import QColor, QFont, QFontMetrics, QPainter, QPaintEvent
from PyQt5.QtWidgets import QCheckBox, QSizePolicy, QWidget

from tsl.style import get_color


class Toggle(QCheckBox):
    """Toggle button (custom checkbox)."""

    def __init__(self, parent: QWidget = None) -> None:
        """Create a new Toggle."""
        super().__init__(parent)

        self._box_width = 40
        self._box_height = 22
        self._spacer = 5
        self.setMinimumSize(self._box_width, self._box_height)
        self.setMaximumWidth(100)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setCursor(Qt.PointingHandCursor)

        self._position = 3
        self._animation = QPropertyAnimation(self, b"position")
        self._animation.setEasingCurve(QEasingCurve.OutBounce)
        self._animation.setDuration(500)
        self.stateChanged.connect(self.setup_animation)

    @pyqtProperty(float)
    def position(self) -> float:
        """Return actual position."""
        return self._position

    @position.setter  # type: ignore
    def position(self, pos: float):
        """Set actual position."""
        self._position = pos
        self.update()

    @pyqtSlot(int, name="setup_animation")
    def setup_animation(self, value: Qt.CheckState) -> None:
        """Initiate _animation of inner circle."""
        self._animation.stop()
        if value != Qt.Unchecked:
            self._animation.setEndValue(self._box_width / 2)
        else:
            self._animation.setEndValue(4)
        self._animation.start()

    def hitButton(  # pylint: disable=invalid-name
        self, pos: Union[QPoint, QPoint]
    ) -> bool:
        """States if checkbox was hit."""
        return self.contentsRect().contains(pos)

    def paintEvent(  # pylint: disable=invalid-name
        self, _: QPaintEvent
    ) -> None:
        """Draw toggle switch."""
        painter = QPainter(self)
        font = QFont("Segoe UI", 9)
        font_metric = QFontMetrics(font)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setFont(font)

        # Draw Text
        self.setMaximumWidth(
            font_metric.horizontalAdvance(self.text())
            + self._box_width
            + self._spacer
        )
        painter.drawText(
            self._box_width + self._spacer,
            int(self._box_height / 1.35),
            self.text(),
        )

        # Draw Rectangle
        painter.setPen(Qt.NoPen)
        if not self.isEnabled():
            color = get_color("bg_disabled")
        else:
            color = (
                get_color("icon_pressed")
                if self.isChecked()
                else get_color("dark_three")
            )

        painter.setBrush(QColor(color))

        painter.drawRoundedRect(
            0,
            0,
            self._box_width,
            self._box_height,
            12,
            12,
        )
        if not self.isEnabled():
            painter.setBrush(QColor(get_color("fg_disabled")))
        else:
            painter.setBrush(QColor(get_color("icon_color")))
        painter.drawEllipse(self._position, 3, 16, 16)
        painter.end()
