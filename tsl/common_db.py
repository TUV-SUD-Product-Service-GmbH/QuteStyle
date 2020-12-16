"""Common db stuff."""
import cProfile
import contextlib
import io
import pstats
from typing import Optional

from sqlalchemy import TypeDecorator, Unicode
from sqlalchemy.engine import Dialect


# pylint: disable=abstract-method
class NullUnicode(TypeDecorator):
    """Handles NULL values for strings like empty strings."""

    impl = Unicode

    def process_bind_param(self, value: Optional[str], _: Dialect)\
            -> Optional[str]:
        """Write always NULL to the db if the string is empty."""
        return value if value else None

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
