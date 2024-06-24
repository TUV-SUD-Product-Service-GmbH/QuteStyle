"""Test script to validate QuteStyle app."""

from __future__ import annotations

import logging
import sys
from importlib import import_module, resources

from PySide6.QtCore import (
    QMessageLogContext,
    QtMsgType,
    qInstallMessageHandler,
)

from qute_style.dev.dev_functions import generate_changelog_resource_file
from qute_style.qs_application import QuteStyleApplication
from qute_style.qs_main_window import AppData
from qute_style_examples.sample_main_window import StyledMainWindow

log = logging.getLogger(
    f"qute_style.{__name__}"
)  # pylint: disable=invalid-name


def create_new_changelog_resource_file(app_name: str) -> None:
    """Create the changelog resource file and import it."""
    traversable = resources.files("qute_style_examples")
    with resources.as_file(traversable) as path:
        generate_changelog_resource_file(
            app_name, path / "test_changelog", path
        )
        import_module("qute_style_examples.resources_cl")


def configure_logging() -> None:
    """Configure logging for the example app."""
    format_str = (
        "%(asctime)s.%(msecs)03d %(threadName)10s  - "
        "%(name)-50s - %(funcName)-25s:%(lineno)-4s - "
        "%(levelname)-8s - %(message)s"
    )
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(format_str, date_format)

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger("qute_style")
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    def qt_message_handler(
        mode: QtMsgType, _: QMessageLogContext, message: str
    ) -> None:
        """Handle messages from Qt logging."""
        level = {
            QtMsgType.QtDebugMsg: logging.DEBUG,
            QtMsgType.QtInfoMsg: logging.INFO,
            QtMsgType.QtWarningMsg: logging.WARNING,
            QtMsgType.QtCriticalMsg: logging.ERROR,
            QtMsgType.QtFatalMsg: logging.FATAL,
        }[mode]
        log.log(level, message)

    qInstallMessageHandler(qt_message_handler)


class QuteStyleCustomApplication(QuteStyleApplication):
    """QuteStyleCustomApplication."""

    MAIN_WINDOW_CLASS = StyledMainWindow

    APP_DATA = AppData(
        "Test-App",
        "2.3.4",
        ":/svg_images/logo_qute_style.svg",
        ":/svg_images/logo_qute_style.svg",
        "",
        "Test Version",
        "Sample Organization",
        "sample_organization.com",
    )


def main_method() -> None:
    """Run sample application."""
    configure_logging()

    # Create the resource file everytime the application starts.
    # No need to add it as a resource for the demo app
    create_new_changelog_resource_file("Test-App")

    app = QuteStyleCustomApplication(sys.argv)
    sys.exit(app.exec())


if __name__ == "__main__":
    main_method()
