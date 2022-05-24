"""Create a custom treeview with a styled expand/unfold arrow."""
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QTreeView
from qute_style.style import get_color
from qute_style.widgets.custom_icon_engine import PixmapStore


class CustomTreeView(QTreeView):
    """Create custom treeview."""

    def drawBranches(  # pylint: disable=invalid-name
        self, painter: QPainter, rect: QtCore.QRect, index: QtCore.QModelIndex
    ) -> None:
        """Draw a unfold/expand arrow."""

        if index.model().hasChildren(index):
            if self.isExpanded(index):
                arrow = PixmapStore.inst().get_pixmap(
                    ":/svg_icons/chevron_down.svg",
                    16,
                    16,
                    get_color("foreground"),
                )
            else:
                arrow = PixmapStore.inst().get_pixmap(
                    ":/svg_icons/chevron_right.svg",
                    16,
                    16,
                    get_color("foreground"),
                )

            rect_x = int(rect.x() + rect.width() / 3)
            # The arrows must be moved depending on the tree depth of the item
            counter = 3
            root_index = index
            while root_index.parent().isValid():
                rect_x = int(rect.x() + rect.width() - rect.width() / counter)
                root_index = root_index.parent()
                counter += 1

            painter.drawPixmap(
                rect_x,
                int(rect.y() + rect.height() / 5),
                arrow,
            )
