"""Test script to validate QuteStyle app."""
from __future__ import annotations

import importlib
import logging
import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from examples.sample_main_window import StyledMainWindow
from qute_style.dev.dev_functions import generate_changelog_resource_file
from qute_style.qs_application import QuteStyleApplication
from qute_style.update_window import AppData

log = logging.getLogger(
    f"qute_style.{__name__}"
)  # pylint: disable=invalid-name


def create_new_changelog_resource_file(app_name: str) -> None:
    """Create the changelog resource file and import it."""
    path = Path.cwd() / "examples"
    if not path.exists():
        path = Path.cwd().parent / "examples"
    generate_changelog_resource_file(app_name, path / "test_changelog", path)

    importlib.import_module("examples.resources_cl")


class QuteStyleCustomApplication(QuteStyleApplication):
    """QuteStyleCustomApplication."""

    MAIN_WINDOW_CLASS = StyledMainWindow

    APP_DATA = AppData(
        "Test-App",
        "2.3.4",
        ":/svg_images/logo_toolbox.svg",
        ":/svg_images/logo_toolbox.svg",
        "",
        "Test Version",
    )


if __name__ == "__main__":
    APP_NAME = "Test-App"

    # Create the resource file everytime the application starts.
    # No need to add it as a resource for the demo app
    create_new_changelog_resource_file(APP_NAME)

    # activate highdpi icons and scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    APP = QuteStyleCustomApplication(sys.argv)
    sys.exit(APP.exec())
