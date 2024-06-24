"""Tests for QS application."""

from copy import copy

import pytest
from PySide6.QtCore import QEventLoop, QThread, QTimer
from PySide6.QtWidgets import QApplication

from qute_style.dev.mocks import check_call
from qute_style.qs_application import QuteStyleApplication
from qute_style.startup_threads import StartupThread


# pylint: disable=protected-access
class SampleThread1(StartupThread):
    """Dummy thread for tests."""

    def _function_to_execute(self) -> None:
        """Thread run."""


class SampleThread2(StartupThread):
    """Dummy thread for tests."""

    def _function_to_execute(self) -> None:
        """Thread run."""


class SampleThread3(StartupThread):
    """Dummy thread for tests with dependency."""

    START_DEPENDS_ON = (SampleThread1, SampleThread2)

    def _function_to_execute(self) -> None:
        """Thread run."""


class SampleThread4(StartupThread):
    """Dummy thread for tests with exit function."""

    EXIT_FUNCTION_PRIORITY = 2

    def _function_to_execute(self) -> None:
        """Thread run."""

    @property
    def exit_application(self) -> bool:
        """Thread run."""
        return True


class SampleThread5(StartupThread):
    """Dummy thread for tests with exit function."""

    EXIT_FUNCTION_PRIORITY = 1

    def _function_to_execute(self) -> None:
        """Thread run."""

    @property
    def exit_application(self) -> bool:
        """Thread run."""
        return True


class SampleThread6(StartupThread):
    """Dummy thread for tests with exit function."""

    def _function_to_execute(self) -> None:
        """Thread run."""

    @property
    def exit_application(self) -> bool:
        """Thread run."""
        return True


def test_qs_application(
    qapp: QuteStyleApplication,
) -> None:
    """Test qs app."""
    assert qapp.APP_DATA.app_name == "Test-App"
    assert qapp.APP_DATA.app_version == "2.3.4"
    assert not qapp.STARTUP_THREADS


def test_startup_thread_configuration_with_same_prio(
    qapp: QuteStyleApplication,
) -> None:
    """Test startup configuration."""
    with pytest.raises(AssertionError) as err:
        qapp.STARTUP_THREADS = [SampleThread4, SampleThread4]
        qapp.check_startup_thread_configuration()
    assert (
        err.value.args[0]
        == "EXIT_FUNCTION_PRIORITY of startup threads must be unique"
    )


def test_startup_thread_configuration_with_prio_0(
    qapp: QuteStyleApplication,
) -> None:
    """Test startup configuration."""
    with pytest.raises(AssertionError) as err:
        qapp.STARTUP_THREADS = [SampleThread6]
        qapp.check_startup_thread_configuration()
    assert (
        err.value.args[0]
        == "EXIT_FUNCTION_PRIORITY of startup threads must be > 0"
    )


def restart_app_instance(
    qapp: QuteStyleApplication, startup_threads: list[type[StartupThread]]
) -> None:
    """Reset the given QApp instance to reset ."""
    qapp.STARTUP_THREADS = startup_threads
    qapp._threads_to_run = copy(qapp.STARTUP_THREADS)
    qapp._threads_running = []
    qapp._threads_finished = []
    qapp._run_threads()


def test_threading(qapp: QuteStyleApplication) -> None:
    """Test threading."""
    restart_app_instance(qapp, [SampleThread1, SampleThread2])
    # need the loop here to handle the finished signal
    loop = QEventLoop()
    QTimer.singleShot(2000, loop.quit)
    loop.exec()
    assert not qapp._threads_to_run


def test_run_threads_function(qapp: QuteStyleApplication) -> None:
    """Test run threads function."""
    with check_call(QThread, "start", None, call_count=2):
        restart_app_instance(qapp, [SampleThread1, SampleThread2])
        assert len(qapp._threads_running) == 2
        assert not qapp._threads_to_run


def test_threads_with_dependency(qapp: QuteStyleApplication) -> None:
    """
    Test run threads function with dependencies.

    Thread 3 has a dependency to SampleThread1 and SampleThread2.
    In order to run, SampleThread1 and SampleThread2 must be finished first.
    """
    with check_call(QThread, "start", None, call_count=3):
        restart_app_instance(
            qapp, [SampleThread1, SampleThread2, SampleThread3]
        )
        assert len(qapp._threads_running) == 2
        assert isinstance(qapp._threads_running[0], SampleThread1)
        assert isinstance(qapp._threads_running[1], SampleThread2)
        assert len(qapp._threads_to_run) == 1
        assert qapp._threads_to_run[0] is SampleThread3

        # now set thread1 to finished
        # still thread3 is not started due to dependency on thread 2
        qapp._threads_running[0].finished.emit()
        assert len(qapp._threads_running) == 1
        assert isinstance(qapp._threads_running[0], SampleThread2)
        assert len(qapp._threads_to_run) == 1
        assert qapp._threads_to_run[0] is SampleThread3

        # now set thread2 to finished. Thread 3 is now able to start
        qapp._threads_running[0].finished.emit()
        assert len(qapp._threads_running) == 1
        assert isinstance(qapp._threads_running[0], SampleThread3)
        assert not qapp._threads_to_run


def test_exit_function(qapp: QuteStyleApplication) -> None:
    """Test exit function call."""
    # sample thread 5 has a lower priority than SampleThread4.
    # Thus it's exit function is called
    with check_call(QThread, "start", None, call_count=2), check_call(
        QApplication, "quit", None, call_count=1
    ), check_call(SampleThread5, "exit_function", None, call_count=1):
        restart_app_instance(qapp, [SampleThread4, SampleThread5])
        assert len(qapp._threads_running) == 2
        assert not qapp._threads_to_run
        qapp._threads_running[0].finished.emit()
        qapp._threads_running[0].finished.emit()
