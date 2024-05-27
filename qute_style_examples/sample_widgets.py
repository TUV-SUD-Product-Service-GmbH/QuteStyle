"""Sample widgets."""

from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from PySide6.QtCore import (
    QEvent,
    QFileInfo,
    QModelIndex,
    QObject,
    QSize,
    QStringListModel,
    Qt,
    Slot,
)
from PySide6.QtGui import QDragEnterEvent, QDropEvent, QIcon
from PySide6.QtWidgets import (
    QCheckBox,
    QDialogButtonBox,
    QFileIconProvider,
    QHBoxLayout,
    QLabel,
    QListView,
    QMenu,
    QSizePolicy,
    QSpacerItem,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
    QWidgetAction,
)

from qute_style.gen.ui_test_window import Ui_test_widget
from qute_style.helper import create_tooltip, create_waiting_spinner
from qute_style.widgets.base_widgets import MainWidget
from qute_style.widgets.custom_icon_engine import CustomIconEngine
from qute_style.widgets.drop_label import DropLabel


class TestWidget(MainWidget):
    """Test Widget."""

    ICON = ":/svg_icons/heart_broken.svg"
    NAME = "Test-Widget"

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a new TestWidget."""
        super().__init__(parent)
        self._ui = Ui_test_widget()
        self._ui.setupUi(self)
        heart_path = ":/svg_icons/heart_broken.svg"
        icon = QIcon(CustomIconEngine(heart_path, "foreground"))
        self._ui.custom_icon_engine_checkbox.setIcon(icon)
        self._ui.custom_icon_engine_checkbox.setIconSize(QSize(16, 16))
        self._ui.icon_checkbox.setIcon(QIcon(heart_path))
        self._ui.icon_checkbox.setIconSize(QSize(16, 16))
        menu = QMenu(self._ui.pushButton_2)
        all_checkbox = QCheckBox(self.tr("Select everything"))
        widget_action = QWidgetAction(menu)
        widget_action.setDefaultWidget(all_checkbox)
        menu.addAction(widget_action)
        menu.addSeparator()
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel,
            Qt.Orientation.Horizontal,
            menu,
        )
        buttons.setCenterButtons(True)
        widget_action = QWidgetAction(menu)
        widget_action.setDefaultWidget(buttons)
        menu.addAction(widget_action)
        self._ui.disable_widgets.clicked.connect(self.on_widgets_disabled)
        self._ui.transparent_combobox.setProperty("cssClass", "transparent")
        self._ui.pushButton_2.setMenu(menu)
        self._ui.pushButton_2.setIcon(icon)
        self._ui.pushButton_4.set_icon(":/svg_icons/accept.svg")
        self._ui.splitter_button.setText("Change orientation")
        self._ui.splitter_button.clicked.connect(self.on_change_orientation)
        self._ui.horizontalSlider.valueChanged.connect(
            self._ui.progressBar.setValue
        )

        text = self.tr("Drop some files.")
        self._drop_label = DropLabel(text, self._ui.drop_widget)
        self._ui.drop_widget.installEventFilter(self)
        self._ui.clear_drop_button.clicked.connect(self.on_clear_drop)

        title = self.tr("Hello there")
        text = self.tr("This might be quite useful.")
        for child in self.children():
            if hasattr(cast(QWidget, child), "toolTip"):
                cast(QWidget, child).setToolTip(create_tooltip(title, text))

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:  # noqa: N802
        """Filter and handle QDragEnterEvents and QDropEvents."""
        if event.type() == QEvent.Type.Drop and obj is self._ui.drop_widget:
            self._handle_file_drop(cast(QDropEvent, event))
            return True
        if (
            event.type() == QEvent.Type.DragEnter
            and cast(QDragEnterEvent, event).mimeData().hasUrls()
        ):
            return self._handle_drag_event(cast(QDragEnterEvent, event), obj)
        return False

    def _handle_drag_event(self, event: QDragEnterEvent, obj: QObject) -> bool:
        """Handle a QDragEnterEvent."""
        if obj is self._ui.drop_widget:
            event.acceptProposedAction()
            return True
        return False  # pragma: no cover

    def _handle_file_drop(self, event: QDropEvent) -> None:
        """Handle a QDropEvent on the list of files."""
        files = event.mimeData().urls()
        for file in files:
            path = Path(file.toLocalFile())
            if path.is_dir():
                return
            self._add_file(path)

    def _add_file(self, path: Path) -> None:
        """Add a file to the list of files."""
        self._drop_label.hide()

        # Create a QTreeWidgetItem that displays the filename only.
        item = QTreeWidgetItem(self._ui.drop_widget, [path.name])
        item.setData(0, Qt.ItemDataRole.UserRole, path)

        # Get a QIcon for the file from OS and set it.
        item.setIcon(0, QFileIconProvider().icon(QFileInfo(str(path))))

    def on_clear_drop(self) -> None:
        """Remove all items from DropArea."""
        self._ui.drop_widget.clear()
        self._drop_label.show()

    @Slot(name="on_change_orientation")
    def on_change_orientation(self) -> None:
        """Change the orientation of the QSplitter."""
        if self._ui.splitter.orientation() == Qt.Orientation.Horizontal:
            self._ui.splitter.setOrientation(Qt.Orientation.Vertical)
        else:
            self._ui.splitter.setOrientation(Qt.Orientation.Horizontal)

    @Slot(name="on_widgets_disabled")
    def on_widgets_disabled(self) -> None:
        """Disable all widgets."""
        if self._ui.disable_widgets.isChecked():
            for child in self.children():
                if child.objectName() != "disable_widgets":
                    cast(QWidget, child).setEnabled(False)
        else:
            for child in self.children():
                cast(QWidget, child).setEnabled(True)


class Model(QStringListModel):
    """Test model with check states."""

    def __init__(self, data: list[str], parent: QObject | None = None) -> None:
        """Create a new Model."""
        self._check_states: dict[str, Qt.CheckState] = {}
        super().__init__(data, parent)

    def data(  # type: ignore[override]
        self,
        index: QModelIndex,
        role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole,
    ) -> Any:
        """Return data for the given role and index."""
        if role == Qt.ItemDataRole.CheckStateRole:
            return self._check_states[index.data()]
        return super().data(index, role)

    def setData(  # type: ignore # noqa: N802
        self,
        index: QModelIndex,
        value: Qt.CheckState,
        role: int = Qt.ItemDataRole.EditRole,
    ) -> bool:
        # pylint: enable=invalid-name
        """Set data for the given role and index."""
        if role == Qt.ItemDataRole.CheckStateRole:
            self._check_states[index.data()] = value
            self.dataChanged.emit(
                index, index, [Qt.ItemDataRole.CheckStateRole]
            )
        return super().setData(index, value, role)

    def flags(self, _: QModelIndex) -> Qt.ItemFlag:  # type: ignore[override]
        """Return the flags for the given index."""
        return (
            Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsUserCheckable
            | Qt.ItemFlag.ItemIsSelectable
        )


class ModelViewWidget(MainWidget):
    """Test Widget for Model View tests."""

    ICON = ":/svg_icons/heart_broken.svg"
    NAME = "Test-Widget"

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a new TestWidget."""
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self._view = QListView()
        self._settings_widget: None | QWidget = None
        layout.addWidget(self._view)
        model = Model(["Item1", "Item2", "Item3\nwith line break"])

        for row in range(model.rowCount()):
            index = model.index(row)
            model.setData(
                index,
                (
                    Qt.CheckState.Checked
                    if row % 2
                    else Qt.CheckState.Unchecked
                ),  # alternate value
                Qt.ItemDataRole.CheckStateRole,
            )
        self._view.setModel(model)

    @property
    def settings_widget(self) -> QWidget:
        """Return ModelViewWidget specific settings."""
        if not self._settings_widget:
            self._settings_widget = QWidget()
            QVBoxLayout(self._settings_widget)
            self._settings_widget.layout().addWidget(
                QLabel(f"Settings {self.NAME}", self)
            )
            self._settings_widget.layout().addWidget(QCheckBox("Activate 1"))
            self._settings_widget.layout().addWidget(QCheckBox("Activate 2"))
            self._settings_widget.layout().addWidget(QCheckBox("Activate 2"))
            self._settings_widget.layout().addWidget(QLabel("...", self))
            self._settings_widget.layout().addItem(
                QSpacerItem(
                    0,
                    0,
                    QSizePolicy.Policy.Expanding,
                    QSizePolicy.Policy.Expanding,
                )
            )
        return self._settings_widget


class SpinnerWidget(MainWidget):
    """Test Widget for pyqtspinner."""

    ICON = ":/svg_icons/heart_broken.svg"
    NAME = "Spinner-Widget"

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a new TestWidget."""
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self._view = QListView()
        self._settings_widget: None | QWidget = None
        layout.addWidget(self._view)
        self._spinner = create_waiting_spinner(self)
        self._spinner.start()
