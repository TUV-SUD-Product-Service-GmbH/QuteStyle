"""Convert every ui-file in qute_style/ui to a py-file in qute_style/gen."""
import os
from pathlib import Path

from qute_style.dev.dev_functions import compile_ui_files

if __name__ == "__main__":
    if Path.cwd().stem == "dev_scripts":
        os.chdir(Path.cwd().parent)
    compile_ui_files([Path("qute_style") / "ui"])
