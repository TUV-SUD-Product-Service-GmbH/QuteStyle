"""Main window class for TSL applications."""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Optional

from PyQt5.QtCore import QSettings, pyqtSlot
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QWidget

import qute_style.resources_rc  # pylint: disable=unused-import  # noqa: F401
from qute_style.whats_new_window import WhatsNewWindow

LOG_NAME = ".".join(["tsl", __name__])
log = logging.getLogger(LOG_NAME)  # pylint: disable=invalid-name


@dataclass
class AppData:
    """Provide required data to startup threads."""

    app_name: str = ""
    app_version: str = ""
    app_icon: str = ""
    app_splash_icon: str = ""
    help_text: str = ""


class TSLMainWindow(QMainWindow):
    """Main window class for TSL applications."""

    WHATS_NEW = True

    def __init__(
        self,
        app_data: AppData,
        force_whats_new: bool = False,
        registry_reset: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        """Create a new QuteStyleMainWindow."""
        super().__init__(parent)
        self._app_data = app_data
        self._force_whats_new: bool = force_whats_new
        self._whats_new_window: Optional[WhatsNewWindow] = None
        if registry_reset:
            log.debug("Resetting QSettings in Registry.")
            QSettings().clear()

    def show(self) -> None:
        """Override show to start update just before."""
        self._load_settings()
        super().show()
        self._handle_last_run()

    def _handle_last_run(self) -> None:
        """Check if the What's new window needs to be shown."""
        last_run = QSettings().value("last_run", (0, 0, 0))
        log.debug("Last run showed details for version %s", last_run)
        current_ver = tuple(
            int(num) for num in self._app_data.app_version.split(".")
        )
        if last_run < current_ver or self._force_whats_new and self.WHATS_NEW:
            log.debug(
                "Current version newer than last run %s",
                self._app_data.app_version,
            )
            # if we force whats new display, we show the error message, even if
            # nothing is visible.
            self._display_whats_new(not self._force_whats_new)
            QSettings().setValue("last_run", current_ver)

    @pyqtSlot(name="on_whats_new")
    def on_whats_new(self) -> None:
        """Display the WhatsNewWindow."""
        # Slot shall not be called when WhatsNew is disabled.
        assert self.WHATS_NEW
        self._display_whats_new(False)

    def _display_whats_new(self, silent: bool = True) -> None:
        """Display the Window with the changes for the current version."""
        filename = (
            f"changes/{self._app_data.app_version}/"
            f"{self._app_data.app_version}.json"
        )
        try:
            with open(
                filename,
                encoding="utf-8",
            ) as fhdl:
                entries = json.loads(fhdl.read())
        except FileNotFoundError:
            log.warning("Changes file not found %s", filename)
            return

        if not entries:
            if not silent:
                log.warning("There are no relevant entries for the user.")
                title = self.tr("Keine Neuerungen")
                text = self.tr(
                    "Die aktuelle Version enthält keine Neuerungen,"
                    " die für den aktuellen Nutzer verfügbar sind."
                )
                QMessageBox.information(self, title, text)
            return
        self._whats_new_window = WhatsNewWindow(
            entries, self._app_data.app_version
        )
        self._whats_new_window.show()

    @pyqtSlot(QCloseEvent, name="closeEvent")
    def closeEvent(  # pylint: disable=invalid-name
        self, close_event: QCloseEvent
    ) -> None:
        """Handle a close event."""
        if self._whats_new_window:
            log.debug("WhatsNewWindow is still open, closing.")
            self._whats_new_window.close()
        self._save_settings()
        super().closeEvent(close_event)

    def _save_settings(self) -> None:
        """Save the paint data and state/geometry settings."""
        log.debug("Saving settings to registry.")
        settings = QSettings()
        settings.setValue("state", self.saveState())
        settings.setValue("geometry", self.saveGeometry())
        log.debug("Finished writing settings to registry")

    def _load_settings(self) -> None:
        """Load geometry and state settings of the ui."""
        log.debug("Loading settings from registry")
        settings = QSettings()
        try:
            self.restoreGeometry(settings.value("geometry"))
        except TypeError:
            log.warning(
                "Could not restore geometry from: %s",
                settings.value("geometry"),
            )
        try:
            self.restoreState(settings.value("state"))
        except TypeError:
            log.warning(
                "Could not restore state from: %s", settings.value("state")
            )

    @pyqtSlot(name="on_about")
    def on_about(self) -> None:
        """Show a message box about the used app version."""
        log.debug(
            "User pressed button to show dialog about %s",
            self._app_data.app_name,
        )
        title = self.tr("Über {}").format(self._app_data.app_name)
        QMessageBox.about(self, title, self._app_data.help_text)
