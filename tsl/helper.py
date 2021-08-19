"""TSL Library - helper: useful functions for TSL tools."""
import logging
import os
from typing import cast

from PyQt5.QtCore import QBuffer, QByteArray, QIODevice
from PyQt5.QtGui import QPixmap
from sqlalchemy.orm.exc import NoResultFound

from tsl.pse_database import AdminSession, Process, Project
from tsl.variables import PATH

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
    byte_array = QByteArray.fromBase64(
        cast(QByteArray, pixmap_string.encode("utf-8"))
    )
    qpixmap = QPixmap()
    qpixmap.loadFromData(byte_array)
    return qpixmap


def get_project_path(project_id: int) -> str:
    """Search for the project folder based on an id."""
    log.info("Searching correct path for project id %s", project_id)
    session = AdminSession()
    try:
        project = (
            session.query(Project)
            .filter(Project.P_ID == project_id)
            .filter(Project.P_WC_ID == "BB8E7738-0ACB-423C-8626-18AA3355B8FF")
            .one()
        )
        log.debug("Got project: %s", project)
        return os.path.join(PATH, project.P_FOLDER)
    except NoResultFound as no_result_found:
        raise ValueError(
            f"No path found for project id {project_id}"
        ) from no_result_found
    finally:
        session.close()


def get_process_path(process_id: int) -> str:
    """Search for the process folder based on an id."""
    log.info("Searching correct path for process id %s", process_id)
    session = AdminSession()
    try:
        process = (
            session.query(Process).filter(Process.PC_ID == process_id).one()
        )
        log.debug("Got process: %s", process)
        return os.path.join(PATH, "PSEX", process.PC_PATH)
    except NoResultFound as no_result_found:
        raise ValueError(
            f"No path found for process id {process_id}"
        ) from no_result_found
    finally:
        session.close()
