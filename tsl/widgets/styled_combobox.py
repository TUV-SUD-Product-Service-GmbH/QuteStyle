"""Combobox that displays a list of items to be checked."""
from __future__ import annotations

import logging
from typing import Generic, List, Tuple, TypeVar, cast

from PyQt5 import QtGui
from PyQt5.QtCore import QEvent, QModelIndex, QObject, QPoint, Qt, pyqtSlot
from PyQt5.QtGui import (
    QFontMetrics,
    QMouseEvent,
    QPainter,
    QResizeEvent,
    QStandardItem,
    QStandardItemModel,
)
from PyQt5.QtWidgets import (
    QComboBox,
    QListView,
    QStyle,
    QStyleOptionComboBox,
    QWidget,
)

from tsl.style import get_color
from tsl.widgets.custom_icon_engine import PixmapStore

log = logging.getLogger(f"tsl.{__name__}")  # pylint: disable=invalid-name

ItemData = TypeVar("ItemData")


class TooManyItemsError(Exception):
    """Raised when more than one item shall be checked in single mode."""


class StyledComboBox(QComboBox):
    """Combobox with custom arrow drawing."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a new StyledComboBox."""
        super().__init__(parent)
        # options below are needed, otherwise the rounded
        # corners of dropdowns cannot be drawn correctly
        self.view().window().setWindowFlags(Qt.Popup | Qt.FramelessWindowHint)
        self.view().window().setAttribute(Qt.WA_TranslucentBackground)

    def paintEvent(  # pylint: disable=invalid-name
        self, event: QtGui.QPaintEvent
    ) -> None:
        """Overwrite method to draw custom arrow."""
        # Draw ComboBox like defined in style sheet
        super().paintEvent(event)

        # Paint custom arrow above ComboBox
        painter = QPainter()
        painter.begin(self)

        # Set correct color
        if self.isEnabled():
            color = get_color("foreground")
        else:
            color = get_color("fg_disabled")

        # Define size of arrow depending on ComboBox SubControl
        opt = QStyleOptionComboBox()
        rect = self.style().subControlRect(
            QStyle.CC_ComboBox, opt, QStyle.SC_ComboBoxArrow
        )
        radius = int(rect.width() * 0.5)

        # Get correct scale and pixmap
        scale = int(painter.device().devicePixelRatio())
        pixmap = PixmapStore.inst().get_pixmap(
            ":/svg_icons/expand_more.svg",
            radius * scale,
            radius * scale,
            color,
        )
        # Draw arrow above existing ComboBox
        painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
        # Draw arrow in rect 25x25 at the end, with size: radius x radius
        # x-axis: in the middle of arrow rect with spacing 2
        # y-axis: in the middle of arrow rect
        painter.drawPixmap(
            int(self.width() - 0.5 * (4 + rect.width() + radius)),
            int(0.5 * (self.height() - radius)),
            radius,
            radius,
            pixmap,
        )
        painter.end()


