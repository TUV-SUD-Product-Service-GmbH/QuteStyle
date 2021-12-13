"""Test for the excepthook."""
import traceback
from types import TracebackType
from typing import cast

import tsl
from tests.mocks import check_call
from tsl.init import excepthook


class TestException(BaseException):
    pass


class FakeTraceback:
    pass


def test_excepthook() -> None:
    test_ex = TestException("Help, I failed!")
    with check_call(traceback, "format_tb", return_value=["TestTraceBack"]):
        with check_call(tsl.init, "error_message_box") as call:
            trace_back = cast(TracebackType, FakeTraceback())
            excepthook(test_ex.__class__, test_ex, trace_back)
            assert (
                call[0][0][0]
                == "<class 'tests.test_excepthook.TestException'>: "
                   "Help, I failed!"
            )
            assert call[0][0][1] == "TestTraceBack\n"
