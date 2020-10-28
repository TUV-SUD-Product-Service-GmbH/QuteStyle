"""Main window class for TSL applications."""
import logging
import os
import subprocess
import sys
from typing import Optional

from PyQt5.QtCore import Qt, pyqtSlot, QObject, QEvent, QThread
from PyQt5.QtWidgets import QWidget, QMainWindow, QProgressDialog, QMessageBox

from tsl.updater import LAGER_PATH, Updater

LOG_NAME = ".".join(["tsl", __name__])
log = logging.getLogger(LOG_NAME)  # pylint: disable=invalid-name


class TSLMainWindow(QMainWindow):
    """Main window class for TSL applications."""

    # pylint: disable=too-many-instance-attributes, too-many-arguments
    def __init__(self, update: bool, help_text: str, name: str, version: str,
                 parent: QWidget = None) -> None:
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

    def show(self) -> None:
        """Override show to start update just before."""
        if self._update:
            log.debug("Starting update.")
            # only run the update if not suppressed by -u
            self._updater_thread = QThread()
            self._updater = Updater(self._app_name, self._version)
            self._updater.moveToThread(self._updater_thread)
            self._updater.update_available.connect(self.update_status)
            self._updater_thread.started.connect(  # type: ignore
                self._updater.start_update)
            self._updater.updater_checked.connect(self._updater_thread.quit)
            self._updater_thread.finished.connect(  # type: ignore
                self.updater_finished)
            self._updater_thread.start()
        else:
            log.debug("Suppressing update with -u or running from IDE.")
            self.update_status(False)
        super(TSLMainWindow, self).show()

    def _handle_update_window(self) -> None:
        """Handle the update window."""
        log.debug("Handling for update status: %s", self._update_status)

        if self._update_status is True:
            log.debug("Update available - updating progress text.")
            self._progress.setLabelText("Aktualisierung verfügbar - "
                                        "Vorbereitung im Gange.")
            self._progress.setValue(0)

        elif self._update_status is None:
            log.debug("Update status not available yet.")
            self._progress.setValue(0)

        elif self._update_status is False:
            log.debug("No update available, closing progress window.")
            self._close_progress_window()

    def _configure_update(self) -> None:
        """Configure the update functionality."""
        self._progress: QProgressDialog = \
            QProgressDialog("Prüfe auf Aktualisierung...", "Abbrechen",
                            0, 0, self)
        self._progress.setMinimumDuration(0)
        self._progress.setCancelButton(None)  # type: ignore
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
    def eventFilter(self, obj: QObject, event: QEvent)\
            -> bool:  # pylint: disable=invalid-name
        """Filter events received in the MainWindow."""
        if obj is self._progress and event.type() == QEvent.Close:
            # prevent closing of progress dialog.
            log.debug("Filtering close event of progress dialog.")
            event.ignore()
            return True
        return False

    @pyqtSlot(name="on_about")
    def on_about(self) -> None:
        """Show a message box about the used app version."""
        log.debug("User pressed button to show dialog about %s",
                  self._app_name)
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
            subprocess.Popen([
                os.path.join(os.path.expanduser("~"), "TSL", "Updater",
                             "App-Updater.exe"),
                r"/ROOT:" + os.path.abspath(sys.argv[0]),
                r"/TEXTFILE:" + os.path.join(LAGER_PATH, self._app_name,
                                             "TSL-Update", "update.json")
            ])
            sys.exit()
        else:
            log.debug("No update is available.")

    def _close_progress_window(self) -> None:
        """Uninstall the eventfilter and then close the progress window."""
        self._progress.removeEventFilter(self)
        self._progress.close()
