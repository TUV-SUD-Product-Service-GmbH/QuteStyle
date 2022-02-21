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
from tsl.style import (
    THEMES,
    Themes,
    get_current_style,
    get_style,
    set_current_style,
)
from tsl.tsl_main_gui import TSLStyledMainWindow
from tsl.update_window import AppData
from tsl.widgets.base_widgets import BaseWidget, SettingsBaseWidget
from tsl.widgets.color_manager import ColorManager
from tsl.widgets.home_page import HomePage
from tsl.widgets.icon_button import IconButton
from tsl.widgets.toggle import Toggle

log = logging.getLogger(f"tsl.{__name__}")  # pylint: disable=invalid-name


class RightWidget(BaseWidget):
    """Test ColumnBaseWidget."""

    ICON = ":/svg_icons/icon_PSE.svg"
    NAME = "PSE Informationen"

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a new RightWidget."""
        super().__init__(parent)

        layout = QHBoxLayout()

        pse_info_button = IconButton(
            self, icon_path=":/svg_icons/clipboard.svg"
        )
        layout.addWidget(pse_info_button)
        rcolumn_spacer1 = QSpacerItem(
            20, 40, QSizePolicy.Fixed, QSizePolicy.Fixed
        )
        layout.addItem(rcolumn_spacer1)
        toggle_test = Toggle()
        layout.addWidget(toggle_test)

        self.setLayout(layout)


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


class StyledMainWindow(TSLStyledMainWindow):
    """Test StyledMainWindow for validation of TSL Darcula Style."""

    MAIN_WIDGET_CLASSES = [HomePage, TestWidget, ModelViewWidget]
    RIGHT_WIDGET_CLASSES = [RightWidget, ColorManager]
    LEFT_WIDGET_CLASSES = [SettingsWidget, InfoWidget]

    MIN_SIZE = QSize(800, 600)

    def __init__(
        self,
        app_data: AppData,
        force_whats_new: bool = False,
        registry_reset: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        """Create a new StyledMainWindow."""
        super().__init__(
            app_data,
            force_whats_new,
            registry_reset,
            parent,
        )
        self._left_column.widget(InfoWidget).switch_style.connect(
            self.on_switch_style
        )

        try:
            self._current_idx = (
                Themes.SNOW_WHITE,
                Themes.DARCULA,
                Themes.PRINCESS_PINK,
                Themes.HIGHBRIDGE_GRAY,
                Themes.RUBY_RED,
            ).index(get_current_style())
        except KeyError:
            self._current_idx = 0

    @pyqtSlot(name="on_switch_style")
    def on_switch_style(self) -> None:
        """Set the next available style."""
        self._current_idx += 1
        if self._current_idx == len(THEMES.keys()):
            self._current_idx = 0
        style_name = tuple(THEMES.keys())[self._current_idx]
        set_current_style(style_name)
        self.setStyleSheet(get_style())
        self.update()
