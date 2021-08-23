"""Left Menu containing the widget selection."""
import logging
from typing import Iterable, List, Type, TypedDict, Union, cast

from PyQt5.QtCore import (
    QEasingCurve,
    QPropertyAnimation,
    Qt,
    pyqtSignal,
    pyqtSlot,
)
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QWidget

from tsl.widgets.base_widgets import ColumnBaseWidget, MainWidget
from tsl.widgets.div import Div
from tsl.widgets.left_menu_button import LeftMenuButton

log = logging.getLogger(f"tsl.{__name__}")  # pylint: disable=invalid-name


class LeftMenuItem(TypedDict):
    """LeftMenuItem configuration that creates an entry in the menu."""

    btn_icon: str
    btn_id: str
    btn_text: str
    btn_tooltip: str
    show_top: bool
    is_active: bool


class LeftMenu(QWidget):
    """Left menu that implements the widget selection."""

    top_button_clicked = pyqtSignal(type, name="top_button_clicked")
    bottom_button_clicked = pyqtSignal(type, name="bottom_button_clicked")

    ICON_PATH_OPEN = ":/svg_icons/icon_menu.svg"
    ICON_PATH_CLOSE = ":/svg_icons/icon_menu_close.svg"

    def __init__(
        self,
        parent: QWidget,
        app_parent: QWidget,
        main_widgets: List[Type[MainWidget]],
        left_column_widgets: List[Type[ColumnBaseWidget]],
    ) -> None:
        """Create a new LeftMenu."""
        super().__init__()

        self._app_parent = app_parent

        left_menu_layout = QVBoxLayout(self)
        left_menu_layout.setContentsMargins(0, 0, 0, 0)

        background = QFrame()
        background.setObjectName("menu_background")
        left_menu_layout.addWidget(background)

        layout = QVBoxLayout(background)
        layout.setContentsMargins(0, 0, 0, 0)

        top_frame = QFrame()
        self._top_layout = QVBoxLayout(top_frame)
        self._top_layout.setContentsMargins(0, 0, 0, 0)
        self._top_layout.setSpacing(1)
        layout.addWidget(top_frame, 0, Qt.AlignTop)

        self._toggle_button = LeftMenuButton(
            app_parent,
            text=self.tr("Menü ausblenden"),
            tooltip_text=self.tr("Menü einblenden"),
            icon_path=LeftMenu.ICON_PATH_OPEN,
            widget_class=None,
        )
        self._toggle_button.clicked.connect(self.toggle_animation)
        self._top_layout.addWidget(self._toggle_button)

        self._top_layout.addWidget(Div())

        bottom_frame = QFrame()
        self._bottom_layout = QVBoxLayout(bottom_frame)
        self._bottom_layout.setContentsMargins(0, 0, 0, 8)
        self._bottom_layout.setSpacing(1)
        layout.addWidget(bottom_frame, 0, Qt.AlignBottom)

        self._bottom_layout.addWidget(Div())
        self._add_main_widgets(main_widgets)
        self._add_bottom_widgets(left_column_widgets)

        self._animation = QPropertyAnimation(parent, b"minimumWidth")

    def _add_main_widgets(self, widgets: Iterable[Type[MainWidget]]) -> None:
        """Create the widgets and add them to the main area."""
        for widget_class in widgets:
            button = LeftMenuButton(
                self._app_parent,
                text=widget_class.NAME,
                tooltip_text=widget_class.NAME,
                icon_path=widget_class.ICON,
                widget_class=widget_class,
            )
            button.clicked.connect(self.on_main_page_button)
            self._top_layout.addWidget(button)

    def _add_bottom_widgets(
        self, widgets: Iterable[Type[ColumnBaseWidget]]
    ) -> None:
        """Create the widgets and add them to the column."""
        for widget_class in widgets:
            button = LeftMenuButton(
                self._app_parent,
                text=widget_class.NAME,
                tooltip_text=widget_class.NAME,
                icon_path=widget_class.ICON,
                widget_class=widget_class,
            )
            button.clicked.connect(self.on_left_column_button)
            self._bottom_layout.addWidget(button)

    @pyqtSlot(name="on_left_column_button")
    def on_left_column_button(self) -> None:
        """Handle a click on one of the buttons for left column widgets."""
        widget_class = cast(LeftMenuButton, self.sender()).widget_class
        log.debug("Emitting bottom_button_clicked for class %s", widget_class)
        self.bottom_button_clicked.emit(widget_class)

    @pyqtSlot(name="on_main_page_button")
    def on_main_page_button(self) -> None:
        """Handle a click on one of the buttons for left column widgets."""
        widget_class = cast(LeftMenuButton, self.sender()).widget_class
        log.debug("Emitting bottom_button_clicked for class %s", widget_class)
        self.top_button_clicked.emit(widget_class)

    @pyqtSlot(name="toggle_animation")
    def toggle_animation(self) -> None:
        """Toggle the animation (closing/opening the menu)."""
        self._animation.stop()
        self._animation.setStartValue(self.width())
        closed = self.width() == 50
        self._animation.setEndValue(240 if closed else 50)
        self._toggle_button.set_active_toggle(not closed)
        icon = LeftMenu.ICON_PATH_CLOSE if closed else LeftMenu.ICON_PATH_OPEN
        self._toggle_button.set_icon(icon)
        self._animation.setEasingCurve(QEasingCurve.InOutCubic)
        self._animation.setDuration(500)
        self._animation.start()

    def set_button_active(
        self,
        widget_class: Union[Type[ColumnBaseWidget], Type[MainWidget]],
        active: bool,
    ) -> None:
        """Set the button for the given widget active/inactive."""
        for btn in self.findChildren(LeftMenuButton):
            if btn.widget_class == widget_class:
                btn.set_active(active)
                btn.set_active_tab(active)
                return
        raise ValueError(f"Could not find button for widget: {widget_class}")
