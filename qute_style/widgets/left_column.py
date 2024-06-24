"""Widget that contains the widgets of the left column."""

from __future__ import annotations

import logging
from typing import TypeVar, cast

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLayout,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from qute_style.widgets.base_widgets import BaseWidget, SettingsBaseWidget
from qute_style.widgets.icon import Icon
from qute_style.widgets.left_column_close_button import LeftColumnCloseButton

log = logging.getLogger(
    f"qute_style.{__name__}"
)  # pylint: disable=invalid-name

BaseWidgetT = TypeVar("BaseWidgetT", bound=BaseWidget)


class LeftColumn(QWidget):
    """Widget that contains the widgets of the left column."""

    close_column = Signal(name="close_column")

    def __init__(
        self,
        app_parent: QWidget,
        widget_types: list[type[BaseWidget]],
        parent: QWidget | None = None,
    ):
        """Create a new LeftColumn."""
        super().__init__(parent)
        # Create all widgets that shall be displayed in the left column.
        log.debug("Creating LeftColumn with widgets %s", widget_types)
        self._widgets = [widget_type() for widget_type in widget_types]

        # Create the main layout.
        base_layout = QVBoxLayout(self)

        # Set the top margin to 4 so that the header will be aligned with the
        # menu button's focus frame and the title bar.
        base_layout.setContentsMargins(0, 4, 0, 0)
        base_layout.setSpacing(0)

        # Create the title frame that contains icon, text and close button.
        self._icon, self._title_label = self._create_title_frame(
            app_parent, base_layout
        )

        # Create the content frame with a QStackedWidget containing all widgets
        # in widget_types.
        self._stacked_widget, self._widgets = self.create_content_frame(
            base_layout, widget_types
        )

        # Set the first widget so that title text is set.
        if widget_types:
            self.set_column_widget(widget_types[0])

    @staticmethod
    def create_content_frame(
        base_layout: QLayout,
        widget_types: list[type[BaseWidget]],
    ) -> tuple[QStackedWidget, list[BaseWidget]]:
        """
        Create the content QFrame and add it to the given layout.

        The frame contains a layout that wraps a QStackedWidget with a margin
        of 5 pixels on each side. The QStackedWidget contains all widgets that
        will be shown in the column when pressing the respective buttons in the
        LeftMenu.

        This method also creates the widgets in widget_types and returns them
        together with the QStackedWidget.
        """
        content_frame = QFrame()
        base_layout.addWidget(content_frame)
        main_pages_layout = QVBoxLayout(content_frame)
        main_pages_layout.setContentsMargins(5, 5, 5, 5)
        stacked_widget = QStackedWidget(content_frame)
        main_pages_layout.addWidget(stacked_widget)
        widgets = [widget_type() for widget_type in widget_types]
        for widget in widgets:
            stacked_widget.addWidget(widget)
        return stacked_widget, widgets

    def _create_title_frame(
        self, app_parent: QWidget, layout: QLayout
    ) -> tuple[Icon, QLabel]:
        """
        Create the title frame containing icon, title and close button.

        Adds the title frame to the given layout.
        """
        # Create the QFrame that contains all elements.
        title_frame = QFrame()
        title_frame.setFixedHeight(47)
        title_base_layout = QVBoxLayout(title_frame)
        title_base_layout.setContentsMargins(5, 3, 5, 3)

        # Create a background QFrame that paints the box around the elements.
        title_bg_frame = QFrame()
        title_bg_frame.setObjectName("title_bg_frame")
        title_bg_layout = QHBoxLayout(title_bg_frame)
        title_bg_layout.setContentsMargins(5, 5, 5, 5)
        title_bg_layout.setSpacing(3)

        # Add the Icon that is painted in the given color.
        icon = Icon()
        title_bg_layout.addWidget(icon)

        # Add the title QLabel.
        title_label = QLabel()
        title_label.setObjectName("column_title_label")
        title_bg_layout.addWidget(title_label)

        # Add the button to close the column.
        btn_close = LeftColumnCloseButton(
            app_parent,
            tooltip_text=self.tr("Schließen"),
            icon_path=":/svg_icons/close.svg",
        )
        btn_close.clicked.connect(self.close_column)
        btn_close.setFixedSize(30, 30)
        title_bg_layout.addWidget(btn_close)

        # Add the title background QFrame to the title's layout.
        title_base_layout.addWidget(title_bg_frame)

        # Add the title QFrame to the layout.
        layout.addWidget(title_frame)

        # Return Icon and title QLabel
        return icon, title_label

    def handle_settings_display(
        self, settings_widget: None | QWidget, icon: str
    ) -> None:
        """Handle the display of the settings widget."""
        current_type = self.current_widget_type()
        assert current_type is not None

        # Check if settings are displayed
        # Do not change to isinstance
        if issubclass(current_type, SettingsBaseWidget):
            current_widget = self.widget(current_type)
            # Clear settings
            # clear_widget() and add_widget() are methods of SettingsBaseWidget
            current_widget.clear_widget()

            # Set general settings icon
            self._icon.set_icon(current_widget.ICON)

            # If specific settings, add widget and set specific Icon
            if settings_widget:
                current_widget.add_widget(settings_widget)
                self._icon.set_icon(icon)

    def set_column_widget(self, widget_type: type[BaseWidget]) -> None:
        """Set left column pages."""
        log.debug("Setting current widget to: %s", widget_type)
        widget = self.widget(widget_type)
        self._stacked_widget.setCurrentWidget(widget)
        self._title_label.setText(widget.NAME)
        self._icon.set_icon(widget.ICON)

    def widget(self, widget_type: type[BaseWidgetT]) -> BaseWidgetT:
        """Get the widget of the given type."""
        for widget in self._widgets:
            if isinstance(widget, widget_type):
                return widget
        raise ValueError(  # pragma: no cover
            f"Could not find widget {widget_type}"
        )

    def current_widget_type(self) -> type[BaseWidget] | None:
        """Return the currently active widget class."""
        if widget := self._stacked_widget.currentWidget():
            return cast(type[BaseWidget], type(widget))
        # Return None explicitly instead of <class NoneType>
        return None
