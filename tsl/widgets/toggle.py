"""Toggle button (custom checkbox)."""
from __future__ import annotations

import logging
from typing import Union, cast

from PyQt5.QtCore import (  # type: ignore # for pyqtProperty
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QRect,
    QSize,
    Qt,
    pyqtProperty,
    pyqtSlot,
)
from PyQt5.QtGui import (
    QColor,
    QFont,
    QFontMetrics,
    QPainter,
    QPaintEvent,
    QPalette,
)
from PyQt5.QtWidgets import (
    QCheckBox,
    QCommonStyle,
    QSizePolicy,
    QStyle,
    QStyleOption,
    QStyleOptionButton,
    QStylePainter,
    QWidget,
)

from tsl.style import get_color
from tsl.widgets.text_truncator import TextTruncator

log = logging.getLogger(f"tsl.{__name__}")  # pylint: disable=invalid-name


class ToggleStyle(QCommonStyle):
    """Custom QStyle for drawing a Toggle."""

    class ToggleOptions:  # pylint: disable=too-few-public-methods
        """Toggle configuration."""

        # This is the offset with which the circle is shown on both sides and
        # on top and bottom of the box.
        CIRCLE_OFFSET = 3

        # Diameter of the circle.
        CIRCLE_SIZE = 16

        # Font definitions
        FONT_SIZE = 9
        # Todo: This font is not a good font for the ui. fix with 70912
        FONT_NAME = "Segoe UI"

        # Width and height of the Box
        BOX_WIDTH = 40
        BOX_HEIGHT = CIRCLE_SIZE + (2 * CIRCLE_OFFSET)

        # Spacer between the text and the toggle box.
        SPACER = 5

        # Duration of the animation.
        ANIM_DURATION = 500

    def standardPalette(self) -> QPalette:  # pylint: disable=invalid-name
        """Return the QStyle's standard QPalette."""
        palette = super().standardPalette()
        palette.setColor(
            QPalette.Normal,
            QPalette.WindowText,
            QColor(get_color("foreground")),
        )
        palette.setColor(
            QPalette.Disabled,
            QPalette.WindowText,
            QColor(get_color("fg_disabled")),
        )
        palette.setColor(
            QPalette.Inactive,
            QPalette.WindowText,
            QColor(get_color("foreground")),
        )
        palette.setColor(
            QPalette.Normal, QPalette.Base, QColor(get_color("dark_two"))
        )
        palette.setColor(
            QPalette.Inactive, QPalette.Base, QColor(get_color("dark_two"))
        )
        palette.setColor(
            QPalette.Disabled, QPalette.Base, QColor(get_color("bg_disabled"))
        )

        return palette

    def background_color(self, option: QStyleOptionButton) -> QColor:
        """Return the color to print the Toggle's background."""
        if not option.state & QStyle.State_Enabled:
            return self.standardPalette().color(
                QPalette.Inactive, QPalette.Base
            )
        if option.state & QStyle.State_On:
            return QColor(get_color("context_color"))
        return self.standardPalette().color(QPalette.Normal, QPalette.Base)

    @staticmethod
    def toggle_color(option: QStyleOptionButton) -> str:
        """Return the color to print the Toggle's circle."""
        if option.state & QStyle.State_Enabled:
            return get_color("foreground")
        return get_color("fg_disabled")

    @staticmethod
    def _toggle_x(option: QStyleOption) -> int:
        """Calculate x position of Toggle box."""
        if option.direction == Qt.LeftToRight:
            x_pos = 0
        else:
            x_pos = option.rect.width() - ToggleStyle.ToggleOptions.BOX_WIDTH
        return x_pos

    @staticmethod
    def _label_x(option: QStyleOption) -> int:
        """Calculate x position of label."""
        if option.direction == Qt.LeftToRight:
            x_pos = (
                ToggleStyle.ToggleOptions.BOX_WIDTH
                + ToggleStyle.ToggleOptions.SPACER
            )
        else:
            x_pos = 0
        return x_pos

    def drawControl(  # pylint: disable=invalid-name
        self,
        element: QStyle.ControlElement,
        option: QStyleOption,
        painter: QPainter,
        widget: QWidget | None = None,
    ) -> None:
        """Draw the checkbox."""
        if element == QStyle.CE_CheckBox and isinstance(widget, Toggle):
            if not isinstance(option, QStyleOptionButton):
                raise AssertionError(
                    f"Expected option type QStyleOptionButton, "
                    f"got {type(option)}"
                )
            x_pos = self._toggle_x(option)
            toggle_rect = QRect(
                x_pos,
                0,
                ToggleStyle.ToggleOptions.BOX_WIDTH,
                ToggleStyle.ToggleOptions.BOX_HEIGHT,
            )
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(self.background_color(option)))
            painter.drawRoundedRect(toggle_rect, 12, 12)
            painter.setBrush(QColor(self.toggle_color(option)))
            painter.drawEllipse(
                x_pos + cast(int, widget.position),
                ToggleStyle.ToggleOptions.CIRCLE_OFFSET,
                ToggleStyle.ToggleOptions.CIRCLE_SIZE,
                ToggleStyle.ToggleOptions.CIRCLE_SIZE,
            )
            if option.text:
                self.drawControl(
                    QStyle.CE_CheckBoxLabel,
                    option,
                    painter,
                    widget,
                )
        elif element == QStyle.CE_CheckBoxLabel:
            if not isinstance(option, QStyleOptionButton):
                raise AssertionError(
                    f"Expected option type QStyleOptionButton, "
                    f"got {type(option)}"
                )
            option.palette = self.standardPalette()
            x_pos = self._label_x(option)
            text_rect = QRect(
                x_pos,
                0,
                option.rect.width()
                - ToggleStyle.ToggleOptions.BOX_WIDTH
                - ToggleStyle.ToggleOptions.SPACER,
                option.rect.height(),
            )
            option.rect = text_rect
            option.text = option.fontMetrics.elidedText(
                option.text, Qt.ElideRight, option.rect.width()
            )
            super().drawControl(element, option, painter, widget)


