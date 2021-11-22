"""Toggle button (custom checkbox)."""
import logging
from typing import Union

from PyQt5.QtCore import (  # type: ignore # for pyqtProperty
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QSize,
    Qt,
    pyqtProperty,
    pyqtSlot,
)
from PyQt5.QtGui import (
    QColor,
    QFont,
    QFontMetrics,
    QMoveEvent,
    QPainter,
    QPaintEvent,
    QPen,
)
from PyQt5.QtWidgets import QCheckBox, QSizePolicy, QWidget

from tsl.style import get_color
from tsl.widgets.text_truncator import TextTruncator

log = logging.getLogger(f"tsl.{__name__}")  # pylint: disable=invalid-name


class Toggle(QCheckBox, TextTruncator):
    """Toggle button (custom checkbox)."""

    _FONT = QFont("Segoe UI", 8)

    # This is the offset with which the circle is shown on both sides.
    _CIRCLE_OFFSET = 3

    # Size of the circle.
    _CIRCLE_SIZE = 16

    # Width of the Box, Height is based on the circle.
    _BOX_WIDTH = 40

    # Spacer between the text and the toggle box.
    _SPACER = 5

    # Duration of the animation.
    _ANIM_DURATION = 500

    def __init__(self, parent: QWidget = None) -> None:
        """Create a new Toggle."""
        super().__init__(parent)

        # Minimum width is the BOX_WIDTH, the height can be calculated
        height = Toggle._CIRCLE_SIZE + (2 * Toggle._CIRCLE_OFFSET)

        # We're at least as wide as the toggle box is. Nevertheless we want to
        # be as wide as the size hint to show the full text. Height is fixed.
        self.setMinimumWidth(Toggle._BOX_WIDTH)
        self.setFixedHeight(height)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.setCursor(Qt.PointingHandCursor)

        self._position = Toggle._CIRCLE_OFFSET

        self._animation = QPropertyAnimation(self, b"position")
        self._animation.setEasingCurve(QEasingCurve.OutBounce)
        self._animation.setDuration(Toggle._ANIM_DURATION)
        self.stateChanged.connect(self.setup_animation)

        # Set the font metrics for text length calculation.
        self._font_metrics: QFontMetrics = QFontMetrics(Toggle._FONT)

        # Store the preferred text width to calculate the size hint.
        self._preferred_width = 0

        # Remember the screen we're on.
        self.current_screen = self.screen()

    def moveEvent(  # pylint: disable=invalid-name
        self, event: QMoveEvent
    ) -> None:
        """
        Detect a screen change when moving the Toggle.

        When a screen change is detected, the preferred text size is
        recalculated and stored.
        """
        if self.current_screen != self.screen():
            log.debug("Current screen has changed, updating geometry.")
            self.current_screen = self.screen()
            self._preferred_width = self._font_metrics.horizontalAdvance(
                self.text()
            )
            self.updateGeometry()
        return super().moveEvent(event)

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
                Toggle._BOX_WIDTH - Toggle._CIRCLE_OFFSET - Toggle._CIRCLE_SIZE
            )
        else:
            # Move the circle back to its initial position
            end = Toggle._CIRCLE_OFFSET
        self._animation.setEndValue(end)
        self._animation.start()

    def hitButton(  # pylint: disable=invalid-name
        self, pos: Union[QPoint, QPoint]
    ) -> bool:
        """States if checkbox was hit."""
        return self.contentsRect().contains(pos)

    def sizeHint(self) -> QSize:  # pylint: disable=invalid-name
        """Return the size hint."""
        factor = self.screen().logicalDotsPerInchX() / 96.0
        width = (
            int(self._preferred_width * factor)
            + Toggle._BOX_WIDTH
            + Toggle._SPACER
        )
        log.debug(
            "Width in size hint for Toggle: %s with factor %s", width, factor
        )
        return QSize(width, self.height())

    def setText(self, text: str) -> None:  # pylint: disable=invalid-name
        """Override setText to calculate a new minimum width."""
        self._preferred_width = self._font_metrics.horizontalAdvance(text)
        super().setText(text)

    def _draw_text(self, painter: QPainter, offset: int, width: int) -> None:
        """Draw Text."""
        if self.isEnabled():
            color = QColor(get_color("foreground"))
        else:
            color = QColor(get_color("fg_disabled"))

        painter.setPen(QPen(color))
        painter.setFont(Toggle._FONT)
        text = self.truncate_text(self.text(), width, self._font_metrics)
        y_pos = (self.height() - text.size().height()) / 2
        painter.drawStaticText(offset, int(y_pos), text)

    def _draw_checkbox(self, painter: QPainter, offset: int) -> None:
        """Draw the checkbox."""
        painter.setPen(Qt.NoPen)
        if not self.isEnabled():
            color = get_color("bg_disabled")
            fg_color = QColor(get_color("fg_disabled"))
        else:
            fg_color = QColor(get_color("foreground"))
            if self.isChecked():
                color = get_color("context_color")
            else:
                color = get_color("dark_two")

        painter.setBrush(QColor(color))

        height = self.height()
        painter.drawRoundedRect(
            offset,
            0,
            Toggle._BOX_WIDTH,
            height,
            12,
            12,
        )
        painter.setBrush(fg_color)
        painter.drawEllipse(
            self._position + offset,
            Toggle._CIRCLE_OFFSET,
            Toggle._CIRCLE_SIZE,
            Toggle._CIRCLE_SIZE,
        )

    def paintEvent(  # pylint: disable=invalid-name
        self, _: QPaintEvent
    ) -> None:
        """Draw toggle switch."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        if not self.text():
            self._draw_checkbox(painter, 0)
        else:
            # Use the available space. If more space is available, use the
            # calculated preferred text width.
            text_width = min(
                self.width() - Toggle._BOX_WIDTH - Toggle._SPACER,
                self._preferred_width,
            )

            if self.layoutDirection() == Qt.LeftToRight:
                self._draw_checkbox(painter, 0)
                self._draw_text(
                    painter, Toggle._BOX_WIDTH + Toggle._SPACER, text_width
                )
            else:  # Qt.RightToLeft:
                # Calculate the offset for the case that more space is
                # available than needed for the text. Otherwise (the calc is
                # negative) we use 0 and crop the text in _draw_text.
                offset = max(
                    self.width()
                    - Toggle._BOX_WIDTH
                    - Toggle._SPACER
                    - self._preferred_width,
                    0,
                )
                self._draw_text(painter, offset, text_width)
                self._draw_checkbox(
                    painter, offset + Toggle._SPACER + text_width
                )
        painter.end()
