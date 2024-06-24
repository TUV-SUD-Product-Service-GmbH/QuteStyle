"""QuteStyleMainWindow definition for custom Darcula style."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TypeVar, cast

from PySide6.QtCore import (
    QByteArray,
    QEasingCurve,
    QLocale,
    QParallelAnimationGroup,
    QPoint,
    QPropertyAnimation,
    QRect,
    QSettings,
    QSize,
    Qt,
    Signal,
    Slot,
)
from PySide6.QtGui import QCloseEvent, QMouseEvent, QResizeEvent, QShowEvent
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLayout,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

import qute_style.resources_rc  # pylint: disable=unused-import  # noqa: F401
from qute_style.qute_style import QuteStyle
from qute_style.style import get_style, set_current_style
from qute_style.widgets.background_frame import BackgroundFrame
from qute_style.widgets.base_widgets import BaseWidget, MainWidget
from qute_style.widgets.credit_bar import CreditBar
from qute_style.widgets.grips import CornerGrip, EdgeGrip
from qute_style.widgets.home_page import HomePage
from qute_style.widgets.left_column import LeftColumn
from qute_style.widgets.left_menu import LeftMenu
from qute_style.widgets.title_bar import TitleBar

log = logging.getLogger(
    f"qute_style.{__name__}"
)  # pylint: disable=invalid-name


@dataclass
class AppData:  # pylint: disable=too-many-instance-attributes
    """Provide required data to startup threads."""

    app_name: str = ""
    app_version: str = ""
    app_icon: str = ""
    app_splash_icon: str = ""
    help_text: str = ""
    debug_text: str = ""
    organization_name: str = ""
    organization_domain: str = ""


class CustomMainWindow(QMainWindow):
    """Base Main window class."""

    def __init__(
        self,
        app_data: AppData,
        # force_whats_new, legacy parameter for backward compatibility
        # not required for qute style apps
        force_whats_new: bool = False,
        registry_reset: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        """Create a new QuteStyleMainWindow."""
        super().__init__(parent)
        self._app_data = app_data
        self._force_whats_new: bool = force_whats_new
        if registry_reset:
            log.debug("Resetting QSettings in Registry.")
            QSettings().clear()


class QuteStyleMainWindow(
    # pylint: disable=too-many-instance-attributes, too-many-public-methods
    CustomMainWindow
):
    """QuteStyleMainWindow definition for custom Darcula style."""

    # Widgets that will be shown in the center content and which are
    # accessible from the main menu on the left side.
    MAIN_WIDGET_CLASSES: list[type[MainWidget]]

    # Widgets that are shown in the right column.
    RIGHT_WIDGET_CLASSES: list[type[BaseWidget]]

    # Widgets that are shown in the left column.
    LEFT_WIDGET_CLASSES: list[type[BaseWidget]]

    MIN_SIZE: QSize = QSize(0, 0)

    # Define the maximum width for the columns (left and right).
    MAX_COLUMN_WIDTH = 240

    # Signal that is emitted when the window has shut down.
    shutdown_complete = Signal(name="shutdown_complete")

    LANG_CODE: str | None = None

    def __init__(  # noqa: PLR0913
        self,
        app_data: AppData,
        force_whats_new: bool = False,
        registry_reset: bool = False,
        load_last_used_widget: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        """Create a new QuteStyleMainWindow."""
        super().__init__(app_data, force_whats_new, registry_reset, parent)

        QApplication.setStyle(QuteStyle())
        QApplication.setPalette(QApplication.style().standardPalette())

        # Set the global stylesheet.
        self.set_style()

        # Stores the position of the last clicked (needed for moving)
        self.last_move_pos = QPoint()

        # This is the animation group for hiding/showing the columns
        # (left/right). It needs to be globally defined to avoid being garbage
        # collected (which would stop the animation).
        self._group = QParallelAnimationGroup()

        # Configure the StyledMainWindow
        self._configure_main_window()

        # Add a central QWidget with a layout
        self.setCentralWidget(QWidget())
        central_widget_layout = QVBoxLayout(self.centralWidget())

        # Add the main QFrame that contains the background style.
        self._background = BackgroundFrame(self)
        central_widget_layout.addWidget(self._background)

        # Get widgets to set visible
        self._visible_widgets = self._get_widgets_to_display(
            self.MAIN_WIDGET_CLASSES
        )

        # Add the left menu.
        self._left_menu = self._add_left_menu(self._background.layout())

        # Add the left column.
        self._left_column_frame, self._left_column = self._add_left_column(
            self._background.layout()
        )

        # Add the main frame that contains title and credit bar as well as
        # the main content and the right column.
        right_app_frame = QFrame()
        right_app_layout = QVBoxLayout(right_app_frame)
        right_app_layout.setContentsMargins(3, 5, 5, 5)
        right_app_layout.setSpacing(6)
        self._background.layout().addWidget(right_app_frame)

        # Add the title bar to the main frame
        self._title_bar = self._add_title_bar(right_app_layout)

        # Add main content and right column to the main frame
        (
            self._right_column_frame,
            self._right_content,
            self._content,
        ) = self._add_main_area(right_app_layout)

        # Add credit bar to the main frame
        right_app_layout.addWidget(CreditBar(self._app_data.app_version))

        self._grips: list[EdgeGrip | CornerGrip] = [
            EdgeGrip(self, Qt.Edge.LeftEdge),
            EdgeGrip(self, Qt.Edge.RightEdge),
            EdgeGrip(self, Qt.Edge.TopEdge),
            EdgeGrip(self, Qt.Edge.BottomEdge),
            CornerGrip(self, Qt.Corner.TopLeftCorner),
            CornerGrip(self, Qt.Corner.TopRightCorner),
            CornerGrip(self, Qt.Corner.BottomLeftCorner),
            CornerGrip(self, Qt.Corner.BottomRightCorner),
        ]
        for grip in self._grips:
            grip.window_geometry_changed.connect(self.window_geometry_changed)
        startup_widget: type[MainWidget] | None = None
        last_used_widget = QSettings().value("last_used_widget")
        if (
            load_last_used_widget
            and last_used_widget
            and last_used_widget in self.MAIN_WIDGET_CLASSES
        ):
            startup_widget = cast(type[MainWidget], last_used_widget)
        elif self.MAIN_WIDGET_CLASSES:
            # Activate the first widget to be visible by default.
            startup_widget = self.MAIN_WIDGET_CLASSES[0]
        if startup_widget:
            self.on_main_widget(startup_widget)

    MainWidgetT = TypeVar("MainWidgetT", bound=MainWidget)

    def show(self) -> None:
        """Override show to start update just before."""
        self._load_settings()
        super().show()

    def _load_settings(self) -> None:
        """Load geometry and state settings of the ui."""
        log.debug("Loading settings from registry")
        settings = QSettings()
        try:
            self.restoreGeometry(cast(QByteArray, settings.value("geometry")))
        except TypeError:
            log.warning(
                "Could not restore geometry from: %s",
                settings.value("geometry"),
            )
        try:
            self.restoreState(cast(QByteArray, settings.value("state")))
        except TypeError:
            log.warning(
                "Could not restore state from: %s", settings.value("state")
            )

    def get_main_widget(self, widget: type[MainWidgetT]) -> MainWidgetT | None:
        """Get main widget from content."""
        return self._content.findChild(widget)  # type: ignore[return-value]

    @Slot(QRect, name="window_geometry_changed")
    def window_geometry_changed(self, geometry: QRect) -> None:
        """Handle change of window geometry by using the grips."""
        self.setGeometry(geometry)

    WidgetT = TypeVar("WidgetT", MainWidget, BaseWidget)

    @classmethod
    def get_app_language(cls) -> str:
        """Get the currently set language to use for the ui."""
        if not cls.LANG_CODE:
            sys_lang = QLocale().system().name()[:2]
            cls.LANG_CODE = cast(str, QSettings().value("lang", sys_lang))
            assert isinstance(cls.LANG_CODE, str)
        return cls.LANG_CODE

    @staticmethod
    def _get_widgets_to_display(
        widgets: list[type[WidgetT]],
    ) -> list[type[WidgetT]]:
        """Reimplement to restrict access to certain widgets."""
        return widgets

    def _add_main_area(
        self, layout: QLayout
    ) -> tuple[QFrame, QStackedWidget, QStackedWidget]:
        """
        Add a Frame that contains the main content and the right column widget.

        The method creates a QFrame that contains two widgets:
        1. A QStackedWidget that contains all the widgets that are accessible
        from the menu (as defined in QuteMainGui.MAIN_WIDGET_CLASS
        2. A QFrame with the widget that is used as the right column.
        """
        content_area_frame = QFrame()
        content_area_layout = QHBoxLayout(content_area_frame)
        content_area_layout.setContentsMargins(0, 0, 0, 0)

        # Create the QStackedWidget that contains all the content widgets
        content = QStackedWidget()
        for widget_class in self._visible_widgets:
            if issubclass(widget_class, HomePage):
                widget = widget_class(
                    (
                        self._app_data.app_name,
                        self._app_data.app_icon,
                        QuteStyleMainWindow.get_app_language().lower(),
                    ),
                    self._visible_widgets,
                )
                content.addWidget(widget)
                widget.change_theme.connect(self.on_change_theme)
            else:
                content.addWidget(widget_class())
        content_area_layout.addWidget(content)

        # Add the QFrame to the given layout.
        layout.addWidget(content_area_frame)

        # Create and add the right column QFrame to the given layout.
        right_column_frame, right_content = self._add_right_column(
            content_area_layout
        )
        return right_column_frame, right_content, content

    def _add_right_column(
        self, layout: QLayout
    ) -> tuple[QFrame, QStackedWidget]:
        """
        Create a frame containing the right column widget and return it.

        This method creates a QFrame that is opened/closed with a button in the
        TitleBar. Therefore it's initial width is 0. The frame contains a
        layout with a margin of 5 pixels which contains the widget for the
        right column (as defined in QuteMainGui.RIGHT_WIDGET_CLASS).
        """
        right_column_frame = QFrame()
        right_column_frame.setObjectName("bg_two_frame")
        right_column_frame.setFixedWidth(0)
        content_area_right_layout = QVBoxLayout(right_column_frame)
        content_area_right_layout.setContentsMargins(5, 5, 5, 5)
        right_content = QStackedWidget()
        for widget in self._get_widgets_to_display(self.RIGHT_WIDGET_CLASSES):
            right_content.addWidget(widget())
        content_area_right_layout.addWidget(right_content)
        layout.addWidget(right_column_frame)
        return right_column_frame, right_content

    def _configure_main_window(self) -> None:
        """Configure the QuteStyleMainWindow."""
        # Set the name of the app.
        self.setWindowTitle(self._app_data.app_name)

        # Make the window borderless and transparent.
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Set the minimum overall size that is configured.
        self.setMinimumSize(self.MIN_SIZE)

    def _add_title_bar(self, right_app_layout: QLayout) -> TitleBar:
        """Add a TitleBar to the given QLayout."""
        title_bar = TitleBar(
            self,
            self.centralWidget(),
            self._get_widgets_to_display(self.RIGHT_WIDGET_CLASSES),
            self._app_data.app_name,
            self._app_data.app_icon,
            self._app_data.debug_text,
        )
        title_bar.close_app.connect(self.close)
        title_bar.minimize.connect(self.showMinimized)
        title_bar.maximize.connect(self.maximize)
        title_bar.move_window.connect(self.move_window)
        right_app_layout.addWidget(title_bar)
        title_bar.right_button_clicked.connect(self.on_right_column)
        return title_bar

    def _add_left_column(self, layout: QLayout) -> tuple[QFrame, LeftColumn]:
        """
        Add a QFrame and the LeftColumn to the given QLayout.

        This will create a QFrame on which the animation will be executed.
        Therefore the initial width is set to 0 (it's hidden). The LeftColumn
        is added into that frame without margins.
        """
        left_column_frame = QFrame()
        left_column_frame.setObjectName("_left_column_frame")
        left_column_frame.setFixedWidth(0)

        left_column_layout = QVBoxLayout(left_column_frame)
        left_column_layout.setContentsMargins(0, 0, 0, 0)

        left_column = LeftColumn(
            app_parent=self.centralWidget(),
            widget_types=self._get_widgets_to_display(
                self.LEFT_WIDGET_CLASSES
            ),
            parent=left_column_frame,
        )
        left_column_layout.addWidget(left_column)
        layout.addWidget(left_column_frame)
        left_column.close_column.connect(self.on_close_left_column)
        return left_column_frame, left_column

    def _add_left_menu(self, layout: QLayout) -> LeftMenu:
        """
        Add the left menu to the app.

        This method creates a LeftMenu which is exactly 50 Pixels wide. The
        LeftMenu is added into a QFrame with 3 Pixels margin on each side, so
        that the overall width is 56 Pixels. The height is adapted dynamically.

        The methods return the LeftMenu.
        """
        # add custom left menu bar
        left_menu_frame = QFrame()
        left_menu_layout = QHBoxLayout(left_menu_frame)
        left_menu_layout.setContentsMargins(3, 3, 3, 3)
        # add custom left menu
        left_menu = LeftMenu(
            parent=left_menu_frame,
            app_parent=self.centralWidget(),
            main_widgets=self._visible_widgets,
            left_column_widgets=self._get_widgets_to_display(
                self.LEFT_WIDGET_CLASSES
            ),
        )
        left_menu_layout.addWidget(left_menu)
        left_menu_frame.setFixedWidth(
            left_menu.minimumWidth()
            + left_menu_layout.contentsMargins().left()
            + left_menu_layout.contentsMargins().right()
        )
        layout.addWidget(left_menu_frame)
        left_menu.bottom_button_clicked.connect(self.on_left_column)
        left_menu.top_button_clicked.connect(self.on_main_widget)
        return left_menu

    def set_style(self) -> None:
        """Set the main stylesheet of the app."""
        self.setStyleSheet(get_style())

    @Slot(QPoint, name="move_window")
    def move_window(self, pos: QPoint) -> None:
        """
        Move the window.

        pos is the position at which the QMouseEvent triggering the move
        occurred.
        """
        if self.isMaximized():
            # Show the window normal
            self.showNormal()

            # Move the window so that the cursor is centered on the title bar.
            new_pos = pos - QPoint(
                int(self.width() / 2), int(self._title_bar.height() / 2)
            )
            self.move(new_pos)
        else:
            # Calculate the difference between the last click's position and
            # the new click position
            diff = pos - self.last_move_pos

            # Add the difference to the current position and move to
            # that position.
            self.move(self.pos() + diff)
        self.last_move_pos = pos

    @Slot(name="maximize")
    def maximize(self) -> None:
        """Handle a maximize request from the TitleBar."""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def showEvent(self, _: QShowEvent) -> None:  # noqa: N802
        """Listen to QShowEvents to get initial window state."""
        if self.isMaximized() or self.isFullScreen():
            log.debug("Window started in maximized/fullscreen mode")
            self._show_maximized_layout()
        else:
            self._show_normal_layout()

    def showFullScreen(self) -> None:  # noqa: N802
        """Overwrite showFullScreen."""
        log.debug("Show window fullscreen")
        self._show_maximized_layout()
        super().showFullScreen()

    def showMaximized(self) -> None:  # noqa: N802
        """Overwrite showMaximized."""
        log.debug("Show window maximized")
        self._show_maximized_layout()
        super().showMaximized()

    def showNormal(self) -> None:  # noqa: N802
        """Overwrite showNormal."""
        log.debug("Show window normal")
        self._show_normal_layout()
        super().showNormal()

    def _show_normal_layout(self) -> None:
        """
        Set the normal main window layout with rounded corners.

        This will add a margin for the contents of the main QLayout
        so that a shadow and the border with round edges is visible.
        This also adds the round borders on the main QFrame.
        """
        log.debug("window is in normal mode")
        self.centralWidget().layout().setContentsMargins(10, 10, 10, 10)
        self._background.set_stylesheet(border_radius=10, border_size=2)
        self._title_bar.set_maximized(False)

        # enable size change in normal mode
        for grip in self._grips:
            grip.setEnabled(True)

    def _show_maximized_layout(self) -> None:
        """
        Set the maximized main window layout without rounded corners.

        This removes the content margin so that the app fits
        exactly into the screen. Also, this removes the round
        borders from the main QFrame.
        """
        log.debug("window is in maximized/fullscreen mode")
        self.centralWidget().layout().setContentsMargins(0, 0, 0, 0)
        self._background.set_stylesheet(border_radius=0, border_size=0)
        self._title_bar.set_maximized(True)

        # size change is not possible in maximized mode
        for grip in self._grips:
            grip.setEnabled(False)

    def _column_is_visible(self, column: QFrame) -> bool:
        """Return if the given column is visible."""
        return (
            column.width() == self.MAX_COLUMN_WIDTH
            or self._check_is_opening(column) is True
        )

    def _check_is_opening(self, frame: QFrame) -> bool | None:
        """
        Check if the given QFrame is currently opening or closing.

        If the QFrame is opening, the method returns True, otherwise False.
        If no animation is in progress, the method returns None
        """
        if self._group.state() == QParallelAnimationGroup.State.Running:
            for idx in range(self._group.animationCount()):
                animation = cast(
                    QPropertyAnimation, self._group.animationAt(idx)
                )
                if animation.targetObject() is frame:
                    log.debug("Found animation for %s", frame)
                    opening = (
                        cast(int, animation.endValue())
                        == self.MAX_COLUMN_WIDTH
                    )
                    log.debug("Is currently opening: %s", opening)
                    return opening
        log.debug("There's no animation running for %s", frame)
        return None

    @staticmethod
    def _create_slide_animation(
        frame: QFrame, slide_out: bool
    ) -> QPropertyAnimation:
        """Create an animation that will open or close a QFrame."""
        animation = QPropertyAnimation(frame, b"minimumWidth")
        animation.setDuration(500)

        # Always start at the current width for the case that the column is
        # currently already animated and not fully closed/opened.
        animation.setStartValue(frame.width())
        animation.setEndValue(
            QuteStyleMainWindow.MAX_COLUMN_WIDTH if slide_out else 0
        )
        animation.setEasingCurve(QEasingCurve.Type.InOutQuart)
        return animation

    def _start_box_animation(self, left_open: bool, right_open: bool) -> None:
        """
        Animate slide in/out of left or right column.

        This method will clear an ongoing animation (group), and create a new
        one based on the request parameters and state of the columns.
        """
        assert not left_open or not right_open
        self._group.clear()

        # Create the two animations that that open/close the columns.
        self._group.addAnimation(
            self._create_slide_animation(self._left_column_frame, left_open)
        )
        self._group.addAnimation(
            self._create_slide_animation(self._right_column_frame, right_open)
        )

        self._group.start()

    def resizeEvent(self, event: QResizeEvent) -> None:  # noqa: N802
        """List to QResizeEvents to adapt position of grips."""
        super().resizeEvent(event)
        for grip in self._grips:
            grip.adapt()

    def mousePressEvent(self, event: QMouseEvent) -> None:  # noqa: N802
        """Event triggered on mouse button press."""
        self.last_move_pos = event.globalPosition().toPoint()
        log.debug("Storing last click at %s", self.last_move_pos)

    @Slot(type, name="on_main_widget")
    def on_main_widget(self, widget_class: type[MainWidget]) -> None:
        """Handle display of the main widget that is of the given type."""
        current_widget = cast(
            type[MainWidget],
            type(self._content.currentWidget()),
        )
        self._left_menu.set_button_active(current_widget, False)
        self._left_menu.set_button_active(widget_class, True)
        for idx in range(self._content.count()):
            widget = self._content.widget(idx)
            if isinstance(widget, widget_class):
                self._content.setCurrentWidget(widget)
                self._title_bar.title_bar_text = (
                    f"{self._app_data.app_name} - {widget.NAME}"
                )
                # show the individual settings widgets per main widget
                if self._column_is_visible(self._left_column_frame):
                    self._left_column.handle_settings_display(
                        widget.settings_widget, widget.ICON
                    )
                return
        raise ValueError(f"Could not find widget {widget_class}")

    @Slot(type, name="on_right_column")
    def on_right_column(self, widget_class: type[BaseWidget]) -> None:
        """Handle a click on the button for the right column."""
        right_widget_type = self.right_widget_type()
        left_widget_type = self._left_column.current_widget_type()

        # Set both buttons inactive (either a new column will be visible or
        # none)
        if right_widget_type:
            self._title_bar.set_button_active(right_widget_type, False)
        if left_widget_type:
            self._left_menu.set_button_active(left_widget_type, False)

        log.debug("Handling right column for %s", widget_class)

        # Check if switching the widget.
        visible = self._column_is_visible(self._right_column_frame)
        if widget_class != right_widget_type:
            # Set the current widget for the right column to make it visible.
            for idx in range(self._right_content.count()):
                if isinstance(self._right_content.widget(idx), widget_class):
                    self._right_content.setCurrentWidget(
                        self._right_content.widget(idx)
                    )

            # If the right column isn't visible, we start the animation.
            if not visible:
                self._start_box_animation(False, True)

            # Finally set the button for the widget active.
            self._title_bar.set_button_active(widget_class, True)

        # If toggling the active widget.
        else:
            # Start animation for the opposite state.
            self._start_box_animation(False, not visible)

            # Set the button to the opposite state.
            self._title_bar.set_button_active(widget_class, not visible)

    def right_widget_type(self) -> type[BaseWidget] | None:
        """Return the type of the right widget."""
        if widget := self._right_content.currentWidget():
            return cast(type[BaseWidget], type(widget))
        # Return None explicitly instead of <class NoneType>
        return None

    @Slot(type, name="on_left_column")
    def on_left_column(self, widget_class: type[BaseWidget]) -> None:
        """Handle a click on the button for the left column."""
        right_widget_type = self.right_widget_type()
        left_widget_type = self._left_column.current_widget_type()

        # Set both buttons inactive (either a new column will be visible or
        # none)
        if right_widget_type:
            self._title_bar.set_button_active(right_widget_type, False)
        if left_widget_type:
            self._left_menu.set_button_active(left_widget_type, False)

        log.debug("Handling left column for %s", widget_class)

        # Check if switching the widget.
        visible = self._column_is_visible(self._left_column_frame)
        if widget_class != left_widget_type:
            # Set the current widget for the left column to make it visible.
            self._left_column.set_column_widget(widget_class)

            # If the left column isn't visible, we start the animation.
            if not visible:
                self._start_box_animation(True, False)

            # Finally set the button for the widget active.
            self._left_menu.set_button_active(widget_class, True)

        # If toggling the active widget.
        else:
            # Start animation for the opposite state.
            self._start_box_animation(not visible, False)

            # Set the button to the opposite state.
            self._left_menu.set_button_active(widget_class, not visible)

        self._left_column.handle_settings_display(
            cast(MainWidget, self._content.currentWidget()).settings_widget,
            cast(MainWidget, self._content.currentWidget()).ICON,
        )

    @Slot(name="on_close_left_column")
    def on_close_left_column(self) -> None:
        """Handle a click on the button for the left column."""
        # if the column was opened before, a widget must be set.
        widget_class = cast(
            type[BaseWidget], self._left_column.current_widget_type()
        )
        self._left_menu.set_button_active(widget_class, False)
        self._start_box_animation(False, False)

    def _save_settings(self) -> None:
        """Save the paint data and state/geometry settings."""
        log.debug("Saving settings to registry.")
        settings = QSettings()
        settings.setValue("state", self.saveState())
        settings.setValue("geometry", self.saveGeometry())
        current_widget = cast(
            type[MainWidget],
            type(self._content.currentWidget()),
        )
        settings.setValue("last_used_widget", current_widget)
        log.debug("Finished writing settings to registry")

    @Slot(QCloseEvent, name="closeEvent")
    def closeEvent(self, close_event: QCloseEvent) -> None:  # noqa: N802
        """Handle a close event."""
        widgets = [
            cast(MainWidget, self._content.widget(idx))
            for idx in range(self._content.count())
        ]
        for widget in widgets:
            log.debug("Requesting shutdown from widget")
            if not widget.request_shutdown():
                log.debug("Widget %s can't be shutdown", widget)
                close_event.ignore()
                return
        self._save_settings()
        super().closeEvent(close_event)

        for widget in widgets:
            widget.store_settings()
            widget.shutdown_completed.connect(self.on_widget_shutdown)
            widget.shutdown()

    def on_widget_shutdown(self, widget: MainWidget) -> None:
        """
        Handle a completed widget shutdown.

        If all widgets have shutdown the application is closed.
        """
        log.debug("Widget completed shutdown: %s", widget)
        self._content.removeWidget(widget)
        if not self._content.count():
            log.debug("All widgets have shut down.")
            self.shutdown_complete.emit()
        else:
            log.debug(
                "Those widgets are still shutting down: %s",
                [
                    self._content.widget(idx)
                    for idx in range(self._content.count())
                ],
            )

    @Slot(str, name="on_change_theme")
    def on_change_theme(self, theme: str) -> None:
        """Change the theme to the theme with the given name."""
        set_current_style(theme)
        QApplication.setPalette(QApplication.style().standardPalette())
        self.setStyleSheet(get_style())
        self.update()
