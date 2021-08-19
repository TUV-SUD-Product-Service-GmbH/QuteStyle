"""Convert every ui-file in tsl/ui to a py-file in tsl/gen."""
import os

from tsl.dev.dev_functions import compile_ui_files

if __name__ == "__main__":
    if "dev_scripts" in os.getcwd():
        os.chdir(os.getcwd().replace("dev_scripts", ""))
    compile_ui_files([os.path.join("tsl", "ui")])
