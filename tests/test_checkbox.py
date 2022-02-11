"""Tests for StyledComboBox and CheckableComboBox"""
from random import randint
from typing import List

import pytest
from PyQt5.QtCore import Qt
from pytestqt.qtbot import QtBot

from tsl.widgets.styled_combobox import CheckableComboBox, TooManyItemsError


# pylint: disable=protected-access
@pytest.fixture(scope="function", name="cb_items")
def fixture_cb_items(combobox: CheckableComboBox[int]) -> None:
    """Create several test items."""
    for idx in range(randint(3, 10)):
        text = f"New Item {idx}"
        combobox.addItem(text, idx)


@pytest.fixture(scope="function", name="combobox")
def fixture_combobox(
    qtbot: QtBot,
) -> CheckableComboBox[int]:
    """Create, register, show and return a new TestComboBox."""
    combobox: CheckableComboBox[int] = CheckableComboBox()
    combobox._default_text = "No selection"
    qtbot.addWidget(combobox)
    combobox.show()
    qtbot.waitUntil(combobox.isVisible)
    return combobox


@pytest.mark.parametrize("mode", (False, True))
@pytest.mark.parametrize("items", ([], [1], [0, 1, 2]))
def test_text(
    combobox: CheckableComboBox[int],
    cb_items: None,  # pylint: disable=unused-argument
    mode: bool,
    items: List[int],
    qtbot: QtBot,
) -> None:
    """Test that the text of CheckableComboBox reflects the selected items."""
    with qtbot.captureExceptions() as exceptions:
        combobox.single_mode = mode
        # custom exception has to be raised if one tries to
        # submit several items to a single mode checkbox
        if mode and len(items) > 1:
            with pytest.raises(TooManyItemsError):
                combobox.item_ids = items
            return
        combobox.item_ids = items
        if not items:
            assert combobox.currentText() == "No selection"
        elif mode:
            assert combobox.currentText() == str(items[-1])
        else:
            assert combobox.currentText() == ", ".join(
                [str(item) for item in items]
            )
    assert not exceptions


@pytest.mark.parametrize("mode", (False, True))
@pytest.mark.parametrize("items", ([1], [0, 1, 2]))
def test_item_ids(
    combobox: CheckableComboBox[int],
    cb_items: None,  # pylint: disable=unused-argument
    mode: bool,
    items: List[int],
    qtbot: QtBot,
) -> None:
    """Test that the ids of checked items are correctly returned."""
    with qtbot.captureExceptions() as exceptions:
        combobox.single_mode = mode
        for item in items:
            combobox.model().item(item).setCheckState(Qt.Checked)
        if mode:
            assert combobox.item_ids == [items[-1]]
        else:
            assert combobox.item_ids == items
    assert not exceptions


def test_popup_event_filter(
    combobox: CheckableComboBox[int], qtbot: QtBot
) -> None:
    """Test that the eventFilter for opening/closing the popup works."""
    with qtbot.captureExceptions() as exceptions:
        combobox.item_ids = [0]

        # the event propagation in QtBot does not work correct, so we cannot
        # test if the popup is really shown. Therefore, we check that at least
        # the internal state and eventFilter work.
        pos = combobox.lineEdit().rect().center()
        qtbot.mouseRelease(combobox.lineEdit(), Qt.LeftButton, pos=pos)
        assert combobox.popup_open is True
        qtbot.mouseRelease(combobox.lineEdit(), Qt.LeftButton, pos=pos)
        assert combobox.popup_open is False

    assert not exceptions


@pytest.mark.parametrize("checked", (Qt.Unchecked, Qt.Checked))
def test_check_state_event_filter(
    combobox: CheckableComboBox[int],
    cb_items: None,  # pylint: disable=unused-argument
    checked: Qt.CheckState,
    qtbot: QtBot,
) -> None:
    """Test that clicking on an entry checks or unchecks the item."""
    with qtbot.captureExceptions() as exceptions:

        combobox.showPopup()
        if not checked:
            combobox.item_ids = [0]

        index = combobox.model().index(0, 0)
        pos = combobox.view().visualRect(index).center()

        qtbot.mouseClick(combobox.view().viewport(), Qt.LeftButton, pos=pos)
        assert combobox.model().item(0).checkState() == checked

    assert not exceptions
