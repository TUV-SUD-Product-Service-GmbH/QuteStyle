"""Test for spinner widget."""
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QWidget
from pytestqt.qtbot import QtBot

from qute_style.widgets.spinner import WaitingSpinner


def test_spinner_properties(qtbot: QtBot) -> None:
    """Test if spinner properties work as expected."""
    widget = QWidget()
    qtbot.addWidget(widget)
    spinner = WaitingSpinner(widget)
    qtbot.addWidget(spinner)

    spinner.roundness = 1
    spinner.fade = 2
    spinner.lines = 3
    spinner.line_length = 4
    spinner.line_width = 5
    spinner.radius = 6
    spinner.speed = 7
    spinner.color = QColor(1, 2, 3)

    assert spinner.roundness == 1
    assert spinner.fade == 2
    assert spinner.lines == 3
    assert spinner.line_length == 4
    assert spinner.line_width == 5
    assert spinner.radius == 6
    assert spinner.speed == 7
    assert spinner.color == QColor(1, 2, 3)


def test_spinning(qtbot: QtBot) -> None:
    """Check if Spinner is spinning."""
    widget = QWidget()
    qtbot.addWidget(widget)
    spinner = WaitingSpinner(widget)
    qtbot.addWidget(spinner)

    assert spinner.is_spinning is False
    spinner.start()
    assert spinner.is_spinning is True
    spinner.stop()
    assert spinner.is_spinning is False
