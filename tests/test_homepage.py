"""Tests for homepage."""
import importlib
from pathlib import Path
from typing import Type, cast

import pytest
from _pytest.monkeypatch import MonkeyPatch
from PyQt5.QtWidgets import QGridLayout, QLabel
from pytestqt.qtbot import QtBot

from examples.styled_main_window import StyledMainWindow
from tests.test_tsl_style_main_window import WindowT
from tsl import tsl_main_gui
from tsl.dev.dev_functions import (
    generate_changelog_resource_file,
    get_change_log_data,
)
from tsl.update_window import AppData
from tsl.widgets.home_page import HomePage

APP_NAME = "TEST-APP"


def create_new_main_window(
    qtbot: QtBot,
    monkeypatch: MonkeyPatch,
    user_group: str,
    lang: str,
    window_class: Type[WindowT],
) -> WindowT:
    """Create and show a new TSLMainWindow."""
    generate_changelog_resource_file(  # create the resource file
        APP_NAME,
        Path.cwd() / "examples" / "test_changelog",
        Path.cwd() / "examples",
    )
    importlib.import_module("examples.resources_cl")

    monkeypatch.setattr(
        tsl_main_gui, "get_user_group_name", lambda: user_group
    )
    monkeypatch.setattr(tsl_main_gui, "get_app_language", lambda: lang)

    widget = window_class(AppData(APP_NAME, "1.0.0"))
    qtbot.addWidget(widget)
    widget.show()
    qtbot.waitUntil(widget.isVisible)
    return widget


# pylint: disable=protected-access
@pytest.mark.parametrize(
    "user_group, lang",
    [("PS-CPS-TSL-G", "de"), ("PS-CPS-TSL-G", "en"), ("PS-not-known", "de")],
)
def test_changelog_data(  # pylint: disable=too-many-locals
    qtbot: QtBot, monkeypatch: MonkeyPatch, user_group: str, lang: str
) -> None:
    """
    Test changelog window.

    When group is not PS-CPS-TSL-G TestWidget is not displayed in changelog
    because the user has no rights. See group setting.
    """
    # get the changelog data
    change_log_data = get_change_log_data(
        APP_NAME,
        Path.cwd() / "examples" / "test_changelog",
    )

    window = create_new_main_window(
        qtbot, monkeypatch, user_group, lang, StyledMainWindow
    )
    homepage = window.get_main_widget(HomePage)
    assert homepage

    layout = homepage._widget_stack.widget(1).layout()
    label = cast(QLabel, layout.itemAt(0).widget())
    assert label.text() == "Versionshistorie"
    grid = cast(QGridLayout, layout.itemAt(1).widget().widget().layout())

    row = 0
    for key, log_data_dict in change_log_data.items():
        version = cast(QLabel, grid.itemAtPosition(row, 1).widget()).text()
        row += 1
        assert version == "V " + key

        # handle general logs
        if APP_NAME in log_data_dict:
            widget_name = cast(
                QLabel, grid.itemAtPosition(row, 2).widget()
            ).text()
            row += 1
            assert APP_NAME == widget_name
            for log_text in log_data_dict[APP_NAME]:
                text = cast(
                    QLabel, grid.itemAtPosition(row, 2).widget()
                ).text()
                row += 1
                assert log_text[lang] == text

        # handle widget specific logs
        for widget in homepage._visible_widgets:
            if widget.__name__ in log_data_dict:
                widget_name = cast(
                    QLabel, grid.itemAtPosition(row, 2).widget()
                ).text()
                row += 1
                assert widget.NAME == widget_name
                for log_text in log_data_dict[widget.__name__]:
                    text = cast(
                        QLabel, grid.itemAtPosition(row, 2).widget()
                    ).text()
                    row += 1
                    assert log_text[lang] == text
