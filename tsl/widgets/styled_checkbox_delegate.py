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
                get_color("text_foreground"),
            ),
        )

        # Calculate a rect for the text.
        text_rect = QRect(
            option.rect.x() + option.rect.height(),
            option.rect.y(),
            option.rect.height(),
            option.rect.width() - option.rect.height(),
        )

        # Draw the text
        painter.drawText(
            text_rect, Qt.AlignRight | Qt.AlignTop, index.data(Qt.DisplayRole)
        )

        # Restore the original painter.
        painter.restore()
