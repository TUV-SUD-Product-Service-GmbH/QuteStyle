"""QuteStyle Library - helper: useful functions for QuteStyle tools."""
import logging
import sys
from pathlib import Path
from typing import List, Union, cast
from xml.etree.ElementTree import Element, SubElement, tostring

from PyQt5.QtCore import QBuffer, QByteArray, QIODevice, QObject, QRectF, Qt
from PyQt5.QtGui import QPainter, QPaintEvent, QPixmap
from pyqtspinner.spinner import WaitingSpinner

from qute_style.style import get_color

log = logging.getLogger("qute_style")  # pylint: disable=invalid-name


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

    def updateTimer(self):
        """Overwrite updateTime in order to deal with float."""
        self._timer.setInterval(
            int(1000 / (self._numberOfLines * self._revolutionsPerSecond))
        )

    def updatePosition(self):
        """Overwrite updatePosition in order to deal with float."""
        if self.parentWidget() and self._centerOnParent:
            self.move(
                int(self.parentWidget().width() / 2 - self.width() / 2),
                int(self.parentWidget().height() / 2 - self.height() / 2),
            )

    def paintEvent(  # pylint: disable=invalid-name, arguments-renamed
        self, _: QPaintEvent
    ) -> None:
        """Overwrite method to change color of spinner."""
        self.setColor(get_color("context_color"))
        self.updatePosition()
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.transparent)
        painter.setRenderHint(QPainter.Antialiasing, True)

        if self._currentCounter >= self._numberOfLines:  # type: ignore
            self._currentCounter = 0

        painter.setPen(Qt.NoPen)
        for i in range(self._numberOfLines):
            painter.save()
            painter.translate(
                self._innerRadius + self._lineLength,
                self._innerRadius + self._lineLength,
            )
            rotateAngle = float(360 * i) / float(self._numberOfLines)
            painter.rotate(rotateAngle)
            painter.translate(self._innerRadius, 0)
            distance = self.lineCountDistanceFromPrimary(
                i, self._currentCounter, self._numberOfLines
            )
            color = self.currentLineColor(
                distance,
                self._numberOfLines,
                self._trailFadePercentage,
                self._minimumTrailOpacity,
                self._color,
            )
            painter.setBrush(color)
            painter.drawRoundedRect(
                QRectF(
                    0, -self._lineWidth / 2, self._lineLength, self._lineWidth
                ),
                self._roundness,
                self._roundness,
                Qt.RelativeSize,
            )
            painter.restore()


def create_waiting_spinner(
    parent: QObject,
    number_of_lines: int = 28,
    line_length: int = 20,
    inner_radius: int = 15,
) -> StyledWaitingSpinner:
    """Create a waiting spinner with default config."""
    spinner = StyledWaitingSpinner(parent)
    spinner.setColor(get_color("context_color"))
    spinner.setNumberOfLines(number_of_lines)
    spinner.setLineLength(line_length)
    spinner.setInnerRadius(inner_radius)
    spinner.setLineWidth(2)
    return spinner


def create_tooltip(title: str, description: Union[str, List[str]]) -> str:
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
