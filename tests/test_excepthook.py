"""Test for the excepthook."""
# pylint: disable=too-few-public-methods
import traceback
from types import TracebackType
from typing import cast

import tsl
from tsl.dev.mocks import check_call
from tsl.init import excepthook


class TestException(BaseException):
    """TestException."""


class FakeTraceback:
    """FakeTraceback."""


def test_excepthook() -> None:
    """Check that the excepthook opens a QMessageBox with correct args."""
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
