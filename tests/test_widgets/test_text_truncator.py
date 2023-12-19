"""Tests for the TextTruncator."""
import pytest
from PySide6.QtGui import QFont, QFontMetrics

from qute_style.widgets.text_truncator import TextTruncator


@pytest.mark.parametrize(
    "text, width, expected",
    [
        ("Hello World", 100, "Hello World"),
        ("Long text that needs to be truncated", 65, "Long text …"),
        ("", 50, ""),
        ("Short", 1000, "Short"),
    ],
)
def test_truncate_text(text: str, width: int, expected: str) -> None:
    """Test if text is truncated as expected."""
    # Arrange
    truncator = TextTruncator()

    # Act
    result = truncator.truncate_text(
        text, width, QFontMetrics(QFont("Segoe UI", 9))
    )

    # Assert
    assert result.text() == expected
