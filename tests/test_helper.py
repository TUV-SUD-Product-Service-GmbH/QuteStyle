"""Test helper methods."""
import sys

import pytest

from qute_style.helper import check_ide


@pytest.mark.parametrize(
    "path,result",
    (
        (r"C:\test\test.exe", False),
        (r"C:\test\test", False),
        (r"C:\test\test.py", True),
    ),
)
def test_check_ide(path: str, result: bool) -> None:
    """Test that the check_ide method returns the correct result."""
    old_path = sys.argv[0]
    sys.argv[0] = path
    assert check_ide() == result
    sys.argv[0] = old_path
