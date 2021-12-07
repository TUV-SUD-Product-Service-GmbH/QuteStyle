"""Sample widgets."""
from typing import Dict, List, cast

from PyQt5.QtCore import QModelIndex, QObject, QStringListModel, Qt, pyqtSlot
from PyQt5.QtWidgets import (
    QCheckBox,
    QDialogButtonBox,
    QHBoxLayout,
    QListView,
    QMenu,
    QWidget,
    QWidgetAction,
)

from tsl.gen.ui_test_window import Ui_test_widget
from tsl.widgets.base_widgets import MainWidget
from tsl.widgets.styled_checkbox_delegate import StyledCheckboxDelegate


class TestWidget(MainWidget):
    """Test Widget."""

    ICON = ":/svg_icons/heart_broken.svg"
    NAME = "Test-Widget"
    GROUPS: List[str] = ["PS-CPS-TSL-G"]

    def __init__(self, parent: QWidget = None) -> None:
        """Create a new TestWidget."""
        super().__init__(parent)
        self._ui = Ui_test_widget()
        self._ui.setupUi(self)
        menu = QMenu(self._ui.pushButton_2)
        all_checkbox = QCheckBox(self.tr("Alles auswählen"))
        widget_action = QWidgetAction(menu)
        widget_action.setDefaultWidget(all_checkbox)
        menu.addAction(widget_action)
        menu.addSeparator()
        buttons = QDialogButtonBox(
            cast(
                QDialogButtonBox.StandardButtons,
                QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            ),
            Qt.Horizontal,
            menu,
        )
        buttons.setCenterButtons(True)
        widget_action = QWidgetAction(menu)
        widget_action.setDefaultWidget(buttons)
        menu.addAction(widget_action)
        self._ui.disable_widgets.clicked.connect(self.on_widgets_disabled)
        self._ui.comboBox_2.setProperty("cssClass", "transparent")
        self._ui.pushButton_2.setMenu(menu)
        self._ui.pushButton_4.set_icon(":/svg_icons/accept.svg")
        self._ui.splitter_button.setText("Change orientation")
        self._ui.splitter_button.clicked.connect(self.on_change_orientation)

    @pyqtSlot(name="on_change_orientation")
    def on_change_orientation(self) -> None:
        """Change the orientation of the QSplitter."""
        if self._ui.splitter.orientation() == Qt.Horizontal:
            self._ui.splitter.setOrientation(Qt.Vertical)
        else:
            self._ui.splitter.setOrientation(Qt.Horizontal)

    @pyqtSlot(name="on_widgets_disabled")
    def on_widgets_disabled(self) -> None:
        """Disable all widgets."""
        if self._ui.disable_widgets.isChecked():
            for child in self.children():
                if child.objectName() != "disable_widgets":
                    child.setEnabled(False)
        else:
            for child in self.children():
                child.setEnabled(True)


class Model(QStringListModel):
    """Test model with check states."""

    def __init__(self, data: List[str], parent: QObject = None) -> None:
        """Create a new Model."""
        self._check_states: Dict[str, Qt.CheckState] = {}
        super().__init__(data, parent)

    def data(
        self, index: QModelIndex, role: int = Qt.DisplayRole
    ) -> Qt.CheckState:
        """Return data for the given role and index."""
        if role == Qt.CheckStateRole:
            return self._check_states[index.data()]
        return super().data(index, role)  # type: ignore

    def setData(  # pylint: disable=invalid-name
        self, index: QModelIndex, value: Qt.CheckState, role: int = Qt.EditRole
    ) -> bool:
        """Set data for the given role and index."""
        if role == Qt.CheckStateRole:
            self._check_states[index.data()] = value
            self.dataChanged.emit(index, index, [Qt.CheckStateRole])
        return super().setData(index, value, role)

    def flags(  # pylint: disable=no-self-use
        self, _: QModelIndex
    ) -> Qt.ItemFlags:
        """Return the flags for the given index."""
        return cast(
            Qt.ItemFlags,
            Qt.ItemIsEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsSelectable,
        )


class ModelViewWidget(MainWidget):
    """Test Widget for Model View tests."""

    ICON = ":/svg_icons/heart_broken.svg"
    NAME = "Test-Widget"

    def __init__(self, parent: QWidget = None) -> None:
        """Create a new TestWidget."""
        super().__init__(parent)
        layout = QHBoxLayout(self)
        self._view = QListView()
        layout.addWidget(self._view)
        model = Model(["A", "B", "C"])

        for row in range(model.rowCount()):
            index = model.index(row)
            model.setData(
                index,
                Qt.Checked if row % 2 else Qt.Unchecked,  # alternate value
                Qt.CheckStateRole,
            )
        self._view.setModel(model)
        delegate = StyledCheckboxDelegate()
        self._view.setItemDelegateForColumn(0, delegate)
