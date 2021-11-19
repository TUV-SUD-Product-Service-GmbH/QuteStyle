"""Tests for the TitleBar."""
import logging
from typing import Dict

import pytest
from PyQt5.QtWidgets import QLabel, QWidget
from pytestqt.qtbot import QtBot

from tsl.vault import Vault
from tsl.widgets.title_bar import TitleBar

log = logging.getLogger(__name__)  # pylint: disable=invalid-name


@pytest.mark.parametrize(
    "db_cache,pse",
    (
        ({Vault.Application.EDOC: Vault.Environment.PROD}, True),
        ({}, True),
        ({Vault.Application.EDOC: Vault.Environment.TEST}, True),
        ({Vault.Application.EDOC: Vault.Environment.PROD}, False),
        ({}, False),
        ({Vault.Application.EDOC: Vault.Environment.TEST}, False),
    ),
)
def test_db_label(
    qtbot: QtBot,
    db_cache: Dict[Vault.Application, Vault.Environment],
    pse: bool,
) -> None:
    """Test that the db_label is shown when necessary."""
    Vault.CREATED_DATABASES = db_cache
    parent = QWidget()
    qtbot.addWidget(parent)
    title_bar = TitleBar(
        parent, parent, [], "Test", ":/svg_images/logo_toolbox.svg"
    )
    qtbot.addWidget(title_bar)
    parent.show()
    qtbot.waitUntil(parent.isVisible)

    label = title_bar.findChild(QLabel, "db_label")

    log.debug("Cache = %s", Vault.CREATED_DATABASES)
    assert (
        bool(label)
        is bool(
            any(env != Vault.Environment.PROD for env in db_cache.values())
        )
        or pse
    )
