"""Test script to validate TSL style."""
from __future__ import annotations

import importlib
import logging
import sys
from pathlib import Path

from PyQt5.QtCore import QCoreApplication, QSize, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)

from examples.sample_widgets import ModelViewWidget, TestWidget
from tsl.dev.dev_functions import generate_changelog_resource_file
from tsl.init import SETTINGS, init
from tsl.style import (
    THEMES,
    Themes,
    get_current_style,
    get_style,
    set_current_style,
)
from tsl.tsl_main_gui import TSLStyledMainWindow
from tsl.widgets.base_widgets import BaseWidget
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


class SettingsWidget(BaseWidget):
    """Test ColumnBaseWidget."""

    ICON = ":/svg_icons/settings.svg"
    NAME = "Einstellungen"

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a new SettingsWidget."""
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Dies ist ein Text-Text \n" * 10))
        layout.addWidget(QTableWidget())


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

    LOGO = ":/svg_images/logo_toolbox.svg"

    def __init__(  # pylint: disable=too-many-arguments
        self,
        update: bool,
        help_text: str,
        name: str,
        version: str,
        force_whats_new: bool = False,
        registry_reset: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        """Create a new StyledMainWindow."""
        super().__init__(
            update,
            help_text,
            name,
            version,
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


def create_new_changelog_resource_file(app_name: str) -> None:
    """Create the changelog resource file and import it."""
    path = Path.cwd().parent / "examples"
    generate_changelog_resource_file(app_name, path / "test_changelog", path)

    importlib.import_module("examples.resources_cl")


if __name__ == "__main__":
    SETTINGS["log_level"] = logging.DEBUG
    APP_NAME = "Test-App"
    init(APP_NAME, logs=True, hook=True, registry=True)

    # Create the resource file everytime the application starts.
    # No need to add it as a resource for the demo app
    create_new_changelog_resource_file(APP_NAME)

    # activate highdpi icons and scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    APP = QApplication(sys.argv)
    QCoreApplication.setApplicationName(APP_NAME)
    QCoreApplication.setOrganizationName("TÜV SÜD Product Service GmbH")
    QCoreApplication.setOrganizationDomain("tuvsud.com")
    WINDOW = StyledMainWindow(False, "", APP_NAME, "2.3.4", False)
    WINDOW.show()
    sys.exit(APP.exec())
