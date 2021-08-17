"""Main window class for TSL applications."""
import json
import logging
import os
import subprocess
import sys
from typing import Optional

from PyQt5.QtCore import Qt, pyqtSlot, QObject, QEvent, QThread, QSettings
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QWidget, QMainWindow, QProgressDialog, QMessageBox

from tsl.edoc_database import get_user_group_name
from tsl.updater import LAGER_PATH, Updater
from tsl.whats_new_window import WhatsNewWindow

LOG_NAME = ".".join(["tsl", __name__])
log = logging.getLogger(LOG_NAME)  # pylint: disable=invalid-name


class TSLMainWindow(QMainWindow):
    """Main window class for TSL applications."""

    # pylint: disable=too-many-instance-attributes, too-many-arguments
    def __init__(
        self,
        update: bool,
        help_text: str,
        name: str,
        version: str,
        force_whats_new: bool = False,
        parent: QWidget = None,
    ) -> None:
        """Create a new TSL main window."""
        super(TSLMainWindow, self).__init__(parent)
        self._update_status: Optional[bool] = None
        self._configure_update()
        self._help_text: str = help_text
        self._app_name: str = name
        self._version: str = version
        self._update: bool = update
        self._updater: Optional[Updater] = None
        self._updater_thread: Optional[QThread] = None
        self._force_whats_new: bool = force_whats_new
        self._whats_new_window: Optional[WhatsNewWindow] = None

    def show(self) -> None:
        """Override show to start update just before."""
        self._load_settings()
        if self._update:
            log.debug("Starting update.")
            # only run the update if not suppressed by -u
            self._updater_thread = QThread()
            self._updater = Updater(self._app_name, self._version)
            self._updater.moveToThread(self._updater_thread)
            self._updater.update_available.connect(self.update_status)
            self._updater_thread.started.connect(self._updater.start_update)
            self._updater.updater_checked.connect(self._updater_thread.quit)
            self._updater_thread.finished.connect(self.updater_finished)
            self._updater_thread.start()
        else:
            log.debug("Suppressing update with -u or running from IDE.")
            self.update_status(False)
        super(TSLMainWindow, self).show()
        self._handle_last_run()

    def _handle_last_run(self) -> None:
        """Check if the What's new window needs to be shown."""
        last_run = QSettings().value("last_run", (0, 0, 0))
        log.debug("Last run showed details for version %s", last_run)
        current_ver = tuple([int(num) for num in self._version.split(".")])
        if last_run < current_ver or self._force_whats_new:
            log.debug("Current version newer than last run %s", self._version)
            # if we force whats new display, we show the error message, even if
            # nothing is visible.
            self._display_whats_new(not self._force_whats_new)
            QSettings().setValue("last_run", current_ver)

    @pyqtSlot(name="on_display_whats_new")
    def on_whats_new(self) -> None:
        """Display the WhatsNewWindow."""
        self._display_whats_new(False)

    def _display_whats_new(self, silent: bool = True) -> None:
        """Display the Window with the changes for the current version."""
        filename = f"changes/{self._version}/{self._version}.json"
        try:
            with open(
                filename,
                encoding="utf-8",
            ) as fhdl:
                entries = json.loads(fhdl.read())
        except FileNotFoundError:
            log.warning("Changes file not found %s", filename)
            return

        # filter out entries, for which a team restriction is specified and
        # that do not contain the user's team in this specification
        grp = get_user_group_name()
        entries = [
            entry
            for entry in entries
            if grp in entry["user_groups"] or not entry["user_groups"]
        ]

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
        self._whats_new_window = WhatsNewWindow(entries, self._version)
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
        super(TSLMainWindow, self).closeEvent(close_event)

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

    def _handle_update_window(self) -> None:
        """Handle the update window."""
        log.debug("Handling for update status: %s", self._update_status)

        if self._update_status is True:
            log.debug("Update available - updating progress text.")
            self._progress.setLabelText(
                "Aktualisierung verfügbar - " "Vorbereitung im Gange."
            )
            self._progress.setValue(0)

        elif self._update_status is None:
            log.debug("Update status not available yet.")
            self._progress.setValue(0)

        elif self._update_status is False:
            log.debug("No update available, closing progress window.")
            self._close_progress_window()

    def _configure_update(self) -> None:
        """Configure the update functionality."""
        self._progress = QProgressDialog(
            "Prüfe auf Aktualisierung...", "Abbrechen", 0, 0, self
        )
        self._progress.setMinimumDuration(0)
        self._progress.setCancelButton(None)
        self._progress.setModal(True)
        flags = self._progress.windowFlags()
        self._progress.setWindowFlags(
            flags  # type: ignore
            & ~Qt.WindowCloseButtonHint
            & ~Qt.WindowContextHelpButtonHint
            | Qt.MSWindowsFixedSizeDialogHint
        )
        self._progress.installEventFilter(self)

    @pyqtSlot(QObject, QEvent, name="eventFilter")
    def eventFilter(  # pylint: disable=invalid-name
        self, obj: QObject, event: QEvent
    ) -> bool:
        """Filter events received in the StyledMainWindow."""
        if obj is self._progress and event.type() == QEvent.Close:
            # prevent closing of progress dialog.
            log.debug("Filtering close event of progress dialog.")
            event.ignore()
            return True
        return False

    @pyqtSlot(name="on_about")
    def on_about(self) -> None:
        """Show a message box about the used app version."""
        log.debug(
            "User pressed button to show dialog about %s", self._app_name
        )
        title = self.tr(f"Über {self._app_name}")
        QMessageBox.about(self, title, self._help_text)

    @pyqtSlot(bool, name="update_status")
    def update_status(self, update_available: bool) -> None:
        """Handle the update status of the Updater."""
        log.debug("Update status from Updater: %s", update_available)
        self._update_status = update_available
        self._handle_update_window()

    @pyqtSlot(name="updater_finished")
    def updater_finished(self) -> None:
        """Handle a signal that the updater has finished."""
        log.debug("Received signal that updater has finished")
        if self._progress.isVisible():
            log.debug("Hiding progress window")
            self._close_progress_window()

        if self._update_status is True:
            log.debug("Update is available.")
            subprocess.Popen(
                [
                    os.path.join(
                        os.path.expanduser("~"),
                        "TSL",
                        "Updater",
                        "App-Updater.exe",
                    ),
                    r"/ROOT:" + os.path.abspath(sys.argv[0]),
                    r"/TEXTFILE:"
                    + os.path.join(
                        LAGER_PATH, self._app_name, "TSL-Update", "update.json"
                    ),
                ]
            )
            sys.exit()
        else:
            log.debug("No update is available.")

    def _close_progress_window(self) -> None:
        """Uninstall the eventfilter and then close the progress window."""
        self._progress.removeEventFilter(self)
        self._progress.close()
