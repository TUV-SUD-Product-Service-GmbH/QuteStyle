"""Styled main window sample."""

from __future__ import annotations

import logging

from PySide6.QtCore import QSize, Signal, Slot
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from qute_style.qs_main_window import AppData, QuteStyleMainWindow
from qute_style.style import THEMES, get_current_style
from qute_style.widgets.base_widgets import BaseWidget, SettingsBaseWidget
from qute_style.widgets.color_manager import ColorManager
from qute_style.widgets.home_page import HomePage
from qute_style.widgets.icon_button import IconButton
from qute_style_examples.sample_widgets import (
    ModelViewWidget,
    SpinnerWidget,
    TestWidget,
)

log = logging.getLogger(f"qute_style.{__name__}")


class SettingsWidget(SettingsBaseWidget):
    """Test SettingsWidget."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a new SettingsWidget."""
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.layout().addWidget(QLabel("Global settings"))
        self.layout().addItem(
            QSpacerItem(
                0,
                0,
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding,
            )
        )
        self._set_global_widget(self)


class InfoWidget(BaseWidget):
    """Test ColumnBaseWidget."""

    ICON = ":/svg_icons/info.svg"
    NAME = "Info"

    switch_style = Signal(name="switch_style")

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a new SettingsWidget."""
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.addWidget(QLabel("Switch style"))
        button = IconButton(self, ":/svg_icons/send.svg")
        layout.addWidget(button)
        button.clicked.connect(self.switch_style)


class StyledMainWindow(QuteStyleMainWindow):
    """Test StyledMainWindow for validation of QuteStyle Darcula Style."""

    MAIN_WIDGET_CLASSES = [
        HomePage,
        TestWidget,
        ModelViewWidget,
        SpinnerWidget,
    ]
    RIGHT_WIDGET_CLASSES = [ColorManager]
    LEFT_WIDGET_CLASSES = [SettingsWidget, InfoWidget]

    MIN_SIZE = QSize(800, 600)

    def __init__(  # noqa: PLR0913
        self,
        app_data: AppData,
        registry_reset: bool = False,
        force_whats_new: bool = False,
        load_last_used_widget: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        """Create a new StyledMainWindow."""
        super().__init__(
            app_data,
            force_whats_new,
            registry_reset,
            load_last_used_widget,
            parent,
        )
        self._left_column.widget(InfoWidget).switch_style.connect(
            self.on_switch_style
        )

        try:
            self._current_idx = (
                "Snow White",
                "Princess Pink",
                "Darcula",
                "Highbridge Gray",
                "Ruby Red",
            ).index(get_current_style())
        except KeyError:
            self._current_idx = 0

    @Slot(name="on_switch_style")
    def on_switch_style(self) -> None:
        """Set the next available style."""
        self._current_idx += 1
        if self._current_idx == len(THEMES.keys()):
            self._current_idx = 0
        style = list(THEMES.keys())[self._current_idx]
        self.on_change_theme(style)
