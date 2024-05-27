"""Top bar with system buttons and extra menu."""

import logging
from typing import cast

from PySide6.QtCore import QEvent, QObject, QPoint, Qt, Signal, Slot
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy, QWidget

from qute_style.widgets.base_widgets import BaseWidget
from qute_style.widgets.icon import Icon
from qute_style.widgets.title_button import TitleButton

log = logging.getLogger(
    f"qute_style.{__name__}"
)  # pylint: disable=invalid-name


class TitleBar(QFrame):
    """Top bar with system buttons and extra menu."""

    right_button_clicked = Signal(type, name="right_button_clicked")
    close_app = Signal(name="close_app")
    minimize = Signal(name="minimize")
    maximize = Signal(name="maximize")
    move_window = Signal(QPoint, name="move")

    def __init__(  # noqa: PLR0913
        self,
        parent: QWidget,
        app_parent: QWidget,
        right_widget_classes: list[type[BaseWidget]],
        name: str,
        logo: str,
        debug_text: str = "",
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
        self._icon.setSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum
        )
        bg_layout.addWidget(self._icon)

        # Label with the application title text.
        self._title_label = QLabel()
        self._title_label.setObjectName("title_label")
        self._title_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self._title_label.setText(name)
        bg_layout.addWidget(self._title_label)

        # eventFilter is used to enable
        # moving + min/maximizing of the app itself.
        self._icon.installEventFilter(self)
        self._title_label.installEventFilter(self)

        # set debug label if any
        debug_label = QLabel(debug_text)
        debug_label.setObjectName("db_label")
        debug_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        debug_label.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        bg_layout.addWidget(debug_label)

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

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:  # noqa: N802
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
        if event.type() == QEvent.Type.MouseButtonRelease:
            self._double_click_in_progress = False
            return True
        if event.type() == QEvent.Type.MouseButtonDblClick:
            self._double_click_in_progress = True
            self.maximize.emit()
            return True
        if event.type() == QEvent.Type.MouseMove:
            if not self._double_click_in_progress:
                self.move_window.emit(
                    cast(QMouseEvent, event).globalPosition().toPoint()
                )
            return True
        return False

    def set_maximized(self, maximized: bool) -> None:
        """Set the _background icon depending if the app is maximized."""
        name = "fullscreen_exit" if maximized else "fullscreen"
        self.maximize_button.set_icon(f":/svg_icons/{name}.svg")
        if maximized:
            self.maximize_button.tooltip_text = self.tr("Verkleinern")
        else:
            self.maximize_button.tooltip_text = self.tr("Maximieren")

    @Slot(name="on_right_column_button")
    def on_right_column_button(self) -> None:
        """Handle a click on one of the buttons for left column widgets."""
        widget_class = cast(TitleButton, self.sender()).widget_class
        log.debug("Emitting right_button_clicked for class %s", widget_class)
        self.right_button_clicked.emit(widget_class)

    def set_button_active(
        self,
        widget_class: type[BaseWidget],
        active: bool,
    ) -> None:
        """Set the button for the given widget active/inactive."""
        button = self._button(widget_class)
        button.set_active(active)

    def _button(self, widget_class: type[BaseWidget]) -> TitleButton:
        """Return the button for the given widget class."""
        for btn in self.findChildren(TitleButton):
            if btn.widget_class == widget_class:
                return cast(TitleButton, btn)
        raise ValueError(  # pragma: no cover
            f"Could not find button for widget: {widget_class}"
        )
