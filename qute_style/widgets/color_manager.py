"""ColorManager for live editing of colors."""

from __future__ import annotations

import json
import logging
from typing import cast

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QPaintEvent
from PySide6.QtWidgets import (
    QApplication,
    QColorDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QWidget,
)

from qute_style.style import MAIN_STYLE, THEMES, get_current_style
from qute_style.widgets.base_widgets import BaseWidget
from qute_style.widgets.icon_button import IconButton

log = logging.getLogger(
    f"qute_style.{__name__}"
)  # pylint: disable=invalid-name


class SmallIconButton(IconButton):
    """Icon button with a reduced size."""

    FIXED_WIDTH = 24
    FIXED_HEIGHT = 24


class ColorWidget(QWidget):
    """Widget displaying a color with a button to change it."""

    color_changed = Signal(name="color_changed")

    def __init__(
        self, key: str, color: str, parent: QWidget | None = None
    ) -> None:
        """Create a new Color Widget."""
        super().__init__(parent)
        self.key = key
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._color_label = QLabel(color)
        self._color_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        layout.addWidget(self._color_label)
        self._color_button = SmallIconButton(self, ":/svg_icons/palette.svg")
        self._color_button.clicked.connect(self.on_change_color)
        layout.addWidget(self._color_button)

    @property
    def color(self) -> str:
        """Return the current color."""
        return self._color_label.text()

    @color.setter
    def color(self, color: str) -> None:
        """Set the color."""
        log.debug(
            "Setting new color: %s, old color: %s",
            color,
            self._color_label.text(),
        )
        self._color_label.setText(color.lower())
        self._color_label.setStyleSheet(
            f"QLabel {{ background-color: {color} ; color: black}}"
        )

    def on_change_color(self) -> None:
        """Open a color dialog to change the color."""
        dialog = QColorDialog(QColor(self._color_label.text()), self)
        if dialog.exec() == QColorDialog.DialogCode.Accepted:
            self.color = dialog.selectedColor().name()
            self.color_changed.emit()


class ColorManager(BaseWidget):
    """ColorManager for live editing of colors."""

    ICON = ":/svg_icons/palette.svg"
    NAME = "Color Manager"

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a new ColorManager."""
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        scroll_area = QScrollArea(self)
        scroll_area.setObjectName("bg_two_frame")
        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        layout.addWidget(scroll_area)

        frame = QWidget()
        frame.setObjectName("bg_two_frame")
        grid_layout = QGridLayout(frame)
        assert frame.layout() is grid_layout
        scroll_area.setWidget(frame)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSizeConstraint(QGridLayout.SizeConstraint.SetFixedSize)
        grid_layout.setSpacing(2)

        self._widgets = []

        for idx, key in enumerate(sorted(THEMES[next(iter(THEMES.keys()))])):
            log.debug("Adding row for key %s", key)
            grid_layout.addWidget(QLabel(key), idx, 0)
            widget = ColorWidget(key, "", scroll_area)
            widget.color_changed.connect(self.on_color_changed)
            grid_layout.addWidget(widget, idx, 1)
            self._widgets.append(widget)

        self._code_label = QLabel(self)
        self._code_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        grid_layout.addWidget(
            self._code_label, grid_layout.rowCount(), 0, 1, 2
        )

        self._current_style: str = get_current_style()
        self.update_style()
        self.set_code()

    def paintEvent(self, event: QPaintEvent) -> None:  # noqa: N802
        """Check if the style has changed."""
        if self._current_style != get_current_style():
            log.debug("Updating colors to style: %s", self._current_style)
            self._current_style = get_current_style()
            self.update_style()
        super().paintEvent(event)

    def update_style(self) -> None:
        """Update all widgets with the current set style."""
        style = THEMES[self._current_style]
        for widget in self._widgets:
            widget.color = style[widget.key]

    def _create_theme(self) -> dict[str, str]:
        """Create the code from the selected colors."""
        return {widget.key: widget.color for widget in self._widgets}

    def on_color_changed(self) -> None:
        """Set the new stylesheet when a color has changed."""
        log.debug("Color has changed, changing theme.")
        theme = self._create_theme()
        app = cast(QApplication, QApplication.instance())
        assert app is not None
        app.activeWindow().setStyleSheet(MAIN_STYLE.format(**theme))
        self.set_code()

    def set_code(self) -> None:
        """Set the theme's code in the label."""
        theme = self._create_theme()
        self._code_label.setText(json.dumps(theme, sort_keys=True, indent=4))
