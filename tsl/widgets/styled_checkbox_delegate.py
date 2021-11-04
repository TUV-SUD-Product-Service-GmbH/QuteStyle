"""Delegate for altering appearance of a checkbox in a view."""
from PyQt5.QtCore import QModelIndex, QRect, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem

from tsl.style import get_color
from tsl.widgets.custom_icon_engine import PixmapStore


class StyledCheckboxDelegate(QStyledItemDelegate):
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

        # Calculate a simple rect for the checkbox that is the max size square
        # from the rectangle we paint in.
        checkbox_rect = QRect(option.rect)
        # width == height
        checkbox_rect.setWidth(checkbox_rect.height())

        # Paint icon depending on CheckState.
        if index.data(Qt.CheckStateRole) == Qt.Checked:
            icon_path = ":/svg_icons/checkbox_checked.svg"

        elif index.data(Qt.CheckStateRole) == Qt.PartiallyChecked:
            icon_path = ":/svg_icons/checkbox_indeterminate.svg"

        else:
            icon_path = ":/svg_icons/checkbox_unchecked.svg"

        store = PixmapStore.inst()
        painter.drawPixmap(
            checkbox_rect,
            store.get_pixmap(
                icon_path,
                checkbox_rect.width(),
                checkbox_rect.height(),
                get_color("foreground"),
            ),
        )
        checkbox_text = index.data()

        counter = 1
        while (
            option.rect.width() - option.rect.height()
        ) < painter.fontMetrics().width(checkbox_text):
            checkbox_text = checkbox_text[:-counter]
            counter += 1
            if len(checkbox_text) == 0:
                break

        if checkbox_text < index.data() and len(checkbox_text) != 0:
            checkbox_text += "..."

        # Calculate a rect for the text.
        text_rect = QRect(
            option.rect.x() + option.rect.height(),
            option.rect.y(),
            option.rect.width()
            - option.rect.height()
            + painter.fontMetrics().width(checkbox_text),
            option.rect.height(),
        )

        # Draw the text
        painter.drawText(
            text_rect, Qt.AlignLeft | Qt.AlignVCenter, checkbox_text
        )

        # Restore the original painter.
        painter.restore()
