"""Tests for message boxes."""

import pytest
from PyQt5.QtWidgets import QWidget
from pytestqt.qtbot import QtBot

from qute_style.dev.mocks import check_call
from qute_style.qs_message_box import QuteMessageBox


@pytest.mark.parametrize(
    "message_type", ("information", "warning", "critical", "question")
)
def test_messagebox_types(qtbot: QtBot, message_type: str) -> None:
    """Test if messageboxes have correct type."""
    widget = QWidget()
    qtbot.addWidget(widget)
    with check_call(QuteMessageBox, "_show_message_box"):
        message_box = getattr(QuteMessageBox, message_type)
        message_box(widget, "test title", "test text")
