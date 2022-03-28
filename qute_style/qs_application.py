"""QuteStyleApplication."""
from __future__ import annotations

import logging
import operator
from copy import copy
from typing import List, Type, cast

from PyQt5 import QtCore
from PyQt5.QtCore import QRectF, QSize, Qt, pyqtSlot
from PyQt5.QtGui import (
    QCloseEvent,
    QColor,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPixmap,
)
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QMainWindow,
    QSplashScreen,
)

from qute_style.helper import check_ide, create_waiting_spinner
from qute_style.startup_threads import StartupThread
from qute_style.style import get_color, get_style
from qute_style.update_window import AppData, TSLMainWindow

log = logging.getLogger(
    f"qute_style.{__name__}"
)  # pylint: disable=invalid-name


class CustomSplashScreen(QSplashScreen):
    """Custom Splash screen for startup of app."""

    def __init__(self, app_data: AppData):
        """Init CustomSplashScreen."""
        super().__init__()
        style_sheet = get_style()
        self.setStyleSheet(style_sheet)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        background_color = get_color("bg_one")
        # use a pixmap as background
        size = QSize(350, 200)
        self.setFixedSize(size)
        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        path = QPainterPath()
        path.addRoundedRect(QRectF(0, 0, size.width(), size.height()), 12, 12)
        painter.fillPath(path, QColor(background_color))
        painter.end()
        # working solution to get the rounded corners to a splash screen
        self.setPixmap(pixmap)
        grid_layout = QGridLayout(self)
        grid_layout.setAlignment(Qt.AlignHCenter)
        logo_svg = QSvgWidget(app_data.app_splash_icon, self)
        logo_svg.setFixedSize(QSize(140, 140))
        grid_layout.addWidget(logo_svg, 0, 0, 1, 0, alignment=Qt.AlignCenter)
        grid_layout.addWidget(
            QLabel(f"Starting {app_data.app_name}. Please wait", self), 1, 0
        )
        label = QLabel(self)
        label.setFixedSize(30, 30)
        self._spinner = create_waiting_spinner(label, 18, 10, 5)
        self._spinner.start()
        grid_layout.addWidget(label, 1, 1)

    def closeEvent(  # pylint: disable=invalid-name
        self, close_event: QCloseEvent
    ) -> None:
        """Handle close event."""
        self._spinner.stop()
        super().closeEvent(close_event)

    def mousePressEvent(  # pylint: disable=invalid-name
        self, event: QMouseEvent
    ) -> None:
        """Disable default "click-to-dismiss" behaviour."""


class QuteStyleApplication(  # pylint: disable=too-many-instance-attributes
    QApplication
):
    """QuteStyleApplication."""

    MAIN_WINDOW_CLASS: Type[TSLMainWindow]

    STARTUP_THREADS: List[Type[StartupThread]] = []

    APP_DATA: AppData

    def __init__(self, argv: List[str], show_splash: bool = True):
        """Init QuteStyleApplication."""
        super().__init__(argv)

        self._update = "-u" not in argv and not check_ide()
        self._force_whats_new = "-w" in argv
        self._reset_settings = "-c" in argv

        self.check_startup_thread_configuration()
        self.setApplicationName(self.APP_DATA.app_name)
        self.setOrganizationName("Sample Organization")
        self.setOrganizationDomain("sample_organization.com")
        if show_splash:
            self._splash_screen: QSplashScreen | None = CustomSplashScreen(
                self.APP_DATA
            )
            self._splash_screen.show()
        else:
            self._splash_screen = None
        self._main_window: QMainWindow | None = None

        self._threads_to_run: List[Type[StartupThread]] = copy(
            self.STARTUP_THREADS
        )
        self._handle_startup_threads()

    def check_startup_thread_configuration(self) -> None:
        """
        Check the configuration of the startup threads.

        In case exit application function is overriden check for a unique
        priority of EXIT_FUNCTION_PRIORITY.
        """
        thread_priorities: List[int] = []
        for thread in self.STARTUP_THREADS:
            if id(StartupThread.exit_application) != id(
                thread.exit_application
            ):
                assert (
                    thread.EXIT_FUNCTION_PRIORITY > 0
                ), "EXIT_FUNCTION_PRIORITY of startup threads must be > 0"
                assert (
                    thread.EXIT_FUNCTION_PRIORITY not in thread_priorities
                ), "EXIT_FUNCTION_PRIORITY of startup threads must be unique"
                thread_priorities.append(thread.EXIT_FUNCTION_PRIORITY)

    def _handle_startup_threads(self) -> None:
        """Handle startup threads if any."""
        # reimplement this method to handle starting threads or for
        # example removing threads before start
        self.show_main_window()

    def _run_threads(self) -> None:
        """Start processing the startup threads."""
        for thread_class in copy(self._threads_to_run):
            log.debug("Preparing thread to start: %s", thread_class)

            threads_finished = [
                thread.__class__ for thread in self._threads_finished
            ]
            if any(
                dependency not in threads_finished
                for dependency in thread_class.START_DEPENDS_ON
            ):
                log.debug("Cannot run thread, dependencies not met")
                continue
            thread = thread_class(self.APP_DATA)
            self._threads_running.append(thread)
            self._threads_to_run.remove(thread_class)
            thread.finished.connect(self.on_finished_thread)
            thread.start()
            log.debug("Thread starting: %s", thread)

    @pyqtSlot(name="on_finished_thread")
    def on_finished_thread(self) -> None:
        """Handle a finished StartupThread."""
        thread = cast(StartupThread, self.sender())
        log.debug("Thread finished: %s", thread)
        self._threads_running.remove(thread)
        self._threads_finished.append(thread)
        if thread.exit_application:
            # clear all threads which are not started yet in case a thread
            # with exit is ended
            self._threads_to_run.clear()
        if not self._threads_running and not self._threads_to_run:
            # all running threads have finished. Check if there are threads
            # that exits the app
            exit_threads = [
                thread
                for thread in self._threads_finished
                if thread.exit_application
            ]
            # sort by EXIT_FUNCTION_PRIORITY
            exit_threads.sort(
                key=operator.attrgetter("EXIT_FUNCTION_PRIORITY")
            )
            self._threads_finished.clear()
            if exit_threads:
                log.debug("Running threads post process, Exit application.")
                exit_threads[0].exit_function()
                self.quit()
            else:
                log.debug(
                    "There are no threads left to run, "
                    "starting QuteStyleMainWindow."
                )
                self.show_main_window()
        else:
            log.debug("Threads still to run: %s", self._threads_to_run)
            log.debug("Thread currently running: %s", self._threads_running)
            self._run_threads()

    def show_main_window(self) -> None:
        """Show the main window."""
        self._main_window = self.MAIN_WINDOW_CLASS(
            self.APP_DATA, self._force_whats_new, self._reset_settings
        )
        if self._splash_screen:
            self._splash_screen.finish(self._main_window)
        self._main_window.show()
