# -*- coding: utf-8 -*-
r"""
TSL Library - init: providing functions needed on application startup.

The init module will run functions on application start that are needed for
several TSL applications.

To use this library in your software project import the function ´ínit´ and
call it with your application name and the keywords needed.

To used any of the following sub-functions define the documented keyword as a
bool value with value ´True´:

key registry: Update the application's registry keys for use in PSE-Assistant.
key logging: Initialize logging to log output to the stdout stream and also
             to a file "logfile.log" in the project folder. To configure
             logging, import SETTINGS. The following values can be set:
             - log_level: log level from logging module (default: DEBUG)
             - full_log: log everything, also logs from 3rd-party modules
"""

import logging
import os
import sys
import traceback
import winreg
from types import TracebackType
from typing import Type, TypedDict, TypeVar

from PyQt5.QtCore import (
    QMessageLogContext,
    QtCriticalMsg,
    QtFatalMsg,
    QtInfoMsg,
    QtMsgType,
    QtWarningMsg,
    qInstallMessageHandler,
)
from PyQt5.QtWidgets import QMessageBox

from tsl.version import VERSION

log = logging.getLogger("tsl")  # pylint: disable=invalid-name


class SettingsDict(TypedDict):
    """Type definition for settings dictionary."""

    log_level: int
    full_log: bool
    name_log: str


SETTINGS = SettingsDict(
    log_level=logging.DEBUG, full_log=False, name_log="logfile.log"
)


def check_ide() -> bool:
    """Check if the application is run from the IDE."""
    log.info("Checking if running from IDE")
    app_path = os.path.abspath(sys.argv[0])
    return not os.path.split(app_path)[1].endswith(".exe")


def edit_registry_keys(app_name: str) -> None:
    """Add or update the registry keys for the application."""
    if check_ide():
        log.info("Application is run from IDE, not updating registry keys.")
        return

    log.info("Updating registry keys for %s", app_name)
    data = {
        os.path.join("Software", app_name): os.path.abspath(sys.argv[0]),
        os.path.join("Software", "TÜV SÜD", app_name): os.path.split(
            os.path.abspath(sys.argv[0])
        )[0],
    }
    for key, value in data.items():
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, key)
        registry_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_WRITE
        )
        winreg.SetValueEx(
            registry_key, "ApplicationPath", 0, winreg.REG_SZ, value
        )
        winreg.CloseKey(registry_key)

ExceptionT = TypeVar("ExceptionT", bound=BaseException)


def excepthook(
    cls: Type[ExceptionT], exception: ExceptionT, trace: TracebackType
) -> None:
    """Override the system except hook to catch PyQt exceptions."""
    log.critical("Critical error occurred:")
    traceback_text = ""
    for line in traceback.format_tb(trace):
        for line_splitted in line.split("\n"):
            if line_splitted:
                traceback_text = traceback_text + line_splitted + "\n"
                log.critical(line_splitted)
    log.critical("%s %s", cls, exception)
    try:
        error_message_box(f"{cls}: {exception}", traceback_text)
    except ImportError:
        log.warning("Not showing error message since PyQt is not installed.")


def error_message_box(error_message: str, traceb: str) -> None:
    """Show an error message box containing the given traceback."""
    try:
        log.info("Showing exception message")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error_message)
        msg.setInformativeText(traceb)
        msg.setWindowTitle("An error occurred")
        msg.exec()
    except NameError:
        log.info("PyQt is not installed, not showing exception message")


def set_excepthook(app_name: str) -> None:
    """Set the excepthook to catch PyQt exceptions in signals and slots."""
    log.info("Setting custom except hook for %s", app_name)
    sys.excepthook = excepthook


def create_logger(app_name: str) -> None:
    """
    Set up the logging environment.

    If SETTINGS["full_log"] is set to True, the function will configure the
    root logger to send its log to our logfile and to the stdout. Otherwise,
    only the application logs are send.

    The function will configure the log level according to SETTINGS["level"].
    """
    format_str = (
        "%(asctime)s.%(msecs)03d %(threadName)10s  - "
        "%(name)-50s - %(funcName)-25s:%(lineno)-4s - "
        "%(levelname)-8s - %(message)s"
    )
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(format_str, date_format)

    try:
        os.remove(SETTINGS["name_log"])
    except PermissionError:
        print(f"Could not get lock on {SETTINGS['name_log']}, exiting")
        sys.exit(0)
    except FileNotFoundError:
        pass

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    file_handler = logging.FileHandler(SETTINGS["name_log"], "w", "utf-8")
    file_handler.setFormatter(formatter)

    if SETTINGS["full_log"]:
        loggers = [logging.getLogger(), log]  # root logger
    else:
        loggers = [logging.getLogger(app_name), log]  # app specific logger

    for logger in loggers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        logger.setLevel(SETTINGS["log_level"])

    log.info("Configuring Qt message handler")
    try:
        qInstallMessageHandler(qt_message_handler)
    except NameError:
        log.info("PyQt is not installed, not configuring Qt message handler")
    log.info("Successfully initialized logging for '%s'", app_name)
    log.info("TSL-Library version %s", VERSION)


def qt_message_handler(
    mode: QtMsgType, context: QMessageLogContext, message: str
) -> None:
    """Handle a Qt log message and write it to python logging."""
    if mode == QtInfoMsg:
        level = logging.INFO
    elif mode == QtWarningMsg:
        level = logging.WARNING
    elif mode == QtCriticalMsg:
        level = logging.CRITICAL
    elif mode == QtFatalMsg:
        level = logging.FATAL
    else:
        level = logging.DEBUG
    msg = f"{context.file}:{context.line}:{context.function} - {message}"
    log.log(level, msg)


def init(
    app_name: str,
    logs: bool = False,
    registry: bool = False,
    hook: bool = False,
) -> None:
    """
    Init the application and setup different TSL specific functions.

    The following keywords are evaluated for execution of different functions:
    - logs: Configure logging
    - registry: Update the registry keys of the app
    - hook: Install a custom excepthook for catching Qt exceptions
    """
    # check that an app_name is given (i.e. not "") and that it is a str
    assert app_name and isinstance(app_name, str)

    if logs:
        create_logger(app_name)
        log.info("Initializing application %s:", app_name)

    if registry:
        edit_registry_keys(app_name)

    if hook:
        set_excepthook(app_name)
