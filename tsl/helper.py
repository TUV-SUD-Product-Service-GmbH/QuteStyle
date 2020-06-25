"""TSL Library - helper: useful functions for TSL tools."""
from datetime import date
import logging
import os
from typing import Dict

from PyQt5.QtCore import QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QPixmap

PATH = r"\\de001.itgr.net\PS\RF-UnitCentralPS_PSE\CPS"

MEMO: Dict[str, Dict[int, str]] = {"process": {}, "project": {}}

log = logging.getLogger("tsl")  # pylint: disable=invalid-name


def encode_pixmap(pixmap: QPixmap) -> str:
    """Encode a QPixmap to a Base64 str."""
    byte_array = QByteArray()
    buffer = QBuffer(byte_array)
    buffer.open(QIODevice.WriteOnly)
    pixmap.save(buffer, "png")
    return byte_array.toBase64().data().decode("utf-8")


def decode_pixmap(pixmap_string: str) -> QPixmap:
    """Decode a QPixmap from a Base64 str."""
    byte_array = QByteArray.fromBase64(pixmap_string.encode("utf-8"))
    qpixmap = QPixmap()
    qpixmap.loadFromData(byte_array)
    return qpixmap


def get_project_path(project_id: int) -> str:
    """
    Search for the project folder based on an id.

    This is a convenience function for backwards compatibility of
    get_path_for_id with id_type "project".
    """
    return get_path_for_id(project_id, "project")


def get_process_path(process_id: int) -> str:
    """
    Search for the process folder based on an id.

    This is a convenience function for backwards compatibility of
    get_path_for_id with id_type "process".
    """
    return get_path_for_id(process_id, "process")


def get_path_for_id(ident: int, id_type: str) -> str:
    """Get the project path for the given id and type."""
    log.info("Searching correct path for %s id %s", id_type, ident)
    year = date.today().year

    try:
        log.info("Trying to returned cached entry.")
        return MEMO[id_type][ident]
    except KeyError:
        for i in range(0, year - 2000):
            path_type = {"process": "PSEX\\Prozesse",
                         "project": "Projects"}[id_type]
            path = os.path.join(os.path.join(PATH, path_type), str(year - i))
            if os.path.exists(path):
                id_path = os.path.join(path, str(ident))
                if os.path.exists(id_path):
                    log.info("Found %s path %s", id_type, id_path)
                    MEMO[id_type][ident] = id_path
                    return id_path

    raise ValueError(f"No path found for {id_type} id {ident}")
