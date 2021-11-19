"""Top bar with system buttons and extra menu."""
import logging
from typing import List, Type, cast

from PyQt5.QtCore import QEvent, QObject, QPoint, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy, QWidget

from tsl.vault import Vault
from tsl.widgets.base_widgets import ColumnBaseWidget
from tsl.widgets.icon import Icon
from tsl.widgets.title_button import TitleButton

log = logging.getLogger(f"tsl.{__name__}")  # pylint: disable=invalid-name


class TitleBar(QFrame):
    """Top bar with system buttons and extra menu."""

    right_button_clicked = pyqtSignal(type, name="right_button_clicked")
    close_app = pyqtSignal(name="close_app")
    minimize = pyqtSignal(name="minimize")
    maximize = pyqtSignal(name="maximize")
    move_window = pyqtSignal(QPoint, name="move")

    def __init__(  # pylint: disable=too-many-arguments
        self,
        parent: QWidget,
        app_parent: QWidget,
        right_widget_classes: List[Type[ColumnBaseWidget]],
        name: str,
        logo: str,
    ) -> None:
        """Create a new TitleBar."""
        super().__init__(parent)
        self.setObjectName("bg_two_frame")

        # Fix the height of the TitleBar to 40 pixels.
        self.setFixedHeight(40)

        bg_layout = QHBoxLayout(self)
        bg_layout.setContentsMargins(10, 0, 5, 0)
        bg_layout.setSpacing(0)

        # Icon with ToolBox logo
        self._icon = Icon(int(self.height() * 0.5), None)
        self._icon.set_icon(logo)
        self._icon.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self._icon.setAlignment(Qt.AlignVCenter)
        bg_layout.addWidget(self._icon)

        # Label with the application title text.
        self._title_label = QLabel()
        self._title_label.setObjectName("title_label")
        self._title_label.setAlignment(Qt.AlignVCenter)
        self._title_label.setText(name)
        bg_layout.addWidget(self._title_label)

        # eventFilter is used to enable
        # moving + min/maximizing of the app itself.
        self._icon.installEventFilter(self)
        self._title_label.installEventFilter(self)

        # Label to inform developer and tester that the cps test database
        # is used
        envs = Vault.CREATED_DATABASES
        log.debug("Envs used: %s", envs)
        if any(env != Vault.Environment.PROD for env in envs.values()):
            log.debug("Usage of test databases detected: %s", envs)
            text = " | ".join(
                f"{app.name}: {env.name}" for app, env in envs.items()
            )
            db_label = QLabel(text)
            db_label.setObjectName("db_label")
            db_label.setAlignment(Qt.AlignVCenter)
            db_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            bg_layout.addWidget(db_label)

        # Button for the right column
        for widget_class in right_widget_classes:
            right_column_button = TitleButton(
                app_parent,
                tooltip_text=widget_class.NAME,
                icon_path=widget_class.ICON,
                widget_class=widget_class,
            )
            right_column_button.clicked.connect(self.on_right_column_button)
            bg_layout.addWidget(right_column_button)

        # Minimize Button
        minimize_button = TitleButton(
            app_parent,
            tooltip_text=self.tr("Minimieren"),
            icon_path=":/svg_icons/minimize.svg",
        )
        minimize_button.released.connect(self.minimize)
        bg_layout.addWidget(minimize_button)

        # Maximize Button
        self.maximize_button = TitleButton(
            app_parent,
            tooltip_text=self.tr("Maximieren"),
            icon_path=":/svg_icons/fullscreen.svg",
        )
        self.maximize_button.released.connect(self.maximize)
        bg_layout.addWidget(self.maximize_button)

        # Close Button
        close_button = TitleButton(
            app_parent,
            tooltip_text=self.tr("Schließen"),
            icon_path=":/svg_icons/close.svg",
        )
        close_button.released.connect(self.close_app)
        bg_layout.addWidget(close_button)

        self._double_click_in_progress = False

    @property
    def title_bar_text(self) -> str:
        """Get the title bar text."""
        return self._title_label.text()

    @title_bar_text.setter
    def title_bar_text(self, text: str) -> None:
        """Set the title bar text."""
        self._title_label.setText(text)

    def eventFilter(  # pylint: disable=invalid-name
        self, obj: QObject, event: QEvent
    ) -> bool:
        """
        Handle mouse events.

        MouseButtonDblClick is a combination of MousePress, MouseRelease
        and MousePress. The final Mouse Release is not part of this event.
        Thus it can happen that by executing a MouseButtonDblClick also a Mouse
        MoveEvent is executed. The introduced _double_click_in_progress
        variable blocks this situation which could lead to e.g. a maximize
        operation followed directly by a minimize operation.
        """
        if obj is not self._title_label and not self._icon:
            return False
        if event.type() == QEvent.MouseButtonRelease:
            self._double_click_in_progress = False
            return True
        if event.type() == QEvent.MouseButtonDblClick:
            self._double_click_in_progress = True
            self.maximize.emit()
            return True
        if event.type() == QEvent.MouseMove:
            if not self._double_click_in_progress:
                self.move_window.emit(cast(QMouseEvent, event).globalPos())
            return True
        return False

    def set_maximized(self, maximized: bool) -> None:
        """Set the _background icon depending if the app is maximized."""
        name = "fullscreen_exit" if maximized else "fullscreen"
        self.maximize_button.set_icon(":/svg_icons/{}.svg".format(name))
        if maximized:
            self.maximize_button.tooltip_text = self.tr("Verkleinern")
        else:
            self.maximize_button.tooltip_text = self.tr("Maximieren")

    @pyqtSlot(name="on_right_column_button")
    def on_right_column_button(self) -> None:
        """Handle a click on one of the buttons for left column widgets."""
        widget_class = cast(TitleButton, self.sender()).widget_class
        log.debug("Emitting right_button_clicked for class %s", widget_class)
        self.right_button_clicked.emit(widget_class)

    def set_button_active(
        self,
        widget_class: Type[ColumnBaseWidget],
        active: bool,
    ) -> None:
        """Set the button for the given widget active/inactive."""
        button = self._button(widget_class)
        button.set_active(active)

    def _button(self, widget_class: Type[ColumnBaseWidget]) -> TitleButton:
        """Return the button for the given widget class."""
        for btn in self.findChildren(TitleButton):
            if btn.widget_class == widget_class:
                return btn
        raise ValueError(  # pragma: no cover
            f"Could not find button for widget: {widget_class}"
        )
