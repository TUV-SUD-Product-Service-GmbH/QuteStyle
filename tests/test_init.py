"""Test init methods."""
import sys
from pathlib import Path

import pytest

from tsl.init import check_ide


@pytest.mark.parametrize(
    "path,result",
    (
        (Path(r"C:\test\test.exe"), False),
        (Path(r"C:\test\test"), False),
        (Path(r"C:\test\test.py"), True),
    ),
)
def test_check_ide(path: Path, result: bool) -> None:
    """Test that the check_ide method returns the correct result."""
    sys.argv[0] = path  # type: ignore
    assert check_ide() == result
