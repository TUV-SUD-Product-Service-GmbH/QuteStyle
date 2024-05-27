"""Startup threads."""

from __future__ import annotations

import logging
from datetime import datetime

from PySide6.QtCore import QThread

from qute_style.qs_main_window import AppData

log = logging.getLogger(
    f"qute_style.{__name__}"
)  # pylint: disable=invalid-name


class StartupThread(QThread):
    """StartupThread base class."""

    START_DEPENDS_ON: tuple[type[StartupThread], ...] = ()

    # Each startup thread must have a unique priority for its exit function.
    # The exit function of the thread with the lowest priority is executed
    # first in case there are more than one finished threads at the same time
    EXIT_FUNCTION_PRIORITY: int = 0

    def __init__(self, app_data: AppData):
        """Startupthread init function."""
        super().__init__(None)
        self.app_data = app_data
        log.info(
            "Creating %s for app %s version %s",
            self.__class__,
            self.app_data.app_name,
            self.app_data.app_version,
        )

    def run(self) -> None:
        """Thread run."""
        start_time = datetime.now()
        self._function_to_execute()
        log.debug(
            "Time taken %s: %s", self.__class__, datetime.now() - start_time
        )

    def _function_to_execute(self) -> None:
        """Thread function. Must be implemented by subclasses."""
        raise NotImplementedError  # pragma: no cover

    @property
    def exit_application(self) -> bool:
        """Return if the app should call exit_function on thread finished."""
        return False

    def exit_function(self) -> None:
        """Exit function to be called."""
