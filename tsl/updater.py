"""Updater object for updating TSL Apps."""
from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import cast

from tsl.copy_worker import CopyWorker
from tsl.startup_threads import StartupThread
from tsl.update_window import AppData

log = logging.getLogger("tsl.updater")  # pylint: disable=invalid-name

LAGER_PATHS = (
    Path(r"\\DE001.itgr.net\PS\RF-UnitPSMUC\Lager"),
    Path(r"\\DE001.itgr.net\PS\RF-UnitPSFRA\Lager"),
)


class Updater(StartupThread):
    """
    Updater to handle and perform updates for TSL apps.

    The Updater will be given the name and the version where it is used and
    provides information if there is a newer version of the current used app
    available.
    The Updater ensures, that the TSL App-Updater itself is installed and
    up to date. If not up-to-date the updater app is updated.
    """

    # updater has the highest execution priority available
    EXIT_FUNCTION_PRIORITY = 1

    def __init__(self, data: AppData) -> None:
        """Init the Updater."""
        StartupThread.__init__(self, data)
        self._update_available: bool = False

    def _function_to_execute(self) -> None:
        """Start the update."""
        log.debug("Start update thread.")
        try:
            self._update_available = self._check_for_update()
            self._update_updater_app()
        except Exception:  # pylint: disable=broad-except
            log.exception("Exception in %s", self)
            self._update_available = False

    @property
    def exit_application(self) -> bool:
        """Provide info if app should be closed."""
        log.debug("Exit application %s", self._update_available)
        return self._update_available

    def exit_function(self) -> None:
        """Post process code."""
        log.debug("Run exit function.")
        log.info("Update is available. Start updating...")
        subprocess.Popen(  # pylint: disable=consider-using-with
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
                    cast(str, Updater.get_accessible_path()),
                    self.app_data.app_name,
                    "TSL-Update",
                    "update.json",
                ),
            ]
        )

    @staticmethod
    def get_accessible_path() -> Path:
        """Test if update path is readable and return it."""
        for path in LAGER_PATHS:
            if os.access(path, os.R_OK):
                return path
        raise ValueError("Could not find update path")

    def _check_for_update(self) -> bool:
        """
        Check if an update is available and start the updater if so.

        The function will terminate the application if an update is available.

        See documentation of ´init´ on how to configure the update folder
        itself.
        """
        log.info(
            "Checking for update of application '%s'", self.app_data.app_name
        )

        try:
            path = self.get_accessible_path()
        except ValueError:
            # abort update if no accessible path was found
            return False

        json_path = (
            path / self.app_data.app_name / "TSL-UPDATE" / "update.json"
        )
        log.debug("Reading update.json from: %s", json_path)

        if not json_path.exists():
            log.error("Path to json does not exist!")
            return False

        new_version = self._extract_version(json_path)
        log.info("Version available: %s", new_version)
        if new_version != self.app_data.app_version:
            log.debug("Update available for current version: %s", new_version)
            return True
        log.info("No update is available, continuing startup.")
        return False

    @staticmethod
    def _extract_version(path: Path) -> str:
        """Extract the version number from the given json file."""
        with open(path, encoding="utf-8") as fhandle:
            json_obj = json.load(fhandle)
        return cast(str, json_obj["version"])

    def _update_updater_app(self) -> None:
        """
        Check that the TSL App-Updater is installed and up to date.

        If the Updater-App is not up to date it's updated.
        TODO This process is currently not checked for success.
        """
        log.info("Starting check of installation of TSL App-Updater")
        try:
            path = self.get_accessible_path()
        except ValueError:
            # abort update if no accessible path was found
            return
        source_path = path / "TSL-Updater"
        destination_path = Path("~").expanduser() / "TSL" / "Updater"
        log.info(
            "Start update TSL-Updater. Src %s, Dest %s",
            source_path,
            destination_path,
        )
        copy_worker = CopyWorker(destination_path, source_path)
        copy_worker.start_copy()
        log.info("End update TSL-Updater.")
