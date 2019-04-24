"""
TSL Library - helper: useful functions for TSL tools.

Public methods:
- get_correct_pse_path: Search for the project folder based on a id.
- encode_pixmap: Encode a QPixmap to a Base64 str.
- decode_pixmap: Decode a QPixmap from a Base64 str.
- get_project_path: Search for the project folder based on the given id.
- get_process_path: Search for the process folder based on the given id.
- create_path_map: Create a map of ians and paths.
"""
import re
from datetime import date
from logging import info
import os

from PyQt5.QtCore import QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QPixmap

PATH = r"\\de001.itgr.net\PS\RF-UnitCentralPS_PSE\CPS"


def encode_pixmap(pixmap):
    """
    Encode a QPixmap to a Base64 str.

    :param pixmap: <class QPixmap> pixmap to be stored
    :return: <class str> Base64 string
    """
    byte_array = QByteArray()
    buffer = QBuffer(byte_array)
    buffer.open(QIODevice.WriteOnly)
    pixmap.save(buffer, "png")
    return byte_array.toBase64().data().decode("utf-8")


def decode_pixmap(pixmap_string):
    """
    Decode a QPixmap from a Base64 str.

    :param pixmap_string: <class str> Base64 string
    :return: <class QPixmap> extracted pixmap
    """
    byte_array = QByteArray.fromBase64(pixmap_string.encode("utf-8"))
    qpixmap = QPixmap()
    qpixmap.loadFromData(byte_array)
    return qpixmap


def get_project_path(project_id):
    """
    Search for the project folder based on an id.

    This is a convenience function for backwards compatibility of
    get_path_for_id with id_type "project".

    :param project_id: <class int> pse number as int
    :raises ValueError: if no path was found for given id
    :return: <class str> path for project
    """
    return get_path_for_id(project_id, "project")


def get_process_path(process_id):
    """
    Search for the process folder based on an id.

    This is a convenience function for backwards compatibility of
    get_path_for_id with id_type "process".

    :param process_id: <class int> pse number as int
    :raises ValueError: if no path was found for given id
    :return: <class str> path for process.
    """
    return get_path_for_id(process_id, "process")


def get_path_for_id(ident, id_type):
    """
    Get the project path for the given id and type.

    :param ident: <class int> process or project number
    :param id_type: <class str> type of project ("process", "project")
    :raises ValueError: if no path was found for given id
    :return: <class tr> path for id
    """
    info(f"Searching correct path for {id_type} id %s", ident)
    year = date.today().year

    for i in range(0, year - 2000):
        path_type = {"process": "PSEX\\Prozesse",
                     "project": "Projects"}[id_type]
        path = os.path.join(os.path.join(PATH, path_type), str(year - i))
        if os.path.exists(path):
            id_path = os.path.join(path, str(ident))
            if os.path.exists(id_path):
                info(f"Found {id_type} path {id_path}")
                return id_path

    raise ValueError(f"No path found for {id_type} id {ident}")


def create_path_map():
    """
    Create a map of ians and paths.

    :return: <class dict> ians with their respective paths
    """
    # there is not better way doing this, an extra function also makes no sense
    # pylint: disable=too-many-nested-blocks
    paths = {}
    for i in range(2):
        path = os.path.join(os.path.join(PATH, "Prozesse"),
                            str(date.today().year - i))

        # create a list of all folders sorted by their INODE number
        folders = [(folder, os.stat(os.path.join(path, folder)).st_ino)
                   for folder in os.listdir(path)]
        folders.sort(key=lambda x: x[1])

        for fold in folders:
            try:
                for file in os.listdir(os.path.join(path, fold[0], "SPEC")):
                    if re.search("_PA_Stand", file) or \
                            re.search("_Anlage EAN-Codes", file):
                        try:
                            paths[int(file[:6])] = fold[0]
                            break
                        except ValueError:
                            continue
            except FileNotFoundError:
                continue
    return paths
