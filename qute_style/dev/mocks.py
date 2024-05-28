"""
Generic mock functions for unit-tests.

Use `check_call` as a context manager to mock calls and their return values as
well as to check if the method was called (or not).

To mock QMessageDialogs one can use `mock_q_message_dialog` to check the
correct call.
"""

from __future__ import annotations

import contextlib
import logging
from collections.abc import Callable, Generator
from types import ModuleType
from typing import Any, overload

from _pytest.monkeypatch import MonkeyPatch
from mypy_extensions import KwArg, VarArg
from PySide6.QtWidgets import QMessageBox, QWidget

from qute_style.qs_message_box import QuteMessageBox

log = logging.getLogger(f"tests.{__name__}")  # pylint: disable=invalid-name

Call = tuple[tuple[Any, ...], dict[str, Any]]
CallList = list[Call]


def _check_mp_dialog(
    calls: CallList, parent: QWidget, title: str, text: str
) -> None:
    """Check that the monkey patched QMessageBox was correctly called."""
    log.debug("Calllist: %s", calls)
    assert len(calls) == 1, f"Calls to QMessageBox: {len(calls)}, expected: 1"
    call_args = calls[0][0]  # arguments of the first and only call
    call_kwargs = calls[0][1]  # kw arguments of the first and only call
    assert call_kwargs == {}  # no kwargs were given
    assert call_args[0] == parent  # parent is set correctly
    assert call_args[1] == title, f"Title is '{call_args[1]}'"
    assert call_args[2] == text, f"Text is '{call_args[2]}'"


def _mp_message_dialog(
    monkeypatch: MonkeyPatch,
    method: str = "warning",
    return_value: QMessageBox.StandardButton | None = None,
    mock_class: type[QMessageBox] = QMessageBox,
) -> CallList:
    """Mock a QMessageDialog and return a list with the call's arguments."""
    return _mp_call(monkeypatch, mock_class, method, return_value, False)  # type: ignore


@overload  # type: ignore
@contextlib.contextmanager
def _mp_call(
    monkeypatch: MonkeyPatch,
    mock_class: type[Any] | ModuleType,
    method: str,
    return_value: Any,
    as_property: bool,
) -> CallList: ...


@overload  # type: ignore
@contextlib.contextmanager
def _mp_call(
    monkeypatch: MonkeyPatch,
    mock_class: str,
    method: Any,  # return value in this case
    return_value: bool,  # as_property in this case
) -> CallList: ...


def _mp_call(  # type: ignore
    monkeypatch: MonkeyPatch,
    mock_class: type[Any] | ModuleType | str,
    method: str | Any,
    return_value: Any,
    as_property: bool = False,
) -> CallList:
    """
    Mock a method in a class and record the calls to it.

    If the given return_value is an Exception, it will be raised. If not, the
    value will be returned from the mocked function/method.
    """
    calls: CallList = []

    def func_call(*a: Any, **k: Any) -> Any:
        """Mock the function call."""
        calls.append((a, k))
        if isinstance(return_value, Exception):
            # bug in pylint https://www.logilab.org/ticket/3207
            raise return_value  # pylint: disable-msg=raising-bad-type
        return (
            return_value(*a, **k) if callable(return_value) else return_value
        )

    # first case handles class + method, second one mock as str
    if as_property or (isinstance(mock_class, str) and return_value):
        callback: Callable[[VarArg(Any), KwArg(Any)], Any] | property = (
            property(func_call)
        )
    else:
        callback = func_call

    if isinstance(mock_class, str):
        return_value = method
        monkeypatch.setattr(mock_class, callback)
    else:
        monkeypatch.setattr(mock_class, method, callback)
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
def mock_qute_message_dialog(
    title: str,
    text: str,
    parent: QWidget,
    method: str = "warning",
    return_value: QMessageBox.StandardButton | None = None,
) -> Generator[None, None, None]:
    """
    Mock the QuteMessageBox call of a method in a context.

    Same method as mock_q_message_dialog. Must be reimplemented for typing.
    """
    if method != "question" and return_value is not None:
        raise ValueError(
            f"Cannot return anything from methods other than question. Given "
            f"method type: '{method}' and return value: {return_value}"
        )

    monkeypatch = MonkeyPatch()
    calls = _mp_message_dialog(
        monkeypatch, method, return_value, QuteMessageBox
    )
    yield
    _check_mp_dialog(calls, parent, title, text)
    monkeypatch.undo()


