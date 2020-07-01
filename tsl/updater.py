"""Updater object for updating TSL Apps."""
import json
import logging
import os
from os.path import expanduser
from typing import cast, Optional

from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal

from tsl.copy_worker import CopyWorker
from tsl.init import check_ide

log = logging.getLogger("tsl.updater")  # pylint: disable=invalid-name

LAGER_PATH = r"\\DE001.itgr.net\PS\RF-UnitPSMUC\Lager"


class Updater(QObject):
    """
    Updater to handle and perform updates for TSL apps.

    The Updater will be given the name and the version where it is used. The
    Updater will ensure, that the TSL App-Updater is installed and up-to-date.

    The Updater will check, if an update for the app is available and emit the
    following signals:
    - update_available: Signals, if an update is available. If so, the app
                        must wait, until updater_checked is emitted.
    - updater_checked: Signals, that the updater was successfully check. The
                       App can then start an update or destroy the Updater.

    """

    update_available = pyqtSignal(bool, name="update_available")
    updater_checked = pyqtSignal(name="updater_checked")

    def __init__(self, app_name: str, version: str, parent: QObject = None):
        """Init the Updater."""
        super(Updater, self).__init__(parent)

        log.info("Creating new Updater for app %s (%s)", app_name, version)

        self._app_name = app_name
        self._version = version
        self._updater_thread = QThread()
        self._copy_worker: CopyWorker
        self._update_available: Optional[bool] = None

    @pyqtSlot(name="start_update")
    def start_update(self) -> None:
        """Start the update check."""
        log.debug("Starting update check.")
        self._update_available = self._check_for_update()
        self.update_available.emit(self._update_available)
        self._check_updater()

    def _check_for_update(self) -> bool:
        """
        Check if an update is available and start the updater if so.

        The function will terminate the application if an update is available.

        See documentation of ´init´ on how to configure the update folder
        itself.
        """
        log.info("Checking for update of application '%s'", self._app_name)

        if check_ide():
            log.info("Application is run from IDE, not running update check.")
            return False

        json_path = os.path.join(LAGER_PATH, self._app_name,
                                 "TSL-UPDATE", "update.json")

        log.debug("Reading update.json from: %s", json_path)

        if not os.path.exists(json_path):
            log.error("Path to json does not exist!")
            return False

        new_version = self._extract_version(json_path)
        log.info("Version available: %s", new_version)
        if new_version != self._version:
            log.debug("Update available for current version: %s", new_version)
            return True
        log.info("No update is available, continuing startup.")
        return False

    @staticmethod
    def _extract_version(path: str) -> str:
        """Extract the version number from the given json file."""
        with open(path) as fhandle:
            json_obj = json.load(fhandle)
        return cast(str, json_obj["version"])

    def _check_updater(self) -> None:
        """Check that the TSL App-Updater is installed and up to date."""
        log.info("Starting check of installation of TSL App-Updater")
        json_file = os.path.join(LAGER_PATH, "TSL-Updater", "update.json")
        install_path = os.path.join(expanduser("~"), "TSL", "Updater")
        self._copy_worker = CopyWorker(install_path, json_file)
        self._copy_worker.moveToThread(self._updater_thread)
        self._updater_thread.started.connect(  # type: ignore
            self._copy_worker.start_copy)
        self._copy_worker.copy_finished.connect(self._updater_thread.quit)
        self._updater_thread.finished.connect(  # type: ignore
            self.check_finished)
        self._updater_thread.start()
        log.info("Copy worker started.")

    @pyqtSlot(name="check_finished")
    def check_finished(self) -> None:
        """Handle that the Updater check is finished."""
        log.info("Updater check finished, Emitting updater_checked")
        self.updater_checked.emit()