"""Toggle button (custom checkbox)."""
from __future__ import annotations

import logging
from typing import Union, cast

from PyQt5.QtCore import (  # type: ignore # for pyqtProperty
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QSize,
    Qt,
    pyqtProperty,
    pyqtSlot,
)
from PyQt5.QtGui import QFont, QFontMetrics, QPainter, QPaintEvent
from PyQt5.QtWidgets import (
    QCheckBox,
    QSizePolicy,
    QStyle,
    QStylePainter,
    QWidget,
)

from qute_style.qute_style import QuteStyle, ToggleOptionButton
from qute_style.widgets.text_truncator import TextTruncator

log = logging.getLogger(
    f"qute_style.{__name__}"
)  # pylint: disable=invalid-name


class Toggle(QCheckBox, TextTruncator):
    """Toggle button (custom checkbox)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a new Toggle."""
        super().__init__(parent)

        self.setFont(
            QFont(
                QuteStyle.ToggleOptions.FONT_NAME,
                QuteStyle.ToggleOptions.FONT_SIZE,
            )
        )

        # The minimum size is defined by the toggle box's dimensions.
        self.setMinimumHeight(QuteStyle.ToggleOptions.BOX_HEIGHT)
        self.setMinimumWidth(QuteStyle.ToggleOptions.BOX_WIDTH)

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self.setCursor(Qt.PointingHandCursor)

        self._position = QuteStyle.ToggleOptions.CIRCLE_OFFSET

        self._animation = QPropertyAnimation(self, b"position")
        self._animation.setEasingCurve(QEasingCurve.OutBounce)
        self._animation.setDuration(QuteStyle.ToggleOptions.ANIM_DURATION)
        self.stateChanged.connect(self.setup_animation)

    def setTristate(  # pylint: disable=invalid-name
        self, on: bool = True  # pylint: disable=invalid-name
    ) -> None:
        """Override setTristate to ensure it's never set."""
        if on:
            raise ValueError("Toggle cannot use tristate.")
        super().setTristate(on)

    def sizeHint(self) -> QSize:  # pylint: disable=invalid-name
        """Return the size hint."""
        width = QuteStyle.ToggleOptions.BOX_WIDTH
        if self.text():
            width += (
                QFontMetrics(self.font()).horizontalAdvance(self.text())
                + QuteStyle.ToggleOptions.SPACER
            )
        return QSize(width, QuteStyle.ToggleOptions.BOX_HEIGHT)

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
            # Calculate the x-position from the right.
            end = (
                QuteStyle.ToggleOptions.BOX_WIDTH
                - QuteStyle.ToggleOptions.CIRCLE_OFFSET
                - QuteStyle.ToggleOptions.CIRCLE_SIZE
            )
        else:
            # Move the circle back to its initial position
            end = QuteStyle.ToggleOptions.CIRCLE_OFFSET
        self._animation.setEndValue(end)
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
        painter = QStylePainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        option = ToggleOptionButton()
        option.initFrom(self)
        option.text = self.text()
        if self.checkState() == Qt.Checked:
            option.state |= QStyle.State_On
        option.position = int(self.position)

        painter.drawControl(QuteStyle.CE_Toggle, option)
        painter.end()
