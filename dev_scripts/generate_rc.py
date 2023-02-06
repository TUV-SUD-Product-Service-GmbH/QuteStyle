"""Script to compile resources into python file."""
import os
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path

if __name__ == "__main__":
    if Path.cwd().stem == "dev_scripts":
        os.chdir(Path.cwd().parent)

    ROOT = Path.cwd() / "qute_style"
    RCS = ROOT / "resources"
    QRC_FILE = RCS / "resources.qrc"
    DIRS = list(RCS.iterdir())

    QRC_FILE.unlink(missing_ok=True)

    print("Creating new resources.qrc")

    RCC = ET.Element("RCC")
    QRC = ET.SubElement(RCC, "qresource")
    for folder in DIRS:
        for file in folder.iterdir():
            relative_path = file.relative_to(RCS).as_posix()
            ET.SubElement(QRC, "file").text = str(relative_path)

    TREE = ET.ElementTree(RCC)
    TREE.write(QRC_FILE)

    print("Generating resource_rc.py with new resources.qrc")
    assert (
        subprocess.call(
            ["pyside6-rcc", "-o", ROOT / "resources_rc.py", QRC_FILE]
        )
        == 0
    )

    print("Deleting resources.qrc")
    QRC_FILE.unlink(missing_ok=False)
