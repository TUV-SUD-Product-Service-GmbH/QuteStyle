"""Convert every ui-file in tsl/ui to a py-file in tsl/gen."""
import os
from pathlib import Path

from tsl.dev.dev_functions import compile_ui_files

if __name__ == "__main__":
    if Path.cwd().stem == "dev_scripts":
        os.chdir(Path.cwd().parent)
    compile_ui_files([Path("tsl") / "ui"])
