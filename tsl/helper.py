"""TSL Library - helper: useful functions for TSL tools."""
import errno
import logging
from pathlib import Path
from typing import Optional, cast
from winreg import HKEY_CURRENT_USER, KEY_READ, OpenKey, QueryValueEx

from PyQt5.QtCore import QBuffer, QByteArray, QIODevice
from PyQt5.QtGui import QPixmap
from sqlalchemy.orm.exc import NoResultFound

from tsl.edoc_database import AdminSession, Process, Project

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


def get_project_path(project_id: int) -> Path:
    """Search for the project folder based on an id."""
    log.info("Searching correct path for project id %s", project_id)
    session = AdminSession()
    try:
        project: Project = (
            session.query(Project)
            .filter(Project.P_ID == project_id)
            .filter(Project.P_WC_ID == "BB8E7738-0ACB-423C-8626-18AA3355B8FF")
            .one()
        )
        log.debug("Got project: %s", project)
        return project.project_folder
    except NoResultFound as no_result_found:
        raise ValueError(
            f"No path found for project id {project_id}"
        ) from no_result_found
    finally:
        session.close()


def get_process_path(process_id: int) -> Path:
    """Search for the process folder based on an id."""
    log.info("Searching correct path for process id %s", process_id)
    session = AdminSession()
    try:
        process: Process = (
            session.query(Process).filter(Process.PC_ID == process_id).one()
        )
        log.debug("Got process: %s", process)
        return process.process_archive
    except NoResultFound as no_result_found:
        raise ValueError(
            f"No path found for process id {process_id}"
        ) from no_result_found
    finally:
        session.close()


def get_selected_psex_id() -> Optional[int]:
    """Get the id of the currently selected project in PSExplorer."""
    key = OpenKey(HKEY_CURRENT_USER, r"Software\TUV\PSExplorer", 0, KEY_READ)
    try:
        project_id = QueryValueEx(key, "SelectedProjectId")[0]
        log.debug("Selected PSEX-ID is %s", project_id)
        return int(project_id) if project_id else None
    except OSError as error:
        if error.errno == errno.ENOENT:
            log.debug("Key does not exist.")
            return None
        raise
    finally:
        key.Close()
