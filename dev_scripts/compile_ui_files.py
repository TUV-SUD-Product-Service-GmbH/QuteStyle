"""
This script automatically converts every ui-file in views/ui to a py-file in views/gen
"""
import os
from PyQt5 import uic


if __name__ == "__main__":
    path = os.getcwd().replace("dev_scripts", "")
    os.chdir(path)
    for file in os.listdir(os.path.join("tsl", "ui")):
        print("Converting file {}".format(file))
        new_file = "ui_" + file.replace(".ui", "") + ".py"
        with open(os.path.join("tsl", "ui", file), "r") as source:
            with open(os.path.join("tsl", "gen", new_file), "w") as target:
                uic.compileUi(source, target)
    print("Conversion finished")
