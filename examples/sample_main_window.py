"""Styled main window sample."""
from __future__ import annotations

import logging

from PyQt5.QtCore import QSize, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from examples.sample_widgets import ModelViewWidget, TestWidget
from qute_style.qs_main_window import AppData, QuteStyleMainWindow
from qute_style.style import THEMES, get_current_style
from qute_style.widgets.base_widgets import BaseWidget, SettingsBaseWidget
from qute_style.widgets.color_manager import ColorManager
from qute_style.widgets.home_page import HomePage
from qute_style.widgets.icon_button import IconButton

log = logging.getLogger(
    f"qute_style.{__name__}"
)  # pylint: disable=invalid-name


class SettingsWidget(SettingsBaseWidget):
    """Test SettingsWidget."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a new SettingsWidget."""
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.layout().addWidget(QLabel("Global settings"))
        self.layout().addItem(
            QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        )
        self._set_global_widget(self)


class InfoWidget(BaseWidget):
    """Test ColumnBaseWidget."""

    ICON = ":/svg_icons/info.svg"
    NAME = "Info"

    switch_style = pyqtSignal(name="switch_style")

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

    MAIN_WIDGET_CLASSES = [HomePage, TestWidget, ModelViewWidget]
    RIGHT_WIDGET_CLASSES = [ColorManager]
    LEFT_WIDGET_CLASSES = [SettingsWidget, InfoWidget]

    MIN_SIZE = QSize(800, 600)

    def __init__(
        self,
        app_data: AppData,
        registry_reset: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        """Create a new StyledMainWindow."""
        super().__init__(
            app_data,
            False,
            registry_reset,
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

    @pyqtSlot(name="on_switch_style")
    def on_switch_style(self) -> None:
        """Set the next available style."""
        self._current_idx += 1
        if self._current_idx == len(THEMES.keys()):
            self._current_idx = 0
        style = list(THEMES.keys())[self._current_idx]
        self.on_change_theme(style)
