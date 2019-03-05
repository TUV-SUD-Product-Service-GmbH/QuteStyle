from datetime import date
from logging import debug
import os

from PyQt5.QtCore import QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QPixmap

from library import settings


def get_correct_pse_path(number):
    """
    Searches for the correct project folder based on the given number
    :param number: <class int> pse number as int
    :return: <class str> path for project. path is empty if not found
    """
    debug("Searching correct path for project number %s", number)
    year = date.today().year

    for i in range(0, year-2000):
        # Todo: make a setting for this
        path = os.path.join(settings.PATH, str(year-i))
        if os.path.exists(path):
            project_path = os.path.join(path, str(number))
            if os.path.exists(project_path):
                debug(f"Returning pse path: {project_path}")
                return project_path

    return ""


def encode_pixmap(pixmap):
    """
    Encodes a QPixmap object so that it can be stored within a json file
    :param pixmap: <class QPixmap> pixmap to be stored
    :return: <class str> Base64 string
    """
    byte_array = QByteArray()
    buffer = QBuffer(byte_array)
    buffer.open(QIODevice.WriteOnly)
    pixmap.save(buffer, "png")
    return byte_array.toBase64().data().decode("utf-8")


def decode_pixmap(string):
    """
    Decodes a base64 string and extracts the QPixmap
    :param pixmap: <class str> Base64 string
    :return: <class QPixmap> extracted pixmap
    """
    byte_array = QByteArray.fromBase64(string.encode("utf-8"))
    qpixmap = QPixmap()
    qpixmap.loadFromData(byte_array)
    return qpixmap
