"""Tests for the Checkable Combobox."""
from PySide6.QtCore import Qt
from pytestqt.qtbot import QtBot

from qute_style_examples.sample_classes import (
    SelectAllTestComboBox,
    TestComboBox,
)


def create_show_test_combobox(
    qtbot: QtBot, single_mode: bool = False
) -> TestComboBox:
    """Create, register, show and return a new TestComboBox."""

    combobox = TestComboBox()
    combobox.single_mode = single_mode
    qtbot.addWidget(combobox)
    combobox.show()
    qtbot.waitUntil(combobox.isVisible)
    return combobox


def create_show_select_all_combobox(qtbot: QtBot) -> SelectAllTestComboBox:
    """Create, register, show and return a new SelectAllTestComboBox."""

    combobox = SelectAllTestComboBox()
    qtbot.addWidget(combobox)
    combobox.show()
    qtbot.waitUntil(combobox.isVisible)
    return combobox


def test_text(qtbot: QtBot) -> None:
    """Test the text of TestComboBox reflects the selected classes."""
    with qtbot.captureExceptions() as exceptions:
        combobox = create_show_test_combobox(qtbot)
        combobox.item_ids = [1, 2]
        assert combobox.currentText() == "1, 2"
        combobox.model().item(2).setCheckState(Qt.CheckState.Checked)
        assert combobox.currentText() == "1, 2, 3"
        assert combobox.item_ids == [1, 2, 3]
    assert not exceptions


def test_single_mode(qtbot: QtBot) -> None:
    """Test the text of TestComboBox reflects the selected classes."""
    with qtbot.captureExceptions() as exceptions:
        combobox = create_show_test_combobox(qtbot, True)
        combobox.item_ids = [1]
        assert combobox.currentText() == "1"
        combobox.model().item(1).setCheckState(Qt.CheckState.Checked)
        assert combobox.currentText() == "2"
        assert combobox.model().item(0).checkState() == Qt.CheckState.Unchecked
    assert not exceptions


def test_popup_event_filter(qtbot: QtBot) -> None:
    """Test that the eventFilter for opening/closing the popup works."""
    with qtbot.captureExceptions() as exceptions:
        combobox = create_show_test_combobox(qtbot, True)
        combobox.item_ids = [1]

        # the event propagation in QtBot does not work correct so we cannot
        # test if the popup is really shown. therefore we check that at least
        # the internal state and eventFilter work.
        pos = combobox.lineEdit().rect().center()
        qtbot.mouseRelease(
            combobox.lineEdit(), Qt.MouseButton.LeftButton, pos=pos
        )
        assert combobox.popup_open is True
        qtbot.mouseRelease(
            combobox.lineEdit(), Qt.MouseButton.LeftButton, pos=pos
        )
        assert combobox.popup_open is False

    assert not exceptions


def test_check_state_event_filter(qtbot: QtBot) -> None:
    """Test that clicking on an entry checks the item."""
    with qtbot.captureExceptions() as exceptions:
        combobox = create_show_test_combobox(qtbot, True)
        combobox.item_ids = [0]

        combobox.showPopup()

        # get item for 1 which isn't checked
        index = combobox.model().index(1, 0)
        pos = combobox.view().visualRect(index).center()

        # click on the item to check it
        qtbot.mouseClick(
            combobox.view().viewport(), Qt.MouseButton.LeftButton, pos=pos
        )
        assert combobox.model().item(1).checkState() == Qt.Checked

        # click again on the item to uncheck it
        qtbot.mouseClick(
            combobox.view().viewport(), Qt.MouseButton.LeftButton, pos=pos
        )
        assert combobox.model().item(1).checkState() == Qt.Unchecked

    assert not exceptions


def test_select_all(qtbot: QtBot) -> None:
    """Test that select_all works as expected."""
    with qtbot.captureExceptions() as exceptions:
        combobox = create_show_select_all_combobox(qtbot)
        combobox.showPopup()

        # all items have to be selected
        for idx in range(2, combobox.model().rowCount()):
            assert (
                combobox.model().item(idx).checkState()
                == Qt.CheckState.Checked
            )

        # if deselected, all items have to be deselected
        combobox.model().item(0).setCheckState(Qt.CheckState.Unchecked)

        for idx in range(2, combobox.model().rowCount()):
            assert (
                combobox.model().item(idx).checkState()
                == Qt.CheckState.Unchecked
            )

        # if items have different checkstates,
        # select_all has to be partially checked
        combobox.model().item(3).setCheckState(Qt.CheckState.Checked)

        assert (
            combobox.model().item(0).checkState()
            == Qt.CheckState.PartiallyChecked
        )

    assert not exceptions
