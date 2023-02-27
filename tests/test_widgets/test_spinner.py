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
    spinner.number_of_lines = 3
    spinner.line_length = 4
    spinner.line_width = 5
    spinner.inner_radius = 6
    spinner.speed = 7
    spinner.minimum_trail_opacity = 8
    spinner.trail_fade_percentage = 9
    spinner.revolutions_per_second = 10
    spinner.color = QColor(1, 2, 3)

    assert spinner.roundness == 1
    assert spinner.fade == 2
    assert spinner.number_of_lines == 3
    assert spinner.line_length == 4
    assert spinner.line_width == 5
    assert spinner.inner_radius == 6
    assert spinner.speed == 7
    assert spinner.minimum_trail_opacity == 8
    assert spinner.trail_fade_percentage == 9
    assert spinner.revolutions_per_second == 10
    assert spinner.color == QColor(1, 2, 3)


def test_spinning(qtbot: QtBot) -> None:
    """Check if Spinner is spinning."""
    widget = QWidget()
    qtbot.addWidget(widget)
    spinner = WaitingSpinner(widget)
    qtbot.addWidget(spinner)
    spinner.show()

    assert spinner.is_spinning is False
    spinner.start()
    assert spinner.is_spinning is True
    spinner.stop()
    assert spinner.is_spinning is False
