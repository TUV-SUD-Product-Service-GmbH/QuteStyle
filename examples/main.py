"""Test script to validate TSL style."""
from __future__ import annotations

import importlib
import logging
import sys
import time
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from examples.styled_main_window import StyledMainWindow
from tsl.dev.dev_functions import generate_changelog_resource_file
from tsl.init import SETTINGS, init
from tsl.startup_threads import StartupThread
from tsl.tsl_application import TslApplication
from tsl.update_window import AppData

log = logging.getLogger(f"tsl.{__name__}")  # pylint: disable=invalid-name


def create_new_changelog_resource_file(app_name: str) -> None:
    """Create the changelog resource file and import it."""
    path = Path.cwd().parent / "examples"
    generate_changelog_resource_file(app_name, path / "test_changelog", path)

    importlib.import_module("examples.resources_cl")


class DummyThread(StartupThread):  # pragma: no cover
    """Dummy thread for sample app."""

    def _function_to_execute(self) -> None:
        """Thread run."""
        log.debug("Start dummy startup thread.")
        time.sleep(1)


class TSLCustomApplication(TslApplication):
    """TSLCustomApplication."""

    STARTUP_THREADS = [DummyThread]

    MAIN_WINDOW_CLASS = StyledMainWindow

    APP_DATA = AppData(
        "Test-App",
        "2.3.4",
        ":/svg_images/logo_toolbox.svg",
        ":/svg_images/logo_toolbox.svg",
        "",
    )


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

    APP = TSLCustomApplication(sys.argv)
    sys.exit(APP.exec())
