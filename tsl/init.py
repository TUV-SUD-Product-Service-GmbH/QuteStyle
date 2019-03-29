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

"""

import ctypes
import traceback
from logging import debug, error, getLogger, Formatter, StreamHandler, \
    FileHandler, DEBUG, warning, critical, info
import os
import subprocess
import sys
import winreg


SETTINGS = {
    "log_level": DEBUG
}


def _check_install_update(app_name):
    """
    Check if an update is available and start the updater if so.

    The function will terminate the application if an _check_install_update is
    available.

    See documentation of ´init´ on how to configure the update folder itself.

    :param app_name: <class str> name of the application.
    :return: <class NoneType> None
    """
    debug(f"Checking for _check_install_update of application \"{app_name}\"")
    app_path = os.path.abspath(sys.argv[0])

    if _check_ide():
        debug("Application is run from IDE, not running update check.")
        return

    upd_path = os.path.join("N:\\Lager", app_name, "UPDATE")
    upd_file = os.path.join(upd_path, f"{app_name}.exe")

    if not os.path.exists(upd_file):
        error(f"Could not update app since path {upd_path} does not exist")
        return

    if os.path.getmtime(upd_file) > os.path.getmtime(app_path):
        debug("An updated version of the software is available.")
        ctypes.windll.user32.MessageBoxW(
            0, "Software update available. The Application will be closed, "
               "updated and relaunched automatically.", "Update", 0)
        subprocess.Popen(
            [os.path.join(upd_path, "APPS_UPDATE.exe"), r"/ROOT:" + app_path,
             r"/TEXTFILE:" + os.path.join(upd_path, app_name + ".txt")])
        sys.exit()
    debug("No update is available, continuing startup.")


def _check_ide():
    """
    Check if the application is run from the IDE.

    :return: <class bool> True if run from IDE
    """
    debug("Checking if running from IDE")
    app_path = os.path.abspath(sys.argv[0])
    return not os.path.split(app_path)[1].endswith(".exe")


def _edit_registry_keys(app_name):
    """
    Add or update the registry keys for the application.

    :param app_name: <class str> name of the app
    :return: <class NoneType> None
    """
    if _check_ide():
        debug("Application is run from IDE, not updating registry keys.")
        return

    debug(f"Updating registry keys for {app_name}")
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


def excepthook(cls, exception, trace):
    """
    Override the system except hook to catch PyQt exceptions.

    :param cls: <class class> class of the exception
    :param exception: <class str> exception string
    :param trace: <class traceback> traceback of the exception
    :return: <class NoneType> None
    """
    critical("Critical error occurred:")
    traceback_text = ""
    for line in traceback.format_tb(trace):
        for line_splitted in line.split("\n"):
            if line_splitted:
                traceback_text = traceback_text + line_splitted + "\n"
                critical(line_splitted)
    critical(f"{cls} {exception}")
    try:
        _error_message_box("{}: {}".format(cls, exception), traceback_text)
    except ImportError:
        warning("Not showing error message since PyQt5 is not installed.")


def _error_message_box(error_message, traceb):
    """
    Show an error message box containing the given traceback.

    :param error_message: <class str> Error text
    :param traceb: <class traceback> traceback as string
    :return: <class NoneType> None
    """
    from PyQt5.QtWidgets import QMessageBox
    info("Showing exception message")
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(error_message)
    msg.setInformativeText(traceb)
    msg.setWindowTitle("An error occurred")
    msg.exec()


def _set_excepthook(app_name):
    """
    Set the excepthook to catch PyQt5 exceptions in signals and slots.

    :param app_name: <class str> name of the app
    :return: <class NoneType> None
    """
    debug(f"Setting custom except hook for {app_name}")
    sys.excepthook = excepthook


def _create_logger(app_name):
    """
    Set up the logging environment.

    :param app_name: <class str> name of the app
    :return: <class NoneType> None
    """
    file_name = "logfile.log"
    log = getLogger()  # root logger
    log.setLevel(SETTINGS["log_level"])
    format_str = '%(asctime)s.%(msecs)03d %(threadName)s  - ' \
                 '%(levelname)-8s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    formatter = Formatter(format_str, date_format)
    stream_handler = StreamHandler()
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)

    try:
        os.remove(file_name)
    except PermissionError:
        print(f"Could not get lock on {file_name}, exiting")
        sys.exit(0)
    except FileNotFoundError:
        pass
    file_handler = FileHandler(file_name)
    file_handler.setFormatter(formatter)

    log.addHandler(file_handler)
    debug(f"Successfully initialized logging for {app_name}")


ARGUMENTS = {
    "logging": _create_logger,
    "excepthook": _set_excepthook,
    "registry": _edit_registry_keys,
    "update": _check_install_update,
}


def init(app_name, **kwargs):
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

    # normalize the app_name just in case.
    app_name = app_name.lower()

    debug(f"Initializing application {app_name} with:")
    for key, parameter in kwargs.items():
        debug(f"Key '{key}': {parameter}")

    for key, func in ARGUMENTS.items():
        if key in kwargs and kwargs[key]:
            func(app_name)
