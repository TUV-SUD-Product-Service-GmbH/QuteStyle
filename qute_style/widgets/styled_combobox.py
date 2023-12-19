"""Combobox that displays a list of items to be checked."""

from __future__ import annotations

import contextlib
import logging
from typing import Generic, TypeVar, cast

from PySide6 import QtGui
from PySide6.QtCore import (
    QEvent,
    QModelIndex,
    QObject,
    QPoint,
    Qt,
    Signal,
    Slot,
)
from PySide6.QtGui import (
    QFontMetrics,
    QIcon,
    QMouseEvent,
    QPainter,
    QResizeEvent,
    QStandardItem,
    QStandardItemModel,
)
from PySide6.QtWidgets import (
    QComboBox,
    QListView,
    QStyle,
    QStyleOptionComboBox,
    QWidget,
)

from qute_style.style import get_color
from qute_style.widgets.custom_icon_engine import CustomIconEngine, PixmapStore

log = logging.getLogger(
    f"qute_style.{__name__}"
)  # pylint: disable=invalid-name

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
        self.view().window().setWindowFlags(
            Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint
        )
        self.view().window().setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )
        # stop combobox contents from limiting width of whole application
        self.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToMinimumContentsLengthWithIcon
        )

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:  # noqa: N802
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
            QStyle.ComplexControl.CC_ComboBox,
            opt,
            QStyle.SubControl.SC_ComboBoxArrow,
            None,
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
        painter.setCompositionMode(
            QPainter.CompositionMode.CompositionMode_SourceOver
        )
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

    dataChanged = Signal(dict, name="dataChanged")  # noqa: N815

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a new CheckableComboBox."""
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

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.popup_open = False

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

    def resizeEvent(self, event: QResizeEvent) -> None:  # noqa: N802
        """Recompute text when CheckableCombobox is resized."""
        super().resizeEvent(event)
        self.update_text()

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:  # noqa: N802
        """Filter events to show popup and set check states."""
        if event.type() == QEvent.Type.MouseButtonRelease:
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
                with contextlib.suppress(AttributeError):
                    self._check_item_at_pos(event.pos())
                    return True
        return False

    def hidePopup(self) -> None:  # noqa: N802
        """Set the state correctly when the popup is hidden from outside."""
        log.debug("Hiding popup")
        self.popup_open = False
        super().hidePopup()

    def _check_item_at_pos(self, pos: QPoint) -> None:
        """Toggle the CheckState at the given pos."""
        index = self.view().indexAt(pos)
        item = cast(QStandardItemModel, self.model()).item(index.row())
        if item.checkState() == Qt.CheckState.Checked:
            item.setCheckState(Qt.CheckState.Unchecked)
        else:
            item.setCheckState(Qt.CheckState.Checked)

    @Slot(
        QModelIndex,
        QModelIndex,
        "QVector<int>",  # type: ignore
        name="handle_data_change",
    )
    def handle_data_change(
        self,
        start: QModelIndex,
        end: QModelIndex,
        roles: list[Qt.ItemDataRole],
    ) -> None:
        """Handle a data change event to handle single_mode."""
        if (
            self._single
            and Qt.ItemDataRole.CheckStateRole in roles
            and Qt.CheckState(start.data(Qt.ItemDataRole.CheckStateRole))
            == Qt.CheckState.Checked
        ):
            log.debug("Unchecking other items, since single mode is active.")
            # we should never edit check state for two indexes at the same time
            assert start == end
            for idx in range(self.model().rowCount()):
                if idx != start.row():
                    index = self.model().index(idx, 0, QModelIndex())
                    self.model().setData(
                        index,
                        Qt.CheckState.Unchecked,
                        Qt.ItemDataRole.CheckStateRole,
                    )
        self.update_text()
        self.send_current_state()

    def update_text(self) -> None:
        """Update the texts."""
        text = self._get_text()

        # Compute elided text (with "...")
        metrics = QFontMetrics(self.lineEdit().font())
        elided_text = metrics.elidedText(
            text, Qt.TextElideMode.ElideRight, self.lineEdit().width()
        )
        self.lineEdit().setText(elided_text)

    def send_current_state(self) -> None:
        """Emit the current state via dataChanged."""
        current_state: dict[str | int, Qt.CheckState] = {
            self.model().item(i).data(): (self.model().item(i).checkState())
            for i in range(self.model().rowCount())
        }
        self.dataChanged.emit(current_state)

    def _get_text(self) -> str:
        """Return the text that is shown at the top of the combobox."""
        texts = [
            str(cast(QStandardItemModel, self.model()).item(idx).data())
            for idx in range(self.model().rowCount())
            if cast(QStandardItemModel, self.model()).item(idx).checkState()
            == Qt.CheckState.Checked
        ]

        text = ", ".join(texts)
        # set to no index otherwise the state icon is displayed from
        # the first item in the combo box text which is selected by default
        self.setCurrentIndex(-1)
        if not text:
            text = self._default_text
        return text

    def addItem(  # type: ignore # noqa: N802
        self,
        text: str,
        data: ItemData | None = None,
        icon_path: str | None = None,
        icon_color: str | None = None,
    ) -> None:
        """Add an Item to the Combobox."""
        if icon_color and not icon_path:
            raise AssertionError(
                "Color can only be passed together with an icon (path)"
            )
        item = QStandardItem(text)
        item.setData(data)
        item.setFlags(
            Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsUserCheckable
        )
        item.setData(Qt.CheckState.Unchecked, Qt.ItemDataRole.CheckStateRole)
        if icon_path:
            item.setData(
                QIcon(CustomIconEngine(icon_path, icon_color or "foreground")),
                Qt.ItemDataRole.DecorationRole,
            )
        cast(QStandardItemModel, self.model()).appendRow(item)
        self.update_text()

    @property
    def item_ids(self) -> list[ItemData]:
        """Return the list of ids checked by the user."""
        return [
            cast(QStandardItemModel, self.model()).item(i).data()
            for i in range(self.model().rowCount())
            if cast(QStandardItemModel, self.model()).item(i).checkState()
            == Qt.CheckState.Checked
        ]

    @item_ids.setter
    def item_ids(self, item_ids: list[ItemData]) -> None:
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
                Qt.CheckState.Checked
                if data in item_ids
                else Qt.CheckState.Unchecked
            )


class SelectAllComboBox(CheckableComboBox[str | int], Generic[ItemData]):
    """CheckableComboBox that has an entry that alters the whole selection."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a new SelectAllComboBox."""
        super().__init__(parent)
        self.addItem(self.tr("Alles auswählen"))
        self.model().item(0).setAutoTristate(True)
        self.insertSeparator(1)

    def initialize_content(self) -> None:
        """Select or deselect all items based on "select all" item."""
        self.handle_data_change(
            self.model().index(0, 0, QModelIndex()),
            self.model().index(0, 0, QModelIndex()),
            [Qt.ItemDataRole.CheckStateRole],
        )

    @Slot(
        QModelIndex,
        QModelIndex,
        "QVector<int>",  # type: ignore
        name="handle_data_change",
    )
    def handle_data_change(
        self,
        start: QModelIndex,
        end: QModelIndex,
        roles: list[Qt.ItemDataRole],
    ) -> None:
        """Handle click on "Select all"."""
        select_all_item = self.model().item(0)
        self.model().blockSignals(True)
        # handle how the select_all_item affects all other items
        if start == self.model().index(0, 0, QModelIndex()):
            if select_all_item.checkState() == Qt.CheckState.Checked:
                log.debug("Selecting all items.")
                for idx in range(2, self.model().rowCount()):
                    self.model().item(idx).setCheckState(Qt.CheckState.Checked)
            elif select_all_item.checkState() == Qt.CheckState.Unchecked:
                log.debug("Deselecting all items.")
                for idx in range(2, self.model().rowCount()):
                    self.model().item(idx).setCheckState(
                        Qt.CheckState.Unchecked
                    )
            elif (
                select_all_item.checkState() == Qt.CheckState.PartiallyChecked
            ):
                return
        # handle how all other items affect the select_all_item
        elif all(
            self.model().item(idx).checkState() == Qt.CheckState.Checked
            for idx in range(2, self.model().rowCount())
        ):
            select_all_item.setCheckState(Qt.CheckState.Checked)
        elif all(
            self.model().item(idx).checkState() == Qt.CheckState.Unchecked
            for idx in range(2, self.model().rowCount())
        ):
            select_all_item.setCheckState(Qt.CheckState.Unchecked)
        else:
            select_all_item.setCheckState(Qt.CheckState.PartiallyChecked)
        self.model().blockSignals(False)
        super().handle_data_change(
            self.model().index(2, 0, QModelIndex()), end, roles
        )

    def _get_text(self) -> str:
        """Return the text that is shown at the top of the combobox."""
        texts = [
            str(cast(QStandardItemModel, self.model()).item(idx).data())
            for idx in range(2, self.model().rowCount())
            if cast(QStandardItemModel, self.model()).item(idx).checkState()
            == Qt.CheckState.Checked
        ]

        text = ", ".join(texts)
        # set to no index otherwise the state icon is displayed from
        # the first item in the combo box text which is selected by default
        self.setCurrentIndex(-1)
        if not text:
            text = self._default_text
        return text