@contextlib.contextmanager
def check_call(  # noqa: PLR0913
    mock_class: type[Any] | ModuleType,
    method: str,
    return_value: Any = None,
    call_args_list: list[tuple[Any, ...]] | None = None,
    call_kwargs_list: list[dict[str, Any]] | None = None,
    call_count: int = 1,
    as_property: bool = False,
) -> Generator[CallList, None, None]:
    """
    Context manager for mocking and checking a call to a method.

    If called is greater 0, and call_args and call_kwargs are given, the
    context manager will check that the call to the mocked method was done with
    those arguments. Also, it will assert that the mock was called exactly
    once.

    If called is False, it will assert that the mock was not called.

    If a return_value is given, the mock will return this value. One can pass
    as exception that will be raised by the mocked method instead of returning
    a value. If a Callable is passed, it will be called and its return value
    returned.
    """
    assert (call_args_list is not None and call_kwargs_list is not None) or (
        call_args_list is None and call_kwargs_list is None
    ), (
        "call_args and call_kwargs must be None or have a value "
        "(list/dict if empty)"
    )
    monkeypatch = MonkeyPatch()
    calls: CallList = _mp_call(  # type: ignore
        monkeypatch, mock_class, method, return_value, as_property
    )
    yield calls
    m_name = f"{mock_class.__name__}.{method}"
    assert_calls(call_count, call_args_list, call_kwargs_list, calls, m_name)
    monkeypatch.undo()


# Duplicate the code because overloading is a mess due to this bug:
# https://github.com/python/mypy/issues/11373
@contextlib.contextmanager
def check_call_str(  # noqa: PLR0913
    mock_class: str,
    return_value: Any = None,
    call_args_list: list[tuple[Any, ...]] | None = None,
    call_kwargs_list: list[dict[str, Any]] | None = None,
    call_count: int = 1,
    as_property: bool = False,
) -> Generator[CallList, None, None]:
    """
    Context manager for mocking and checking a call to a method.

    See `check_call` documentation.
    """
    assert (call_args_list is not None and call_kwargs_list is not None) or (
        call_args_list is None and call_kwargs_list is None
    ), (
        "call_args and call_kwargs must be None or have a value "
        "(list/dict if empty)"
    )
    monkeypatch = MonkeyPatch()
    calls: CallList = _mp_call(  # type: ignore
        monkeypatch, mock_class, return_value, as_property
    )
    yield calls
    m_name = mock_class
    assert_calls(call_count, call_args_list, call_kwargs_list, calls, m_name)
    monkeypatch.undo()


def assert_calls(
    call_count: int,
    call_args_list: list[tuple[Any, ...]] | None,
    call_kwargs_list: list[dict[str, Any]] | None,
    calls: CallList,
    m_name: str,
) -> None:
    """Check that the calls made to the mocked function are correct."""
    if call_count != -1:
        assert (
            len(calls) == call_count
        ), f"Expected {call_count} calls to {m_name} but got: {len(calls)}"
    if call_args_list and call_kwargs_list:
        for idx, call_args in enumerate(call_args_list):
            assert (
                call_args == calls[idx][0]
            ), f"Args to {m_name}: {call_args} expected: {call_args}"
        for idx, call_kwargs in enumerate(call_kwargs_list):
            assert (
                call_kwargs == calls[idx][1]
            ), f"Kwargs to {m_name}: {call_kwargs} expected: {call_kwargs}"
