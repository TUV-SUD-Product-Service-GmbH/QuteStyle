"""Startup threads."""
from __future__ import annotations

import logging
import re
import urllib
from datetime import datetime
from typing import Tuple, Type

import sqlalchemy
from PyQt5.QtCore import QThread
from sqlalchemy.engine import Engine

from tsl.edoc_database import ENGINE
from tsl.tsl_message_box import TSLMessageBox
from tsl.update_window import AppData

log = logging.getLogger(f"tsl.{__name__}")  # pylint: disable=invalid-name


class StartupThread(QThread):
    """StartupThread base class."""

    START_DEPENDS_ON: Tuple[Type[StartupThread], ...] = ()

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
    def exit_application(self) -> bool:  # pylint: disable=no-self-use
        """Return if the app should call exit_function on thread finished."""
        return False

    def exit_function(self) -> None:
        """Exit function to be called."""


class CheckDBConnectionThread(StartupThread):
    """Thread to check if connection to db is working."""

    def __init__(self, app_data: AppData, engine: Engine):
        """Init connect thread."""
        super().__init__(app_data)
        self._db_conn_state: bool = False
        self._db_conn_error: str = ""
        self._engine = engine
        log.info(
            "Creating DBConnectionThread for app %s version %s engine %s",
            self.app_data.app_name,
            self.app_data.app_version,
            self._engine,
        )

    @property
    def database_name(self) -> str:
        """Get the database name from the ENGINE path."""
        result = re.search(
            r"Database=(.*?);", urllib.parse.unquote(str(self._engine))
        )
        assert result
        return result.group(1)

    def _function_to_execute(self) -> None:
        """Thread run."""
        log.debug("Start db connection check startup thread.")
        try:
            conn = self._engine.connect()
            conn.close()
            self._db_conn_state = True
        except sqlalchemy.exc.OperationalError as err:
            log.exception("Sqlalchemy.exc.OperationalError")
            if "[08001]" in str(err):
                self._db_conn_error = (
                    f"Connection to database {self.database_name} failed.<br>"
                    "Please make sure you are connected to "
                    "TÜV SÜD network."
                )
            else:
                self._db_conn_error = str(err)
        except sqlalchemy.exc.InterfaceError as err:
            log.exception("Sqlalchemy.exc.InterfaceError")
            if "[IM002]" in str(err):
                self._db_conn_error = (
                    "Microsoft® ODBC Driver missing.<br>"
                    "Please contact BSG-IT to install the current "
                    "Microsoft® ODBC Driver."
                )
            else:
                self._db_conn_error = str(err)
        except Exception as exp:  # pylint: disable=broad-except
            log.exception(exp)
            self._db_conn_error = str(exp)

    @property
    def exit_application(self) -> bool:
        """Exit application in case db connection failed."""
        log.debug("Exit application %s", self._db_conn_state)
        return not self._db_conn_state

    def exit_function(self) -> None:
        """Exit function."""
        log.debug("Run exit function.")
        title = f"Error Database connection: {self.database_name}"
        TSLMessageBox.critical(None, title, self._db_conn_error)


class CheckEdocDBConnectionThread(CheckDBConnectionThread):
    """Thread to check if connection to edoc db is working."""

    EXIT_FUNCTION_PRIORITY = 2

    def __init__(self, app_data: AppData):
        """Init connection thread."""
        super().__init__(app_data, ENGINE)
