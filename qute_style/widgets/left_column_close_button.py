"""Close Button on the left Menu."""

from __future__ import annotations

from PySide6.QtWidgets import QWidget

from qute_style.widgets.icon_button import BackgroundColorNames
from qute_style.widgets.title_button import TitleButton


class LeftColumnCloseButton(TitleButton):
    """Close Button on the left TitleBar (TitleButton with other colors)."""

    def __init__(
        self,
        app_parent: QWidget,
        tooltip_text: str,
        icon_path: str,
        parent: QWidget | None = None,
    ) -> None:
        """Init LeftMenuCloseButton."""
        bgs = BackgroundColorNames(
            hovering="bg_two",
            background="bg_one",
            pressed="bg_one",
            released="bg_three",
        )
        super().__init__(app_parent, tooltip_text, icon_path, parent, bgs)
