"""Test helper methods."""
import sys

import pytest
from PySide6.QtWidgets import QApplication, QWidget

from qute_style.helper import check_ide, create_tooltip, create_waiting_spinner
from qute_style.qs_application import QuteStyleApplication
from tests.conftest import QuteStyleTestApplication


@pytest.mark.parametrize(
    "path,result",
    (
        (r"C:\test\test.exe", False),
        (r"C:\test\test", False),
        (r"C:\test\test.py", True),
    ),
)
def test_check_ide(path: str, result: bool) -> None:
    """Test that the check_ide method returns the correct result."""
    old_path = sys.argv[0]
    sys.argv[0] = path
    assert check_ide() == result
    sys.argv[0] = old_path


def test_create_spinner(qapp: QuteStyleApplication) -> None:
    """Test that a default waiting spinner is returned."""
    assert qapp
    widget = QWidget()
    spinner = create_waiting_spinner(widget)
    assert spinner.number_of_lines == 28
    assert spinner.line_length == 20
    assert spinner.inner_radius == 15
    assert spinner.line_width == 2


def test_create_tooltip() -> None:
    """Test if given text is translated to html."""
    tooltip = create_tooltip("test title", "test description")
    assert tooltip == (
        "<div><p><b>test title</b></p>"
        "<p><small>test description</small></p></div>"
    )
