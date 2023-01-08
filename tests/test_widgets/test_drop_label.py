"""Test for drop label."""
from typing import cast

from PyQt5.QtWidgets import QLabel, QWidget
from pytestqt.qtbot import QtBot

from qute_style.widgets.drop_label import DropLabel


def test_drop_label(qtbot: QtBot) -> None:
    """Test if drop label is shown as expected."""
    widget = QWidget()
    qtbot.addWidget(widget)
    drop_label = DropLabel("test text", widget)
    drop_label.show()
    qtbot.addWidget(drop_label)
    assert drop_label.layout().count() == 4
    assert (
        cast(QLabel, drop_label.layout().itemAt(2).widget()).text()
        == "test text"
    )
