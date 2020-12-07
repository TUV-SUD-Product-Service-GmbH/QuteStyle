"""Common db stuff."""
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
