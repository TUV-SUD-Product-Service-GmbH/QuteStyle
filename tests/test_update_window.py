"""Tests for the TSLMainWindow."""
from PyQt5.QtCore import QPoint, QSettings, QSize
from pytestqt.qtbot import QtBot

from tsl.update_window import AppData, TSLMainWindow


def test_update_window(qtbot: QtBot) -> None:
    """Test position and size of the UpdateWindow are stored and loaded."""
    with qtbot.captureExceptions() as exceptions:
        assert not QSettings().value("geometry")
        assert not QSettings().value("state")
        widget = create_new_tsl_main_window(qtbot)
        widget.move(300, 300)
        widget.resize(QSize(500, 500))
        widget.close()

        widget = create_new_tsl_main_window(qtbot)
        assert widget.pos() == QPoint(300, 300)
        assert widget.size() == QSize(500, 500)

    assert not exceptions


def create_new_tsl_main_window(qtbot: QtBot) -> TSLMainWindow:
    """Create and show a new TSLMainWindow."""
    widget = TSLMainWindow(AppData("", "1.0.0"))
    qtbot.addWidget(widget)
    widget.show()
    qtbot.waitUntil(widget.isVisible)
    return widget
