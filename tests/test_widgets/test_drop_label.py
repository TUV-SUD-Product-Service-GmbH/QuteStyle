"""Test for drop label."""

from typing import cast

from PySide6.QtWidgets import QLabel, QWidget
from pytestqt.qtbot import QtBot

from qute_style.widgets.drop_label import DropLabel


def test_drop_label(qtbot: QtBot) -> None:
    """Test if drop label is shown as expected."""
    widget = QWidget()
    qtbot.addWidget(widget)
    drop_label = DropLabel("test text", widget)
    drop_label.show()
    qtbot.addWidget(drop_label)
    layout = drop_label.layout()
    assert layout is not None
    assert layout.count() == 4
    item = layout.itemAt(2)
    assert item is not None
    assert cast(QLabel, item.widget()).text() == "test text"
