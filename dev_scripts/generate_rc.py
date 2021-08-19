"""Script to compile resources into python file."""

import os
import subprocess
import xml.etree.cElementTree as ET

if __name__ == "__main__":

    try:
        os.remove("../tsl/resources/resources.qrc")

    except FileNotFoundError:
        pass

    DIR_NAME = "resources"
    ROOT = os.getcwd().replace("dev_scripts", "tsl")
    RCS = os.path.join(ROOT, DIR_NAME)
    DIRS = os.listdir(RCS)

    print("Creating new resources.qrc")

    RCC = ET.Element("RCC")
    QRC = ET.SubElement(RCC, "qresource")
    for folder in DIRS:
        folder_path = os.path.join(RCS, folder)
        files = os.listdir(folder_path)
        for file in files:
            ET.SubElement(QRC, "file").text = os.path.join(folder, file)

    TREE = ET.ElementTree(RCC)
    TREE.write("../tsl/resources/resources.qrc")

    print("Generating resource_rc.py with new resources.qrc")
    assert (
        subprocess.call(
            "PyRCC5 -o ../tsl/resources_rc.py "
            "../tsl/resources/resources.qrc"
        )
        == 0
    )

    print("Deleting resources.qrc")
    os.remove("../tsl/resources/resources.qrc")
