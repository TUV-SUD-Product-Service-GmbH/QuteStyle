"""Base widget definitions."""
from PyQt5.QtWidgets import QWidget


class ColumnBaseWidget(QWidget):
    """Base class for a widget that is displayed in the right section."""

    ICON: str
    NAME: str


class MainWidget(QWidget):
    """Base class for a widget that is display in the main section."""

    ICON: str
    NAME: str
