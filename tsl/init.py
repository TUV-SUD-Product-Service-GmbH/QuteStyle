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
from logging import debug
import os
import subprocess
import sys
import winreg


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


ARGUMENTS = {
    "registry": _edit_registry_keys,
    "update": _check_install_update
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
