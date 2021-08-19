"""Top bar with system buttons and extra menu."""
from typing import Type, cast

from PyQt5.QtCore import QEvent, QObject, QPoint, Qt, pyqtSignal
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from tsl.widgets.base_widgets import ColumnBaseWidget
from tsl.widgets.title_button import TitleButton


class TitleBar(QWidget):
    """Top bar with system buttons and extra menu."""

    right_button_clicked = pyqtSignal(name="right_button_clicked")
    close_app = pyqtSignal(name="close_app")
    minimize = pyqtSignal(name="minimize")
    maximize = pyqtSignal(name="maximize")
    move_window = pyqtSignal(QPoint, name="move")

    def __init__(
        self,
        parent: QWidget,
        app_parent: QWidget,
        right_widget_class: Type[ColumnBaseWidget],
        name: str,
    ) -> None:
        """Create a new TitleBar."""
        super().__init__(parent)

        # Fix the height of the TitleBar to 40 pixels.
        self.setFixedHeight(40)

        # Create a main layout.
        title_bar_layout = QVBoxLayout(self)
        title_bar_layout.setContentsMargins(0, 0, 0, 0)

        # Create a background QFrame and a layout for the TitleBar's elements
        # and add it to the main layout.
        title_bar_background = QFrame()
        title_bar_background.setObjectName("title_bar_background")
        title_bar_layout.addWidget(title_bar_background)
        bg_layout = QHBoxLayout(title_bar_background)
        bg_layout.setContentsMargins(10, 0, 5, 0)
        bg_layout.setSpacing(0)

        # Label with the application title text. eventFilter is used to enable
        # moving + min/maximizing of the app itself.
        self.title_label = QLabel()
        self.title_label.setObjectName("title_label")
        self.title_label.setAlignment(Qt.AlignVCenter)
        self.title_label.installEventFilter(self)
        self.title_label.setText(name)
        bg_layout.addWidget(self.title_label)

        # Button for the right column
        self._right_column_button = TitleButton(
            app_parent,
            tooltip_text=right_widget_class.NAME,
            icon_path=right_widget_class.ICON,
        )
        self._right_column_button.clicked.connect(self.right_button_clicked)
        bg_layout.addWidget(self._right_column_button)

        # Minimize Button
        minimize_button = TitleButton(
            app_parent,
            tooltip_text=self.tr("Minimieren"),
            icon_path=":/svg_icons/icon_minimize.svg",
        )
        minimize_button.released.connect(self.minimize)
        bg_layout.addWidget(minimize_button)

        # Maximize Button
        self.maximize_button = TitleButton(
            app_parent,
            tooltip_text=self.tr("Maximieren"),
            icon_path=":/svg_icons/icon_maximize.svg",
        )
        self.maximize_button.released.connect(self.maximize)
        bg_layout.addWidget(self.maximize_button)

        # Close Button
        close_button = TitleButton(
            app_parent,
            tooltip_text=self.tr("Schließen"),
            icon_path=":/svg_icons/icon_close.svg",
        )
        close_button.released.connect(self.close_app)
        bg_layout.addWidget(close_button)

    def eventFilter(  # pylint: disable=invalid-name
        self, obj: QObject, event: QEvent
    ) -> bool:
        """Handle double click events."""
        if obj is not self.title_label:
            return False
        if event.type() == QEvent.MouseButtonDblClick:
            self.maximize.emit()
            return True
        if event.type() == QEvent.MouseMove:
            self.move_window.emit(cast(QMouseEvent, event).globalPos())
            return True
        return False

    def set_maximized(self, maximized: bool) -> None:
        """Set the _background icon depending if the app is maximized."""
        name = "restore" if maximized else "maximize"
        self.maximize_button.set_icon(":/svg_icons/icon_{}.svg".format(name))

    def set_right_button_active(self, active: bool) -> None:
        """Return the button to open/close the right column."""
        self._right_column_button.set_active(active)
