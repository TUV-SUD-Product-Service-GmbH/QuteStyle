"""Left Menu containing the widget selection."""

import logging
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any, TypedDict, cast

from PySide6.QtCore import QEasingCurve, QPropertyAnimation, Qt, Signal, Slot
from PySide6.QtWidgets import (
    QFrame,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from qute_style.widgets.base_widgets import BaseWidget, MainWidget
from qute_style.widgets.div import Div
from qute_style.widgets.icon_tooltip_button import BaseWidgetType
from qute_style.widgets.left_menu_button import LeftMenuButton

log = logging.getLogger(
    f"qute_style.{__name__}"
)  # pylint: disable=invalid-name


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

    top_button_clicked = Signal(type, name="top_button_clicked")
    bottom_button_clicked = Signal(type, name="bottom_button_clicked")

    ICON_PATH_OPEN = ":/svg_icons/menu.svg"
    ICON_PATH_CLOSE = ":/svg_icons/arrow_back.svg"

    def __init__(
        self,
        parent: QWidget,
        app_parent: QWidget,
        main_widgets: list[type[MainWidget]],
        left_column_widgets: list[type[BaseWidget]],
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
        layout.addWidget(top_frame, 0, Qt.AlignmentFlag.AlignTop)

        self._toggle_button: LeftMenuButton[None] = LeftMenuButton(
            app_parent,
            text=self.tr("Menü ausblenden"),
            tooltip_text=self.tr("Menü einblenden"),
            icon_path=LeftMenu.ICON_PATH_OPEN,
            widget_class=None,
        )
        self._toggle_button.clicked.connect(self.toggle_animation)
        self._top_layout.addWidget(self._toggle_button)

        self._top_layout.addWidget(Div())

        self._setup_scroll_area(len(main_widgets))
        # Set stretch factor 1 to ensure that,
        # if enough space is available, all widgets are displayed
        layout.addWidget(self._scroll_area, 1)
        # Add stretch to ensure that scroll
        # area is aligned below the Menubutton
        layout.addStretch()

        bottom_frame = QFrame()
        self._bottom_layout = QVBoxLayout(bottom_frame)
        self._bottom_layout.setContentsMargins(0, 0, 0, 8)
        self._bottom_layout.setSpacing(1)
        layout.addWidget(bottom_frame, 0, Qt.AlignmentFlag.AlignBottom)

        self._add_main_widgets(main_widgets)
        log.debug("Handling left column widgets: %s", left_column_widgets)
        if left_column_widgets:
            self._bottom_layout.addWidget(Div())
            self._add_bottom_widgets(left_column_widgets)

        self.setMinimumWidth(50)
        self._animation = QPropertyAnimation(parent, b"minimumWidth")

    if TYPE_CHECKING:

        def parent(self) -> QWidget:
            """Override base class method for correct type hint."""

    def _add_main_widgets(self, widgets: Iterable[type[MainWidget]]) -> None:
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
            self._middle_layout.addWidget(button)

    def _setup_scroll_area(self, num_widgets: int) -> None:
        """Create the ScrollArea with correct sizePolicies and margins."""
        self._scroll_area = QScrollArea()
        # Never show a scrollbar
        self._scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self._scroll_area.setFixedWidth(self.width())

        # MaximumHeight depends on number of widgets:
        # 50 px widget height + 1 px spacing
        self._scroll_area.setMaximumHeight(51 * num_widgets)
        # Horizontal Policy: MinimumExpanding --> widget text gets displayed
        # Vertical Policy: Maximum --> is set to the number of visible widgets
        self._scroll_area.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Maximum
        )

        self._scroll_area.setWidgetResizable(True)
        widget = QWidget(self._scroll_area)
        # ObjectName to style the background in stylesheet
        widget.setObjectName("scroll_widget")
        self._scroll_area.setWidget(widget)
        # the main widgets will be added later to middle_layout
        self._middle_layout = QVBoxLayout()
        self._middle_layout.setContentsMargins(0, 0, 0, 0)
        self._middle_layout.setSpacing(1)
        widget.setLayout(self._middle_layout)

    def _add_bottom_widgets(self, widgets: Iterable[type[BaseWidget]]) -> None:
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

    @Slot(name="on_left_column_button")
    def on_left_column_button(self) -> None:
        """Handle a click on one of the buttons for left column widgets."""
        widget_class = cast(LeftMenuButton[Any], self.sender()).widget_class
        log.debug("Emitting bottom_button_clicked for class %s", widget_class)
        self.bottom_button_clicked.emit(widget_class)

    @Slot(name="on_main_page_button")
    def on_main_page_button(self) -> None:
        """Handle a click on one of the buttons for left column widgets."""
        widget_class = cast(LeftMenuButton[Any], self.sender()).widget_class
        log.debug("Emitting top_button_clicked for class %s", widget_class)
        self.top_button_clicked.emit(widget_class)

    @Slot(name="toggle_animation")
    def toggle_animation(self) -> None:
        """
        Toggle the animation (closing/opening the menu).

        Animation is working with the minimum width of the parent widget.
        """
        parent_margin = (
            self.parent().layout().contentsMargins().left()
            + self.parent().layout().contentsMargins().right()
        )
        parent_width = self.parent().width()
        self._animation.stop()
        closed = self.minimumWidth() + parent_margin == parent_width
        self._animation.setStartValue(self.parent().width())
        self._animation.setEndValue(
            240 if closed else self.minimumWidth() + parent_margin
        )
        # if closed, menu is expanding so set toggle active
        # if not closed, menu is closing set toggle not active
        self._toggle_button.set_active_toggle(closed)
        icon = LeftMenu.ICON_PATH_CLOSE if closed else LeftMenu.ICON_PATH_OPEN
        self._toggle_button.set_icon(icon)
        self._animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self._animation.setDuration(500)
        self._animation.start()

    def _button(
        self, widget_class: type[BaseWidgetType]
    ) -> LeftMenuButton[BaseWidgetType]:
        """Return the button for the given widget class."""
        for btn in self.findChildren(LeftMenuButton):
            if btn.widget_class == widget_class:
                return cast(LeftMenuButton[BaseWidgetType], btn)
        raise ValueError(  # pragma: no cover
            f"Could not find button for widget: {widget_class}"
        )

    def set_button_active(
        self,
        widget_class: type[BaseWidgetType],
        active: bool,
    ) -> None:
        """Set the button for the given widget active/inactive."""
        button = self._button(widget_class)
        button.set_active(active)
        button.set_active_tab(active)
