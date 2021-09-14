"""Entry defining a software change for the WhatsNewWindow."""
import logging
from enum import IntEnum
from typing import List, TypedDict

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QWidget

from tsl.gen.ui_whats_new_window import Ui_whats_new_window

LOG_NAME = ".".join(["tsl", __name__])
log = logging.getLogger(LOG_NAME)  # pylint: disable=invalid-name


class WhatsNewEntryType(IntEnum):
    """Definition of the type of a WhatsNewEntry."""

    FEATURE = 0
    BUGFIX = 1


class WhatsNewEntry(TypedDict):
    """Entry defining a software change for the WhatsNewWindow."""

    entry_type: WhatsNewEntryType
    title: str
    text: str  # text as html
    work_item_id: int  # id of the work item in TFS or DevOps
    cl_text: str  # one lined text for the changelog generation
    user_groups: List[str]  # restrict display to user groups


class WhatsNewWindow(QMainWindow):
    """WhatsNewWindow showing version update information."""

    def __init__(
        self,
        entries: List[WhatsNewEntry],
        version: str,
        parent: QWidget = None,
    ) -> None:
        """Set up the WhatsNewWindow."""
        super().__init__(parent)
        log.debug(
            "Creating WhatsNewWindow for version %s with entries: %s",
            version,
            entries,
        )
        self._ui = Ui_whats_new_window()
        self._ui.setupUi(self)

        self._entries = entries
        self._version = version

        self._current_entry_idx = 0
        self._display_entry()

        self._ui.previous_button.clicked.connect(self.on_previous)
        self._ui.next_button.clicked.connect(self.on_next)
        self._ui.close_button.clicked.connect(self.close)
        self._ui.text_label.setOpenExternalLinks(True)

    @pyqtSlot(name="on_next")
    def on_next(self) -> None:
        """Handle a click on the button to display the next entry."""
        self._current_entry_idx += 1
        log.debug("Changing to entry %s", self._current_entry_idx)
        self._display_entry()

    @pyqtSlot(name="on_previous")
    def on_previous(self) -> None:
        """Handle a click on the button to display the previous entry."""
        self._current_entry_idx -= 1
        log.debug("Changing to entry %s", self._current_entry_idx)
        self._display_entry()

    def _display_entry(self) -> None:
        """Display the entry set as current index."""
        log.debug(
            "Displaying entry %s/%s",
            self._current_entry_idx,
            len(self._entries),
        )
        if not self._entries:
            self._display_no_entries()
        entry = self._entries[self._current_entry_idx]

        self.setWindowTitle(
            f"Version {self._version} - {self._current_entry_idx + 1}/"
            f"{len(self._entries)} - {entry['title']}"
        )

        entry_font = QFont("Segoe UI", 9)
        self._ui.text_label.setFont(entry_font)
        self._ui.text_label.setText(entry["text"])

        prev_disable = self._current_entry_idx == 0
        self._ui.previous_button.setDisabled(prev_disable)

        next_disable = self._current_entry_idx == len(self._entries) - 1
        self._ui.next_button.setDisabled(next_disable)

    def _display_no_entries(self) -> None:
        """Display that no entries are available."""
        no_entries: WhatsNewEntry = {
            "entry_type": WhatsNewEntryType.FEATURE,
            "title": "Keine Neuerungen",
            "text": "<p>Es gibt keine Neuerungen.</p>",
            "work_item_id": 51762,
            "cl_text": "Es gibt keine Neuerungen.",
            "user_groups": [],
        }
        self._entries.append(no_entries)
        self._display_entry()
