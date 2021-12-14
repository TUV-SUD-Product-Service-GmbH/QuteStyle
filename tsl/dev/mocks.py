"""
Generic mock functions for unit-tests

Use `check_call` as a context manager to mock calls and their return values as
well as to check if the method was called (or not).

To mock QMessageDialogs one can use `mock_q_message_dialog` to check the
correct call.
"""
from __future__ import annotations

import contextlib
import logging
from types import ModuleType
from typing import Any, Dict, Generator, List, Tuple, Type

from _pytest.monkeypatch import MonkeyPatch
from PyQt5.QtWidgets import QMessageBox, QWidget

log = logging.getLogger(f"tests.{__name__}")  # pylint: disable=invalid-name

CallList = List[Tuple[Tuple[Any, ...], Dict[str, Any]]]


def _check_mp_dialog(
    calls: CallList, parent: QWidget, title: str, text: str
) -> None:
    """Check that the monkey patched QMessageBox was correctly called."""
    log.debug("Calllist: %s", calls)
    assert len(calls) == 1  # only called once
    call_args = calls[0][0]  # arguments of the first and only call
    call_kwargs = calls[0][1]  # kw arguments of the first and only call
    assert call_kwargs == {}  # no kwargs were given
    assert call_args[0] == parent  # parent is set correctly
    assert call_args[1] == title  # check correct title
    assert call_args[2] == text  # check correct text


def _mp_message_dialog(
    monkeypatch: MonkeyPatch,
    method: str = "warning",
    return_value: QMessageBox.StandardButton | None = None,
) -> CallList:
    """Mock a QMessageDialog and return a list with the call's arguments."""
    return _mp_call(monkeypatch, QMessageBox, method, return_value)


def _mp_call(
    monkeypatch: MonkeyPatch,
    mock_class: Type[Any] | ModuleType,
    method: str,
    return_value: Any = None,
) -> CallList:
    """Mock a method in a class and record the calls to it."""
    calls: CallList = []

    def func_call(*a: Any, **k: Any) -> Any:
        """Mock the function call."""
        calls.append((a, k))
        return return_value

    monkeypatch.setattr(mock_class, method, func_call)
    return calls


@contextlib.contextmanager
def mock_q_message_dialog(
    title: str,
    text: str,
    parent: QWidget,
    method: str = "warning",
    return_value: QMessageBox.StandardButton | None = None,
) -> Generator[None, None, None]:
    """
    Mock the QMessageDialog call of a method in a context.

    This context manager will mock and record all calls made within its
    context. It will assert that exactly one call is made to the mocked
    QMessageBox method with the given title, text and parent.

    If a call is made, it will return the given return_value which is of
    type QMessageBox.StandardButton.
    """
    if method != "question" and return_value is not None:
        raise ValueError(
            f"Cannot return anything from methods other than question. Given "
            f"method type: '{method}' and return value: {return_value}"
        )

    monkeypatch = MonkeyPatch()
    calls = _mp_message_dialog(monkeypatch, method, return_value)
    yield
    _check_mp_dialog(calls, parent, title, text)
    monkeypatch.undo()


@contextlib.contextmanager
def check_call(  # pylint: disable=too-many-arguments
    mock_class: Type[Any] | ModuleType,
    method: str,
    return_value: Any = None,
    call_args: Tuple[Any, ...] | None = None,
    call_kwargs: Dict[str, Any] | None = None,
    called: bool = True,
) -> Generator[CallList, None, None]:
    """
    Context manager for mocking and checking a call to a method.

    If called is True, and call_args and call_kwargs are given, the context
    manager will check that the call to the mocked method was done with those
    arguments. Also, it will assert that the mock was called exactly once.

    If called is False, it will assert that the mock was not called.

    If a return_value is given, the mock will return this value.
    """
    assert (call_args is not None and call_kwargs is not None) or (
        call_args is None and call_kwargs is None
    ), (
        "call_args and call_kwargs must be None or have a value "
        "(list/dict if empty)"
    )
    monkeypatch = MonkeyPatch()
    calls = _mp_call(monkeypatch, mock_class, method, return_value)
    yield calls
    if not called:
        assert not calls
    else:
        assert (
            len(calls) == 1
        ), f"Calls to {method}: {len(calls)}"  # only called once
        if call_args or call_kwargs:
            assert call_args == calls[0][0]
            assert call_kwargs == calls[0][1]
    monkeypatch.undo()
