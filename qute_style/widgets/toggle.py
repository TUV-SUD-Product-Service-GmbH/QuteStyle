"""Toggle button (custom checkbox)."""

from __future__ import annotations

import logging

from PySide6.QtCore import (
    Property,
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QSize,
    Qt,
    Slot,
)
from PySide6.QtGui import QFont, QFontMetrics, QPainter, QPaintEvent
from PySide6.QtWidgets import (
    QCheckBox,
    QSizePolicy,
    QStyle,
    QStylePainter,
    QWidget,
)

from qute_style.qute_style import QuteStyle, ToggleOptionButton

log = logging.getLogger(
    f"qute_style.{__name__}"
)  # pylint: disable=invalid-name


class Toggle(QCheckBox):
    """Toggle button (custom checkbox)."""

    # todo: Working, but probably not ok
    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a new Toggle."""
        super().__init__(parent)  # pylint: disable=too-many-function-args

        self.setFont(
            QFont(
                QuteStyle.ToggleOptions.FONT_NAME,
                QuteStyle.ToggleOptions.FONT_SIZE,
            )
        )

        # The minimum size is defined by the toggle box's dimensions.
        self.setMinimumHeight(QuteStyle.ToggleOptions.BOX_HEIGHT)
        self.setMinimumWidth(QuteStyle.ToggleOptions.BOX_WIDTH)

        self.setSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed
        )

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._position = QuteStyle.ToggleOptions.CIRCLE_OFFSET

        self._animation = QPropertyAnimation(self, b"position")
        self._animation.setEasingCurve(QEasingCurve.Type.OutBounce)
        self._animation.setDuration(QuteStyle.ToggleOptions.ANIM_DURATION)
        self.stateChanged.connect(self.setup_animation)

    def setTristate(self, on: bool = True) -> None:  # noqa: N802
        """Override setTristate to ensure it's never set."""
        if on:
            raise ValueError("Toggle cannot use tristate.")
        super().setTristate(on)

    def sizeHint(self) -> QSize:  # noqa: N802
        """Return the size hint."""
        width = QuteStyle.ToggleOptions.BOX_WIDTH
        if self.text():
            width += (
                QFontMetrics(self.font()).horizontalAdvance(self.text())
                + QuteStyle.ToggleOptions.SPACER
            )
        return QSize(width, QuteStyle.ToggleOptions.BOX_HEIGHT)

    @Property(int)
    def position(self) -> int:
        """Return actual position."""
        return self._position

    # todo: Qt property is not recognized properly atm
    @position.setter  # type: ignore[no-redef]
    def position(self, pos: int):
        """Set actual position."""
        self._position = pos
        self.update()

    @Slot(int, name="setup_animation")
    def setup_animation(self, value: Qt.CheckState) -> None:
        """Initiate _animation of inner circle."""
        self._animation.stop()
        if Qt.CheckState(value) == Qt.CheckState.Checked:
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

    def hitButton(self, pos: QPoint | QPoint) -> bool:  # noqa: N802
        """States if checkbox was hit."""
        return self.contentsRect().contains(pos)

    def paintEvent(self, _: QPaintEvent) -> None:  # noqa: N802
        """Draw toggle switch."""
        painter = QStylePainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        option = ToggleOptionButton()
        option.initFrom(self)
        option.text = self.text()
        if self.checkState() == Qt.CheckState.Checked:
            # todo: this works but doesn't seem correct
            option.state |= (  # pylint: disable=no-member
                QStyle.StateFlag.State_On
            )
        option.position = self._position

        painter.drawControl(QuteStyle.CE_Toggle, option)
        painter.end()
