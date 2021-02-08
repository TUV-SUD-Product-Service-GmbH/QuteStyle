"""Common db stuff."""
import cProfile
import contextlib
import io
import pstats
from typing import Optional, TYPE_CHECKING

from sqlalchemy import TypeDecorator, Unicode
from sqlalchemy.engine import Dialect


# add typing that is used only when running type check
# this does not work during normal execution
if TYPE_CHECKING:
    StrEngine = TypeDecorator[str]  # noqa
else:
    StrEngine = TypeDecorator


# pylint: disable=abstract-method
class NullUnicode(StrEngine):
    """
    Handles NULL values for strings like empty strings.

    Please note that Column definitions must (and also should) always include
    the following: nullable=False, default="".
    """

    impl = Unicode

    # pylint: disable=no-self-use
    def process_result_value(self, value: Optional[str], _: Dialect) -> str:
        """Return the value or an empty str if the value is None (NULL)."""
        return value or ""


@contextlib.contextmanager  # type: ignore
def profiled() -> None:  # type: ignore
    """Print profile information about a code block."""
    profile = cProfile.Profile()
    profile.enable()
    yield
    profile.disable()
    string = io.StringIO()
    process = pstats.Stats(profile, stream=string).sort_stats('cumulative')
    process.print_stats()
    # uncomment this to see who's calling what
    # ps.print_callers()
    print(string.getvalue())
