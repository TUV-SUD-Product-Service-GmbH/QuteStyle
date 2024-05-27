"""Custom widgets for grips to resize the application."""

import logging
from typing import TYPE_CHECKING

from PySide6.QtCore import QRect, Qt, Signal
from PySide6.QtGui import QCursor, QMouseEvent
from PySide6.QtWidgets import QSizeGrip, QWidget

log = logging.getLogger(
    f"qute_style.{__name__}"
)  # pylint: disable=invalid-name


class CornerGrip(QSizeGrip):
    """Widget that shows a grip handle in a corner."""

    window_geometry_changed = Signal(QRect, name="window_geometry_changed")

    def __init__(self, parent: QWidget, position: Qt.Corner) -> None:
        """Create a new CornerGrip."""
        super().__init__(parent)
        self._position = position
        self.setObjectName("grip")
        self.setFixedSize(15, 15)

    if TYPE_CHECKING:

        def parent(self) -> QWidget:
            """Override base class method for correct type hint."""

    def adapt(self) -> None:
        """Adapt the position when the main window was resized."""
        if self._position == Qt.Corner.TopLeftCorner:
            self.move(5, 5)
        elif self._position == Qt.Corner.TopRightCorner:
            self.move(self.parent().width() - 20, 5)
        elif self._position == Qt.Corner.BottomLeftCorner:
            self.move(5, self.parent().height() - 20)
        elif self._position == Qt.Corner.BottomRightCorner:
            self.move(self.parent().width() - 20, self.parent().height() - 20)

    def mousePressEvent(self, _: QMouseEvent) -> None:  # noqa: N802
        """
        Override the mousePressEvent.

        This is required to be overriden in this class
        otherwise the mouse move event is
        not working.
        """
        log.debug("Mouse press event")

    def mouseMoveEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        """
        Handle a mouse move event to resize the grip.

        The mouseMoveEvent method is only called after a mousePressEvent call.
        """
        self._resize_x_y(event.pos().x(), event.pos().y())
        super().mouseMoveEvent(event)

    def _resize_x_y(self, delta_x: int, delta_y: int) -> None:
        """
        Resize the parents geometry and by this reposition the grips.

        By doing the resize here flickering is avoided which comes with setting
        of Qt.WA_TranslucentBackground.
        """
        geo = self.parent().geometry()
        if self._position == Qt.Corner.TopLeftCorner:
            width = max(
                self.parent().minimumWidth(), self.parent().width() - delta_x
            )
            height = max(
                self.parent().minimumHeight(),
                self.parent().height() - delta_y,
            )
            geo.setLeft(geo.right() - width)
            geo.setTop(geo.bottom() - height)
        elif self._position == Qt.Corner.BottomLeftCorner:
            width = max(
                self.parent().minimumWidth(), self.parent().width() - delta_x
            )
            height = max(
                self.parent().minimumHeight(),
                self.parent().height() + delta_y,
            )
            geo.setLeft(geo.right() - width)
            geo.setHeight(height)
        elif self._position == Qt.Corner.TopRightCorner:
            width = max(
                self.parent().minimumWidth(), self.parent().width() + delta_x
            )
            height = max(
                self.parent().minimumHeight(),
                self.parent().height() - delta_y,
            )
            geo.setTop(geo.bottom() - height)
            geo.setWidth(width)
        elif self._position == Qt.Corner.BottomRightCorner:
            width = max(
                self.parent().minimumWidth(), self.parent().width() + delta_x
            )
            height = max(
                self.parent().minimumHeight(),
                self.parent().height() + delta_y,
            )
            geo.setHeight(height)
            geo.setWidth(width)
        self.window_geometry_changed.emit(geo)


class EdgeGrip(QWidget):
    """Widget that shows a grip handle in an edge."""

    window_geometry_changed = Signal(QRect, name="window_geometry_changed")

    def __init__(self, parent: QWidget, position: Qt.Edge) -> None:
        """Create a new EdgeGrip."""
        super().__init__(parent)
        self.installEventFilter(self.parent())
        self._position = position
        self.setObjectName("grip")
        if position in (Qt.Edge.TopEdge, Qt.Edge.BottomEdge):
            self.setCursor(QCursor(Qt.CursorShape.SizeVerCursor))
            self.setMaximumHeight(10)
        elif position in (Qt.Edge.LeftEdge, Qt.Edge.RightEdge):
            self.setCursor(QCursor(Qt.CursorShape.SizeHorCursor))
            self.setMaximumWidth(10)

    if TYPE_CHECKING:

        def parent(self) -> QWidget:
            """Override base class method for correct type hint."""

    def adapt(self) -> None:
        """Adapt the size and position when the main window was resized."""
        width = self.parent().width()
        height = self.parent().height()
        if self._position == Qt.Edge.TopEdge:
            self.setGeometry(5, 5, width, 10)
        elif self._position == Qt.Edge.BottomEdge:
            self.setGeometry(5, height - 15, width, 10)
        elif self._position == Qt.Edge.LeftEdge:
            self.setGeometry(5, 10, 10, height)
        elif self._position == Qt.Edge.RightEdge:
            self.setGeometry(width - 15, 10, 10, height)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        """
        Handle a mouse move event to resize the grip.

        The mouseMoveEvent method is only called after a mousePressEvent call.
        """
        if self._position in (Qt.Edge.TopEdge, Qt.Edge.BottomEdge):
            self._resize_y(event.pos().y())
        if self._position in (Qt.Edge.LeftEdge, Qt.Edge.RightEdge):
            self._resize_x(event.pos().x())
        event.accept()

    def _resize_x(self, delta_x: int) -> None:
        """Resize the grip in x-direction."""
        geo = self.parent().geometry()
        if self._position == Qt.Edge.LeftEdge:
            width = max(self.parent().minimumWidth(), geo.width() - delta_x)
            geo.setLeft(geo.right() - width)
        elif self._position == Qt.Edge.RightEdge:
            width = max(
                self.parent().minimumWidth(), self.parent().width() + delta_x
            )
            geo.setWidth(width)
        self.window_geometry_changed.emit(geo)

    def _resize_y(self, delta_y: int) -> None:
        """Resize the grip in y-direction."""
        geo = self.parent().geometry()
        if self._position == Qt.Edge.TopEdge:
            height = max(
                self.parent().minimumHeight(),
                geo.height() - delta_y,
            )
            geo.setTop(geo.bottom() - height)
        elif self._position == Qt.Edge.BottomEdge:
            height = max(
                self.parent().minimumHeight(),
                self.parent().height() + delta_y,
            )
            geo.setHeight(height)
        self.window_geometry_changed.emit(geo)
