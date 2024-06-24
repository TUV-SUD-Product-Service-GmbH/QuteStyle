"""Base widget definitions."""

from __future__ import annotations

import logging
from typing import cast

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QGridLayout, QVBoxLayout, QWidget

log = logging.getLogger(
    f"qute_style.{__name__}"
)  # pylint: disable=invalid-name


class BaseWidget(QWidget):
    """Base class for a widget that is displayed in the right section."""

    ICON: str
    NAME: str
    GROUPS: list[str] = []


class MainWidget(BaseWidget):
    """Base class for a widget that is display in the main section."""

    shutdown_completed = Signal(QWidget, name="shutdown_completed")

    def __repr__(self) -> str:
        """Return a str representation for the MainWidget."""
        return f"<{self.__class__} {self.NAME} {id(self)}>"

    def shutdown(self) -> None:
        """
        Shutdown the application.

        Can be overriden in case some special actions (finish threads, ...) are
        needed to shutdown the widget. At the end shutdown_completed signal
        must be emitted.
        """
        log.debug("Shutting down tab %s", self.NAME)
        self.shutdown_completed.emit(self)

    def store_settings(self) -> None:  # pragma: no cover
        """
        Store the settings.

        Can be overriden to store widget based information when the application
        is closed.
        """

    @property
    def settings_widget(
        self,
    ) -> None | QWidget:
        """Get the settings widget. Implemented by custom classes."""
        return None

    def request_shutdown(self) -> bool:
        """
        Request shutdown from a widget so that the widget can interfere.

        If a widget wants to cancel the shutdown, it must reimplement this
        method and return False.
        """
        return True


class SettingsBaseWidget(BaseWidget):
    """SettingsBaseWidget."""

    ICON = ":/svg_icons/settings.svg"
    NAME = "Einstellungen"

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a new SettingsWidget."""
        super().__init__(parent)
        # define layout in which local settings will be displayed
        self._layout = QGridLayout()
        self._layout.setSpacing(10)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._has_no_global = True

    def _set_global_widget(self, global_widget: QWidget) -> None:
        """Global widget can only be set once."""
        if self._has_no_global:
            # insert local settings layout into global one
            cast(QVBoxLayout, global_widget.layout()).insertLayout(
                -1, self._layout
            )

    def add_widget(self, widget: QWidget) -> None:
        """Add the given widget to the settings."""
        self._layout.addWidget(widget, 1, 0)

    def clear_widget(self) -> None:
        """Remove a widget from the settings if present."""
        if item := self._layout.itemAtPosition(1, 0):
            item.widget().setParent(None)  # type: ignore[call-overload]
