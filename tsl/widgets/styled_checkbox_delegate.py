"""Delegate for altering appearance of a checkbox in a view."""

from PyQt5.QtCore import QModelIndex, QPoint, QRect, QSize, Qt
from PyQt5.QtGui import QBrush, QColor, QPainter, QPaintEvent, QStaticText
from PyQt5.QtWidgets import (
    QCheckBox,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QWidget,
)

from tsl.style import get_color
from tsl.widgets.custom_icon_engine import PixmapStore
from tsl.widgets.text_truncator import TextTruncator


def get_icon_path(state: Qt.CheckState) -> str:
    """Get icon path depending on state."""
    if state == Qt.Checked:
        path = ":/svg_icons/checkbox_checked.svg"
    elif state == Qt.PartiallyChecked:
        path = ":/svg_icons/checkbox_indeterminate.svg"
    else:
        path = ":/svg_icons/checkbox_unchecked.svg"
    return path


def get_state_color(state: QStyle.StateFlag) -> str:
    """Get disabled/enabled color depending on state."""
    if state & QStyle.State_Selected or state & QStyle.State_MouseOver:
        return get_color("active")
    if state & QStyle.State_Enabled:
        return get_color("foreground")
    return get_color("fg_disabled")


def draw_checkbox(
    painter: QPainter, rect: QRect, path: str, color: str
) -> None:
    """Draws checkbox."""

    scale = painter.device().devicePixelRatio()
    store = PixmapStore.inst()
    painter.drawPixmap(
        rect,
        store.get_pixmap(
            path,
            scale * rect.width(),
            scale * rect.height(),
            color,
        ),
    )


class StyledCheckboxDelegate(QStyledItemDelegate, TextTruncator):
    """Delegate for altering appearance of a checkbox in a view."""

    def paint(  # pylint: disable=no-self-use
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> None:
        """Implement custom painting."""

        if index.data(Qt.CheckStateRole) is None:
            super().paint(painter, option, index)
            return
        # Save the painter and restore it later as recommended in the doc:
        # https://doc.qt.io/qt-5/qstyleditemdelegate.html#paint
        painter.save()

        # Check if we need to paint a background.
        if (
            option.state & QStyle.State_Selected  # type: ignore
            or option.state & QStyle.State_MouseOver  # type: ignore
        ):
            # Get the background color depending on the two cases:
            color = get_color(
                "context_pressed"
                if option.state & QStyle.State_Selected  # type: ignore
                else "context_color"
            )
            # Save the pen, since we draw the background with a brush
            pen = painter.pen()
            # Set the text color for hovered or selected items.
            pen.setColor(QColor(get_color("active")))
            painter.setBrush(QBrush(QColor(color)))
            painter.setPen(Qt.NoPen)
            painter.drawRect(option.rect)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)

        # If there is not enough space for the checkbox nothing is shown
        # This prevents the overlap of checkboxes with neighbouring columns
        if option.rect.width() < option.rect.height():
            return

        # Calculate a simple rect for the checkbox that is the max size square
        # from the rectangle we paint in.
        checkbox_rect = QRect(option.rect)
        # width == height
        checkbox_rect.setWidth(checkbox_rect.height())

        # Paint icon depending on CheckState.
        icon_path = get_icon_path(index.data(Qt.CheckStateRole))

        # Set color depending on state
        color = get_state_color(option.state)  # type: ignore

        # Draw CheckBox Icon
        draw_checkbox(painter, checkbox_rect, icon_path, color)

        # Calculate a rect for the text.
        text_rect = QRect(
            option.rect.x() + checkbox_rect.width(),
            option.rect.y(),
            option.rect.width() - checkbox_rect.width(),
            checkbox_rect.height(),
        )
        elided_text = self.truncate_text(
            index.data(), text_rect.width(), option.fontMetrics
        )

        # Draw the text
        painter.drawStaticText(text_rect.x(), text_rect.y(), elided_text)

        painter.restore()


class StyledCheckBox(QCheckBox, TextTruncator):
    """Styled Version of CheckBox."""

    SPACER = 4

    def __init__(self, parent: QWidget = None):
        """Initialize Checkbox with static text."""
        super().__init__(parent)
        self._text = QStaticText()
        self._text.setPerformanceHint(QStaticText.AggressiveCaching)
        self._text.setTextFormat(Qt.PlainText)

    def setText(self, text: str) -> None:  # pylint: disable=invalid-name
        """Save text as static text."""
        self._text.setText(text)
        super().setText(text)

    def sizeHint(self) -> QSize:  # pylint: disable=invalid-name
        """Compute size Hint."""
        width = int(
            self.iconSize().width() + self.SPACER + self._text.size().width()
        )
        height = int(self.iconSize().height())
        return QSize(width, height)

    def paintEvent(  # pylint: disable=invalid-name, unused-argument
        self, event: QPaintEvent
    ) -> None:
        """Implement custom painting."""

        painter = QPainter(self)
        # Define rect for CheckBox Icon
        checkbox_rect = QRect(
            QPoint(self.rect().x(), self.rect().y()), self.iconSize()
        )

        # Paint icon depending on CheckState.
        icon_path = get_icon_path(self.checkState())

        # Set color depending on state
        color = get_state_color(
            QStyle.State_Enabled if self.isEnabled() else QStyle.State_None
        )
        painter.setPen(QColor(color))

        # Draw CheckBox Icon
        draw_checkbox(painter, checkbox_rect, icon_path, color)

        # Calculate a rect for the text.
        text_rect = QRect(
            checkbox_rect.width() + self.SPACER,
            0,
            self.width() - self.SPACER - checkbox_rect.width(),
            self.height(),
        )

        # Shorten text, if if cannot be fully displayed
        elided_text = self.truncate_text(
            self._text.text(), text_rect.width(), self.fontMetrics()
        )

        # Draw the text
        painter.drawStaticText(text_rect.x(), text_rect.y(), elided_text)

        painter.end()
