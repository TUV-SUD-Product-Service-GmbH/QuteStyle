"""Development functions."""
import ntpath
import os
import subprocess
import sys
from typing import List

from PyQt5 import uic


def compile_ui_files(src_folders: List[str]) -> None:
    """
    Compile the ui files.

    Compile the ui files in src_folders and copy the created
    files to gen folder.
    """
    for folder in src_folders:
        for file in os.listdir(folder):
            print("Converting file {}".format(file))
            new_file = "ui_" + file.replace(".ui", "") + ".py"
            with open(os.path.join(folder, file), "r") as source:
                with open(
                    os.path.join(os.path.dirname(folder), "gen", new_file), "w"
                ) as target:
                    uic.compileUi(source, target)
        # run black after ui files are created
        subprocess.run(
            [
                os.path.join(ntpath.split(sys.executable)[0], "black"),
                "-l79",
                os.path.join(os.path.dirname(folder), "gen"),
            ],
            check=False,
        )
    print("Conversion finished")