class Toggle(QCheckBox, TextTruncator):
    """Toggle button (custom checkbox)."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a new Toggle."""
        super().__init__(parent)

        self.setFont(
            QFont(
                ToggleStyle.ToggleOptions.FONT_NAME,
                ToggleStyle.ToggleOptions.FONT_SIZE,
            )
        )

        # Todo: This must ultimately be moved to a QApplication-wide style.
        self.setStyle(ToggleStyle())

        # The minimum size is defined by the toggle box's dimensions.
        self.setMinimumHeight(ToggleStyle.ToggleOptions.BOX_HEIGHT)
        self.setMinimumWidth(ToggleStyle.ToggleOptions.BOX_WIDTH)

        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        self.setCursor(Qt.PointingHandCursor)

        self._position = ToggleStyle.ToggleOptions.CIRCLE_OFFSET

        self._animation = QPropertyAnimation(self, b"position")
        self._animation.setEasingCurve(QEasingCurve.OutBounce)
        self._animation.setDuration(ToggleStyle.ToggleOptions.ANIM_DURATION)
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
        width = ToggleStyle.ToggleOptions.BOX_WIDTH
        if self.text():
            width += (
                QFontMetrics(self.font()).horizontalAdvance(self.text())
                + ToggleStyle.ToggleOptions.SPACER
            )
        return QSize(width, ToggleStyle.ToggleOptions.BOX_HEIGHT)

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
                ToggleStyle.ToggleOptions.BOX_WIDTH
                - ToggleStyle.ToggleOptions.CIRCLE_OFFSET
                - ToggleStyle.ToggleOptions.CIRCLE_SIZE
            )
        else:
            # Move the circle back to its initial position
            end = ToggleStyle.ToggleOptions.CIRCLE_OFFSET
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

        option = QStyleOptionButton()
        option.initFrom(self)
        option.text = self.text()
        if self.checkState() == Qt.Checked:
            option.state |= QStyle.State_On

        painter.drawControl(ToggleStyle.CE_CheckBox, option)
        painter.end()
