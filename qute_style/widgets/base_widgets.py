"""Base widget definitions."""
from __future__ import annotations

import logging
from typing import cast

from PySide6.QtCore import QThread, Signal, Slot
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

    def __init__(self, parent: QWidget | None = None) -> None:
        """Init the BaseWidget for a Widget in QuteStyle."""
        self._thread: QThread | None = None
        super().__init__(parent)

    def __repr__(self) -> str:
        """Return a str representation for the MainWidget."""
        return f"<{self.__class__} {self.NAME} {id(self)}>"

    def shutdown(self) -> None:
        """Shutdown the application."""
        log.debug("Shutting down tab %s", self.NAME)
        if self._thread is not None and self._thread.isRunning():
            log.debug("Thread is in running state %s", self.NAME)
            # Disconnect the current handlers before attaching a new slot.
            # In case of nav_loader a new thread would be started in the
            # original finished handler which will then lead to an error
            # when closing the app because this thread is still running.
            # Restarting the app in this case fails.
            self._thread.finished.disconnect()
            self._thread.finished.connect(self.on_thread_finished)
        else:
            self.on_thread_finished()

    def store_settings(self) -> None:  # pragma: no cover
        """Store the settings."""

    @property
    def settings_widget(
        self,
    ) -> None | QWidget:
        """Get the settings widget. Implemented by custom classes."""
        return None

    @Slot(name="on_thread_finished")
    def on_thread_finished(self) -> None:
        """Handle the shutdown when the thread has finished."""
        log.debug("On thread finished base class %s", self.NAME)
        self.shutdown_completed.emit(self)

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
            item.widget().setParent(QWidget())
