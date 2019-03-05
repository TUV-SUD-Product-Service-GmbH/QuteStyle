import os
import sys
import winreg
import subprocess
import datetime
import ctypes
import time


def update(app_name):
    """"
    In order for the auto-update function to work correctly. Follow the
    instructions:
    under: N:/Lager/App_name/UPDATE. Following files will be needed
    1 - The latest built exe  (App_name.exe)
    2 - The APPS.UPDATE.exe
    """
    AppPath = os.path.abspath(sys.argv[0])
    head, tail = os.path.split(AppPath)
    extension = tail.split(".")
    if extension[1] == "exe":  # Don't auto update on IDE
        winreg.CreateKey(winreg.HKEY_CURRENT_USER,
                         os.path.join("Software", app_name))
        registry_key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            os.path.join("Software", app_name),
            0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key,
                          "ApplicationPath", 0,
                          winreg.REG_SZ, AppPath)
        winreg.CloseKey(registry_key)
        REG_PATH2 = os.path.join("Software", "TÜV SÜD", app_name)
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH2)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                      REG_PATH2, 0,
                                      winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key,
                          "ApplicationPath", 0,
                          winreg.REG_SZ, head)
        winreg.CloseKey(registry_key)
        server_path_time = time.ctime(
            os.path.getmtime(os.path.join(
                "N:", "Lager", app_name, "UPDATE", app_name + ".exe")))
        serverpathtime = datetime.datetime.strptime(
            server_path_time, '%a %b %d %H:%M:%S %Y')
        local_path_time = time.ctime(os.path.getmtime(AppPath))
        localpathtime = datetime.datetime.strptime(
            local_path_time, '%a %b %d %H:%M:%S %Y')
        if serverpathtime > localpathtime:
            ctypes.windll.user32.MessageBoxW(
                0, "Softwareupdate available. The Application will be closed, "
                   "updateted and relaunched automatically.",
                "Update", 0)
            subprocess.Popen(
                [os.path.join(
                    "N:", "Lager", app_name, "UPDATE", "APPS_UPDATE.exe"),
                 r"/ROOT:" + AppPath,
                 r"/TEXTFILE:" + os.path.join(
                 "N:", "Lager", app_name, "UPDATE", app_name + ".txt")])
            sys.exit()
