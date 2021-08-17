"""Custom widgets for grips to resize the application."""
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QMouseEvent
from PyQt5.QtWidgets import QSizeGrip, QWidget

log = logging.getLogger(f"tsl.{__name__}")  # pylint: disable=invalid-name


class CornerGrip(QSizeGrip):
    """Widget that shows a grip handle in a corner."""

    def __init__(self, parent: QWidget, position: Qt.Corner) -> None:
        """Create a new CornerGrip."""
        super().__init__(parent)
        self._position = position
        self.setObjectName("grip")
        self.setFixedSize(15, 15)

    def adapt(self) -> None:
        """Adapt the position when the main window was resized."""
        if self._position == Qt.TopLeftCorner:
            self.move(5, 5)
        elif self._position == Qt.TopRightCorner:
            self.move(self.parent().width() - 20, 5)
        elif self._position == Qt.BottomLeftCorner:
            self.move(5, self.parent().height() - 20)
        elif self._position == Qt.BottomRightCorner:
            self.move(self.parent().width() - 20, self.parent().height() - 20)


class EdgeGrip(QWidget):
    """Widget that shows a grip handle in an edge."""

    def __init__(self, parent: QWidget, position: Qt.Edge) -> None:
        """Create a new EdgeGrip."""
        super().__init__(parent)
        self.installEventFilter(self.parent())
        self._position = position
        self.setObjectName("grip")
        if position in (Qt.TopEdge, Qt.BottomEdge):
            self.setCursor(QCursor(Qt.SizeVerCursor))
            self.setMaximumHeight(10)
        elif position in (Qt.LeftEdge, Qt.RightEdge):
            self.setCursor(QCursor(Qt.SizeHorCursor))
            self.setMaximumWidth(10)

    def adapt(self) -> None:
        """Adapt the size and position when the main window was resized."""
        width = self.parent().width()
        height = self.parent().height()
        if self._position == Qt.TopEdge:
            self.setGeometry(5, 5, width, 10)
        elif self._position == Qt.BottomEdge:
            self.setGeometry(5, height - 15, width, 10)
        elif self._position == Qt.LeftEdge:
            self.setGeometry(5, 10, 10, height)
        elif self._position == Qt.RightEdge:
            self.setGeometry(width - 15, 10, 10, height)

    def mouseMoveEvent(  # pylint: disable=invalid-name
        self, event: QMouseEvent
    ) -> None:
        """
        Handle a mouse move event to resize the grip.

        The mouseMoveEvent method is only called after a mousePressEvent call.
        """
        if self._position in (Qt.TopEdge, Qt.BottomEdge):
            self.resize_y(event.pos().y())
        if self._position in (Qt.LeftEdge, Qt.RightEdge):
            self.resize_x(event.pos().x())
        event.accept()

    def resize_x(self, delta_x: int) -> None:
        """Resize the grip in x-direction."""
        if self._position == Qt.LeftEdge:
            width = max(
                self.parent().minimumWidth(), self.parent().width() - delta_x
            )
            geo = self.parent().geometry()
            geo.setLeft(geo.right() - width)
            self.parent().setGeometry(geo)
        elif self._position == Qt.RightEdge:
            width = max(
                self.parent().minimumWidth(), self.parent().width() + delta_x
            )
            self.parent().resize(width, self.parent().height())

    def resize_y(self, delta_y: int) -> None:
        """Resize the grip in y-direction."""
        if self._position == Qt.TopEdge:
            height = max(
                self.parent().minimumHeight(),
                self.parent().height() - delta_y,
            )
            geo = self.parent().geometry()
            geo.setTop(geo.bottom() - height)
            self.parent().setGeometry(geo)
        elif self._position == Qt.BottomEdge:
            height = max(
                self.parent().minimumHeight(),
                self.parent().height() + delta_y,
            )
            self.parent().resize(self.parent().width(), height)
