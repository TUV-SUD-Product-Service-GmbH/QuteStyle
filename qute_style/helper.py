"""QuteStyle Library - helper: useful functions for QuteStyle tools."""
import logging
import sys
from pathlib import Path
from typing import Union, cast
from xml.etree.ElementTree import Element, SubElement, tostring

from PySide6.QtCore import QBuffer, QByteArray, QIODevice, QObject
from PySide6.QtGui import QColor, QPaintEvent, QPixmap

from qute_style.style import get_color
from qute_style.widgets.spinner import WaitingSpinner

log = logging.getLogger("qute_style")


def check_ide() -> bool:
    """Check if the application is run from the IDE."""
    return Path(sys.argv[0]).suffix == ".py"


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


class StyledWaitingSpinner(WaitingSpinner):
    """Styled Version of QWaitingSpinner."""

    def paintEvent(self, _: QPaintEvent) -> None:
        """Overwrite method to change color of spinner."""
        self._color = QColor(get_color("context_color"))
        super().paintEvent(_)


def create_waiting_spinner(
    parent: QObject,
    number_of_lines: int = 28,
    line_length: int = 20,
    inner_radius: int = 15,
) -> StyledWaitingSpinner:
    """Create a waiting spinner with default config."""
    spinner = StyledWaitingSpinner(parent)
    spinner.color = get_color("context_color")
    spinner.number_of_lines = number_of_lines
    spinner.line_length = line_length
    spinner.inner_radius = inner_radius
    spinner.line_width = 2
    return spinner


def create_tooltip(title: str, description: Union[str, list[str]]) -> str:
    """Create a tooltip as HTML str."""
    top = Element("div")
    first = SubElement(top, "p")
    headline = SubElement(first, "b")
    headline.text = title
    second = SubElement(top, "p")
    text = SubElement(second, "small")
    if isinstance(description, str):
        text.text = description
    else:
        text.text = "<br />".join(description)
    return tostring(top).decode("utf-8")
