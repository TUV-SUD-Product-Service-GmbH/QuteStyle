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
key update: Check if an update is available for the application.
            If an update is available, the function will open the updater and
            exit the application.  An update will be detected, if a newer
            version of the application's executable is available in folder
            "N:\Lager\{app_name}\UPDATE". If more than the executable needs
            to be copied, one must provide a "{app_name}.txt" file that
            contains the paths to the additional files like this:
            ___________________________________________
            [FILES TO BE UPDATED IN THE UPDATE FOLDER]
            base_library.zip
            ...
            ___________________________________________
key logging: Initialize logging to log output to the stdout stream and also
             to a file "logfile.log" in the project folder. To configure
             logging, import SETTINGS. The following values can be set:
             - log_level: log level from logging module (default: DEBUG)
             - full_log: log everything, also logs from 3rd-party modules
"""

import logging
import traceback
import os
import sys
import winreg
from typing import Callable, Dict

from tsl.version import VERSION


log = logging.getLogger("tsl")  # pylint: disable=invalid-name

SETTINGS = {
    "log_level": logging.DEBUG,
    "full_log": False
}


def check_ide() -> bool:
    """
    Check if the application is run from the IDE.

    :return: <class bool> True if run from IDE
    """
    log.info("Checking if running from IDE")
    app_path = os.path.abspath(sys.argv[0])
    return not os.path.split(app_path)[1].endswith(".exe")


def _edit_registry_keys(app_name: str) -> None:
    """
    Add or update the registry keys for the application.

    :param app_name: <class str> name of the app
    :return: <class NoneType> None
    """
    if check_ide():
        log.info("Application is run from IDE, not updating registry keys.")
        return

    log.info("Updating registry keys for %s", app_name)
    data = {
        os.path.join("Software", app_name): os.path.abspath(sys.argv[0]),
        os.path.join("Software", "TÜV SÜD", app_name):
            os.path.split(os.path.abspath(sys.argv[0]))[0]
    }
    for key, value in data.items():
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, key)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0,
                                      winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, "ApplicationPath", 0, winreg.REG_SZ,
                          value)
        winreg.CloseKey(registry_key)


def excepthook(cls: Callable, exception: Exception,
               trace: traceback  # type: ignore
               ) -> None:
    """
    Override the system except hook to catch PyQt exceptions.

    :param cls: <class class> class of the exception
    :param exception: <class str> exception string
    :param trace: <class traceback> traceback of the exception
    :return: <class NoneType> None
    """
    log.critical("Critical error occurred:")
    traceback_text = ""
    for line in traceback.format_tb(trace):
        for line_splitted in line.split("\n"):
            if line_splitted:
                traceback_text = traceback_text + line_splitted + "\n"
                log.critical(line_splitted)
    log.critical("%s %s", cls, exception)
    try:
        _error_message_box("{}: {}".format(cls, exception), traceback_text)
    except ImportError:
        log.warning("Not showing error message since PyQt5 is not installed.")


def _error_message_box(error_message: str, traceb: str) -> None:
    """
    Show an error message box containing the given traceback.

    :param error_message: <class str> Error text
    :param traceb: <class traceback> traceback as string
    :return: <class NoneType> None
    """
    try:
        # pylint: disable=import-outside-toplevel
        from PyQt5.QtWidgets import QMessageBox
        log.info("Showing exception message")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(error_message)
        msg.setInformativeText(traceb)
        msg.setWindowTitle("An error occurred")
        msg.exec()
    except ModuleNotFoundError:
        log.info("PyQt5 is not installed, not showing exception message")


def _set_excepthook(app_name: str) -> None:
    """
    Set the excepthook to catch PyQt5 exceptions in signals and slots.

    :param app_name: <class str> name of the app
    :return: <class NoneType> None
    """
    log.info("Setting custom except hook for %s", app_name)
    sys.excepthook = excepthook  # type: ignore


def _create_logger(app_name: str) -> None:
    """
    Set up the logging environment.

    If SETTINGS["full_log"] is set to True, the function will configure the
    root logger to send its log to our logfile and to the stdout. Otherwise,
    only the application logs are send.

    The function will configure the log level according to SETTINGS["level"].
    """
    format_str = '%(asctime)s.%(msecs)03d %(threadName)10s  - ' \
                 '%(name)-50s - %(funcName)-25s:%(lineno)-4s - ' \
                 '%(levelname)-8s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(format_str, date_format)

    file_name = "logfile.log"
    try:
        os.remove(file_name)
    except PermissionError:
        print(f"Could not get lock on {file_name}, exiting")
        sys.exit(0)
    except FileNotFoundError:
        pass

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    file_handler = logging.FileHandler(file_name, "w", "utf-8")
    file_handler.setFormatter(formatter)

    if SETTINGS["full_log"]:
        loggers = [logging.getLogger(), log]  # root logger
    else:
        loggers = [logging.getLogger(app_name), log]  # app specific logger

    for logger in loggers:
        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)
        logger.setLevel(SETTINGS["log_level"])

    log.info("Successfully initialized logging for '%s'", app_name)
    log.info("TSL-Library version %s", VERSION)


ARGUMENTS = {
    "excepthook": _set_excepthook,
    "registry": _edit_registry_keys,
}


def init(app_name: str, **kwargs: Dict[str, bool]) -> None:
    """
    Init the application and setup different TSL specific functions.

    The following keywords are evaluated for execution of different functions:
    - registry: Update the registry keys of the app
    - update: Check of an application update

    :param app_name: <class str> name of the application.
    :param kwargs: <class dict> keyword arguments.
    :return: <class NoneType> None
    """
    # check that an app_name is given (i.e. not "") and that it is a str
    assert app_name and isinstance(app_name, str)

    if "logging" in kwargs and kwargs["logging"]:
        _create_logger(app_name)

    log.info("Initializing application %s with:", app_name)
    for key, parameter in kwargs.items():
        log.info("Key '%s': %s", key, parameter)

    for key, func in ARGUMENTS.items():
        if key in kwargs and kwargs[key]:
            func(app_name)
