"""Tests for LeftColumn."""
# pylint: disable=protected-access
from __future__ import annotations

from typing import Type

import pytest
from _pytest.fixtures import SubRequest
from PyQt5.QtWidgets import QWidget
from pytestqt.qtbot import QtBot

from examples.styled_main_window import InfoWidget, SettingsWidget
from tsl.dev.mocks import check_call
from tsl.widgets.base_widgets import BaseWidget, SettingsBaseWidget
from tsl.widgets.left_column import LeftColumn


@pytest.fixture(name="left_column")
def fixture_left_column(qtbot: QtBot) -> LeftColumn:
    """Get Left Column."""
    left_column = LeftColumn(QWidget(), [SettingsWidget, InfoWidget])
    qtbot.addWidget(left_column)
    left_column.show()
    qtbot.waitUntil(left_column.isVisible)
    return left_column


@pytest.fixture(
    name="settings_widget",
    params=[True, False],
    ids=["Local Settings", "No Local Settings"],
)
def fixture_settings_widget(
    qtbot: QtBot, request: SubRequest
) -> QWidget | None:
    """Get settings widget."""
    if request.param:
        widget = QWidget()
        qtbot.addWidget(widget)
        return widget
    return None


@pytest.mark.parametrize(
    "column_widget, result",
    [(SettingsWidget, 1), (InfoWidget, 0)],
    ids=["On Settings", "On Info"],
)
def test_handle_settings_display(
    left_column: LeftColumn,
    settings_widget: QWidget,
    column_widget: Type[BaseWidget],
    result: int,
) -> None:
    """
    Test handling of settings display.

    Parametrization:
    On Settings: If local settings exist, they need to be displayed otherwise
    global settings are displayed.
    On Info: In both cases, the info needs to be displayed.
    """
    left_column.set_column_widget(column_widget)
    with check_call(SettingsBaseWidget, "clear_widget", call_count=result):
        if settings_widget:
            with check_call(
                SettingsBaseWidget, "add_widget", call_count=result
            ):
                left_column.handle_settings_display(
                    settings_widget, ":/svg_icons/no_icon.svg"
                )
                if result == 1:
                    assert (
                        left_column._icon._icon_path
                        == ":/svg_icons/no_icon.svg"
                    )
                else:
                    assert (
                        left_column._icon._icon_path == ":/svg_icons/info.svg"
                    )
        else:
            left_column.handle_settings_display(
                settings_widget, ":/svg_icons/no_icon.svg"
            )
            if result == 0:
                assert left_column._icon._icon_path == ":/svg_icons/info.svg"
                return
            assert left_column._icon._icon_path == ":/svg_icons/settings.svg"