class CheckableComboBox(StyledComboBox, Generic[ItemData]):
    """Combobox that displays a list of items to be checked."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a new BatchCombobox."""
        super().__init__(parent)

        # default text that is shown when nothing is selected
        self._default_text = self.tr("Keine Auswahl")

        # sets the single mode so that only one class can be selected.
        self._single = False

        # Make the combo editable to set a custom text, but readonly
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)

        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.handle_data_change)

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.popup_open = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

        # add some spacing between the items
        cast(QListView, self.view()).setSpacing(2)

    @property
    def single_mode(self) -> bool:
        """Return if only one item can be checked at a time (single mode)."""
        return self._single

    @single_mode.setter
    def single_mode(self, single_mode: bool) -> None:
        """Set the single mode."""
        log.debug("Setting single mode to %s", single_mode)
        self._single = single_mode

    def resizeEvent(  # pylint: disable=invalid-name
        self, event: QResizeEvent
    ) -> None:
        """Recompute text when CheckableCombobox is resized."""
        super().resizeEvent(event)
        self.update_text()

    def eventFilter(  # pylint: disable=invalid-name
        self, obj: QObject, event: QEvent
    ) -> bool:
        """Filter events to show popup and set check states."""
        if event.type() == QEvent.MouseButtonRelease:
            event = cast(QMouseEvent, event)
            if obj is self.lineEdit():
                log.debug(
                    "User clicked on line edit, popup is open: %s",
                    self.popup_open,
                )
                if self.popup_open:
                    # popup is closed automatically on click on Combobox
                    # we just need to set the correct state
                    self.popup_open = False
                else:
                    self.showPopup()
                    self.popup_open = True
                return True

            if obj is self.view().viewport():
                try:
                    self._check_item_at_pos(event.pos())
                    return True
                except AttributeError:
                    # happens when the user clicks between two items
                    pass
        return False

    def hidePopup(self) -> None:  # pylint: disable=invalid-name
        """Set the state correctly when the popup is hidden from outside."""
        log.debug("Hiding popup")
        self.popup_open = False
        super().hidePopup()

    def _check_item_at_pos(self, pos: QPoint) -> None:
        """Toggle the CheckState at the given pos."""
        index = self.view().indexAt(pos)
        item = cast(QStandardItemModel, self.model()).item(index.row())
        if item.checkState() == Qt.Checked:
            item.setCheckState(Qt.Unchecked)
        else:
            item.setCheckState(Qt.Checked)

    @pyqtSlot(
        QModelIndex, QModelIndex, "QVector<int>", name="handle_data_change"
    )
    def handle_data_change(
        self, start: QModelIndex, end: QModelIndex, roles: Tuple[int]
    ) -> None:
        """Handle a data change event to handle single_mode."""
        if (
            self._single
            and Qt.CheckStateRole in roles
            and start.data(Qt.CheckStateRole) == Qt.Checked
        ):
            log.debug("Unchecking other items, since single mode is active.")
            # we should never edit check state for two indexes at the same time
            assert start == end
            for idx in range(self.model().rowCount()):
                if idx != start.row():
                    index = self.model().index(idx, 0, QModelIndex())
                    self.model().setData(
                        index, Qt.Unchecked, Qt.CheckStateRole
                    )
        self.update_text()

    def update_text(self) -> None:
        """Update the texts."""
        text = self._get_text()

        # Compute elided text (with "...")
        metrics = QFontMetrics(self.lineEdit().font())
        elided_text = metrics.elidedText(
            text, Qt.ElideRight, self.lineEdit().width()
        )
        self.lineEdit().setText(elided_text)

    def _get_text(self) -> str:
        """Return the text that is shown at the top of the combobox."""
        texts = [
            str(cast(QStandardItemModel, self.model()).item(idx).data())
            for idx in range(self.model().rowCount())
            if cast(QStandardItemModel, self.model()).item(idx).checkState()
            == Qt.Checked
        ]

        text = ", ".join(texts)
        # set to no index otherwise the state icon is displayed from
        # the first item in the combo box text which is selected by default
        self.setCurrentIndex(-1)
        if not text:
            text = self._default_text
        return text

    def addItem(  # type: ignore  # pylint: disable=invalid-name
        self,
        text: str,
        data: ItemData | None = None,
        icon_path: str | None = None,
        icon_color: str | None = None,
    ) -> None:
        """Add an Item to the Combobox."""
        item = QStandardItem(text)
        item.setData(data)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        item.setData(icon_path, Qt.DecorationRole)
        item.setData(icon_color, Qt.ForegroundRole)
        cast(QStandardItemModel, self.model()).appendRow(item)
        self.update_text()

    @property
    def item_ids(self) -> List[ItemData]:
        """Return the list of ids checked by the user."""
        return [
            cast(QStandardItemModel, self.model()).item(i).data()
            for i in range(self.model().rowCount())
            if cast(QStandardItemModel, self.model()).item(i).checkState()
            == Qt.Checked
        ]

    @item_ids.setter
    def item_ids(self, item_ids: List[ItemData]) -> None:
        """Set the ids that are selected/checked."""
        if self.single_mode and len(item_ids) > 1:
            raise TooManyItemsError(
                "Passed list contains more than one "
                "item for single mode checkbox."
            )
        log.debug("Setting item_ids: %s", item_ids)
        for idx in range(self.model().rowCount()):
            data = cast(QStandardItemModel, self.model()).item(idx).data()
            cast(QStandardItemModel, self.model()).item(idx).setCheckState(
                Qt.Checked if data in item_ids else Qt.Unchecked
            )
