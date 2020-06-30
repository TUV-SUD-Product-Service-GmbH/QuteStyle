"""Tests for tsl.helper."""
import pytest

from tsl.helper import get_project_path, get_process_path


def test_check_project_path() -> None:
    """Test getting a project path works as expected."""
    assert get_project_path(1234575) == \
        r'\\de001.itgr.net\PS\RF-UnitCentralPS_' \
        r'PSE\CPS\Projects\2018\1234575'


def test_check_project_path_fail() -> None:
    """Test getting a project path works as expected."""
    with pytest.raises(ValueError):
        get_project_path(1234567)


def test_check_process_path() -> None:
    """Test getting a project path works as expected."""
    assert get_process_path(20000) == \
        r'\\de001.itgr.net\PS\RF-UnitCentralPS_' \
        r'PSE\CPS\PSEX\Prozesse\2015\20000'


def test_check_process_path_fail() -> None:
    """Test getting a project path works as expected."""
    with pytest.raises(ValueError):
        get_project_path(9999999)
