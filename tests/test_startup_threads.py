"""Tests for startup threads."""
import pytest
import sqlalchemy

from tsl.dev.mocks import check_call
from tsl.startup_threads import (
    CheckDBConnectionThread,
    CheckEdocDBConnectionThread,
    StartupThread,
)
from tsl.tsl_message_box import TSLMessageBox
from tsl.update_window import AppData
from tsl.vault import Vault

# pylint: disable=protected-access


@pytest.fixture(name="edoc_conn_thread", scope="function")
def fixture_edoc_conn_thread() -> CheckDBConnectionThread:
    """Create and return an CheckDBConnectionThread."""
    return CheckEdocDBConnectionThread(
        AppData("Test-App", "1.2.3"),
    )


def test_edoc_conn_thread(
    edoc_conn_thread: CheckDBConnectionThread,
) -> None:
    """Test edoc_connection_thread."""
    assert edoc_conn_thread.app_data.app_name == "Test-App"
    assert edoc_conn_thread.app_data.app_version == "1.2.3"
    assert edoc_conn_thread.EXIT_FUNCTION_PRIORITY == 2
    assert edoc_conn_thread._db_conn_state is False
    assert isinstance(edoc_conn_thread, StartupThread)


@pytest.mark.parametrize("db_conn_state", (True, False))
def test_edoc_conn_exit_func(
    edoc_conn_thread: CheckDBConnectionThread, db_conn_state: bool
) -> None:
    """Test edoc_connection_thread exit function."""
    edoc_conn_thread._db_conn_state = db_conn_state
    assert edoc_conn_thread.exit_application is not db_conn_state


def test_edoc_conn_exec_func(
    edoc_conn_thread: CheckDBConnectionThread,
) -> None:
    """Test the execution function."""
    with check_call(
        sqlalchemy.engine.base.Engine,
        "connect",
        sqlalchemy.engine.base.Connection,
    ):
        with check_call(sqlalchemy.engine.base.Connection, "close", None):
            edoc_conn_thread._function_to_execute()
            assert edoc_conn_thread._db_conn_state is True


@pytest.mark.parametrize(
    "exception",
    [
        sqlalchemy.exc.OperationalError("", "", ""),
        sqlalchemy.exc.InterfaceError("", "", ""),
        Exception(),
    ],
)
def test_edoc_conn_exec_func_exception(
    edoc_conn_thread: CheckDBConnectionThread,
    exception: Exception,
) -> None:
    """Test the execution function with raising exception."""
    with check_call(sqlalchemy.engine.base.Engine, "connect", exception):
        edoc_conn_thread._function_to_execute()
        assert edoc_conn_thread._db_conn_state is False


def test_exit_function(edoc_conn_thread: CheckDBConnectionThread) -> None:
    """Test the exit function."""
    with check_call(TSLMessageBox, "critical", None) as call:
        db_name = Vault._get_name(
            Vault.Application.EDOC, Vault.Environment.DEV
        )
        edoc_conn_thread._db_conn_error = "Test"
        edoc_conn_thread.exit_function()
        assert call[0][0][1] == f"Error Database connection: {db_name}"
        assert call[0][0][2] == "Test"
