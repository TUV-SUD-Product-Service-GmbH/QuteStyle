"""Sample classes."""

from __future__ import annotations

from PySide6.QtWidgets import QWidget

from qute_style.widgets.styled_combobox import (
    CheckableComboBox,
    SelectAllComboBox,
)


class TestComboBox(CheckableComboBox[int]):
    """Combobox that displays a list of sample items to be checked."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a new TestCombobox."""
        super().__init__(parent)
        self._default_text = "No selection."

        # Set the data for nine test items
        for idx in range(1, 10):
            text = f"New Item {idx}"
            self.addItem(text, idx, ":/svg_icons/delete_forever.svg")


class SelectAllTestComboBox(SelectAllComboBox[int]):
    """Combobox that displays a list of sample items to be checked."""

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a new TestCombobox."""
        super().__init__(parent)
        self._default_text = "No selection."

        # Set the data for nine test items
        for idx in range(1, 10):
            text = f"New Item {idx}"
            self.addItem(text, idx, ":/svg_icons/delete_forever.svg")

        # initialize combobox content
        self.initialize_content()
