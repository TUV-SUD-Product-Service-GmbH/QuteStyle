"""Tests for tsl.helper."""
import pytest

from tsl.pse_database import session_scope, Project, Process
from tsl.helper import get_project_path, get_process_path


def test_check_project_path() -> None:
    """Test getting a project path works as expected."""
    with session_scope() as session:
        session.add(
            Project(
                P_ID=1234575,
                P_FOLDER=r"Projects\2018\1234575",
                P_WC_ID="BB8E7738-0ACB-423C-8626-18AA3355B8FF",
            )
        )
        session.add(
            Project(
                P_ID=1504436,
                P_FOLDER=r"Projects\2020\1504436",
                P_WC_ID="BB8E7738-0ACB-423C-8626-18AA3355B8FF",
            )
        )
    assert (
        get_project_path(1234575) == r"\\de001.itgr.net\PS\RF-UnitCentralPS_"
        r"PSE\CPS\Projects\2018\1234575"
    )
    assert (
        get_project_path(1504436) == r"\\de001.itgr.net\PS\RF-UnitCentralPS_"
        r"PSE\CPS\Projects\2020\1504436"
    )


def test_check_project_path_fail() -> None:
    """Test getting a project path works as expected."""
    with pytest.raises(ValueError):
        get_project_path(1234567)


def test_check_process_path() -> None:
    """Test getting a project path works as expected."""
    with session_scope() as session:
        session.add(Process(PC_ID=20000, PC_PATH=r"Prozesse\2015\20000"))
    assert (
        get_process_path(20000) == r"\\de001.itgr.net\PS\RF-UnitCentralPS_"
        r"PSE\CPS\PSEX\Prozesse\2015\20000"
    )


def test_check_process_path_fail() -> None:
    """Test getting a project path works as expected."""
    with pytest.raises(ValueError):
        get_project_path(9999999)
