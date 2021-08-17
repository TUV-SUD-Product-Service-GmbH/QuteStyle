"""TSLStyledMainWindow definition for custom Darcula style."""
import logging
from typing import List, Tuple, Type, cast

from PyQt5.QtCore import (
    QEasingCurve,
    QParallelAnimationGroup,
    QPoint,
    QPropertyAnimation,
    QSize,
    Qt,
    pyqtSlot,
)
from PyQt5.QtGui import QMouseEvent, QResizeEvent
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLayout,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from tsl.style import get_style
from tsl.update_window import TSLMainWindow
from tsl.widgets.background_frame import BackgroundFrame
from tsl.widgets.base_widgets import ColumnBaseWidget, MainWidget
from tsl.widgets.credit_bar import CreditBar
from tsl.widgets.grips import CornerGrip, EdgeGrip
from tsl.widgets.left_column import LeftColumn
from tsl.widgets.left_menu import LeftMenu
from tsl.widgets.title_bar import TitleBar

log = logging.getLogger(f"tsl.{__name__}")  # pylint: disable=invalid-name


class TSLStyledMainWindow(  # pylint: disable=too-many-instance-attributes
    TSLMainWindow
):
    """TSLStyledMainWindow definition for custom Darcula style."""

    # Widgets that will be shown in the center content and which are
    # accessible from the main menu on the left side.
    MAIN_WIDGET_CLASSES: List[Type[MainWidget]]

    # Widget that is shown in the right column.
    RIGHT_WIDGET_CLASS: Type[ColumnBaseWidget]

    # Widgets that are shown in the left column.
    LEFT_WIDGET_CLASSES: List[Type[ColumnBaseWidget]]

    MIN_SIZE: QSize = QSize(0, 0)

    def __init__(  # pylint: disable=too-many-arguments
        self,
        update: bool,
        help_text: str,
        name: str,
        version: str,
        force_whats_new: bool = False,
        parent: QWidget = None,
    ) -> None:
        """Create a new TSLStyledMainWindow."""
        super().__init__(
            update, help_text, name, version, force_whats_new, parent
        )

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

        # Add the left menu.
        self._left_menu = self._add_left_menu(self._background.layout())

        # Add the left column.
        self._left_column_frame, self._left_column = self.add_left_column(
            self._background.layout()
        )

        # Add the main frame that contains title and credit bar as well as
        # the main content and the right column.
        right_app_frame = QFrame()
        right_app_layout = QVBoxLayout(right_app_frame)
        right_app_layout.setContentsMargins(3, 7, 7, 3)
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
        right_app_layout.addWidget(CreditBar(self._version))

        self._grips = [
            EdgeGrip(self, Qt.LeftEdge),
            EdgeGrip(self, Qt.RightEdge),
            EdgeGrip(self, Qt.TopEdge),
            EdgeGrip(self, Qt.BottomEdge),
            CornerGrip(self, Qt.TopLeftCorner),
            CornerGrip(self, Qt.TopRightCorner),
            CornerGrip(self, Qt.BottomLeftCorner),
            CornerGrip(self, Qt.BottomRightCorner),
        ]

        # Activate the first widget to be visible by default.
        self.on_main_widget(self.MAIN_WIDGET_CLASSES[0])

    def _add_main_area(
        self, layout: QLayout
    ) -> Tuple[QFrame, ColumnBaseWidget, QStackedWidget]:
        """
        Add a Frame that contains the main content and the right column widget.

        The method creates a QFrame that contains two widgets:
        1. A QStackedWidget that contains all the widgets that are accessible
        from the menu (as defined in TslMainGui.MAIN_WIDGET_CLASS
        2. A QFrame with the widget that is used as the right column.
        """
        content_area_frame = QFrame()
        content_area_layout = QHBoxLayout(content_area_frame)
        content_area_layout.setContentsMargins(0, 0, 0, 0)

        # Create the QStackedWidget that contains all the content widgets
        content = QStackedWidget()
        for widget_class in self.MAIN_WIDGET_CLASSES:
            content.addWidget(widget_class())
        content_area_layout.addWidget(content)

        # Add the QFrame to the given layout.
        layout.addWidget(content_area_frame)

        # Create and add the right column QFrame to the given layout.
        right_column_frame, right_content = self.add_right_column(
            content_area_layout
        )
        return right_column_frame, right_content, content

    def add_right_column(
        self, layout: QLayout
    ) -> Tuple[QFrame, ColumnBaseWidget]:
        """
        Create a frame containing the right column widget and return it.

        This method creates a QFrame that is opened/closed with a button in the
        TitleBar. Therefore it's initial width is 0. The frame contains a
        layout with a margin of 5 pixels which contains the widget for the
        right column (as defined in TslMainGui.RIGHT_WIDGET_CLASS).
        """
        right_column_frame = QFrame()
        right_column_frame.setObjectName("bg_frame")
        right_column_frame.setFixedWidth(0)
        content_area_right_layout = QVBoxLayout(right_column_frame)
        content_area_right_layout.setContentsMargins(5, 5, 5, 5)
        right_content = self.RIGHT_WIDGET_CLASS()
        content_area_right_layout.addWidget(right_content)
        layout.addWidget(right_column_frame)
        return right_column_frame, right_content

    def _configure_main_window(self) -> None:
        """Configure the TSLStyledMainWindow."""
        # Set the name of the app.
        self.setWindowTitle(self._app_name)

        # Make the window borderless and transparent.
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Set the minimum overall size that is configured.
        self.setMinimumSize(self.MIN_SIZE)

    def _add_title_bar(self, right_app_layout: QLayout) -> TitleBar:
        """Add a TitleBar to the given QLayout."""
        title_bar = TitleBar(
            self,
            self.centralWidget(),
            self.RIGHT_WIDGET_CLASS,
            self._app_name,
        )
        title_bar.close_app.connect(self.close)
        title_bar.minimize.connect(self.showMinimized)
        title_bar.maximize.connect(self.maximize)
        title_bar.move_window.connect(self.move_window)
        right_app_layout.addWidget(title_bar)
        title_bar.right_button_clicked.connect(self.on_right_column)
        return title_bar

    def add_left_column(self, layout: QLayout) -> Tuple[QFrame, LeftColumn]:
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
            widget_types=self.LEFT_WIDGET_CLASSES,
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

        The methods returns the LeftMenu.
        """
        # add custom left menu bar
        left_menu_frame = QFrame()
        left_menu_frame.setFixedWidth(56)  # 50 px and 3px margin on each side
        left_menu_layout = QHBoxLayout(left_menu_frame)
        left_menu_layout.setContentsMargins(3, 3, 3, 3)
        # add custom left menu
        left_menu = LeftMenu(
            parent=left_menu_frame,
            app_parent=self.centralWidget(),
            main_widgets=self.MAIN_WIDGET_CLASSES,
            left_column_widgets=self.LEFT_WIDGET_CLASSES,
        )
        left_menu_layout.addWidget(left_menu)
        layout.addWidget(left_menu_frame)
        left_menu.bottom_button_clicked.connect(self.on_left_column)
        left_menu.top_button_clicked.connect(self.on_main_widget)
        return left_menu

    def set_style(self) -> None:
        """Set the main stylesheet of the app."""
        self.setStyleSheet(get_style())

    @pyqtSlot(QPoint, name="move_window")
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

    def showNormal(self) -> None:  # pylint: disable=invalid-name
        """
        Override showNormal for custom handling of style.

        This will add a margin for the contents of the main QLayout so that
        a shadow and the border with round edges is visible. This also adds
        the round borders on the main QFrame.

        It will set the correct icon on the maximize button.
        """
        self.centralWidget().layout().setContentsMargins(10, 10, 10, 10)
        self._background.set_stylesheet(border_radius=10, border_size=2)
        self._title_bar.set_maximized(False)
        super().showNormal()

    def showMaximized(self) -> None:  # pylint: disable=invalid-name
        """
        Override showNormal for custom handling of style.

        This removes the content margin so that the app fits exactly into the
        screen. Also, this removed the round borders from the main QFrame.

        It will set the correct icon on the maximize button.
        """
        self.centralWidget().layout().setContentsMargins(0, 0, 0, 0)
        self._background.set_stylesheet(border_radius=0, border_size=0)
        self._title_bar.set_maximized(True)
        super().showMaximized()

    def maximize(self) -> None:
        """Handle a maximize request from the TitleBar."""
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def left_column_is_visible(self) -> bool:
        """Determine if left column is visible."""
        return not self._left_column_frame.width() == 0

    def right_column_is_visible(self) -> bool:
        """Determine if right column is visible."""
        return self._right_column_frame.width() != 0

    @staticmethod
    def _create_slide_animation(
        frame: QFrame, slide_out: bool
    ) -> QPropertyAnimation:
        """Create an animation that will open or close a QFrame."""
        animation = QPropertyAnimation(frame, b"minimumWidth")
        animation.setDuration(500)
        if slide_out:
            animation.setStartValue(0)
            animation.setEndValue(240)
        else:
            animation.setStartValue(240)
            animation.setEndValue(0)
        animation.setEasingCurve(QEasingCurve.InOutQuart)
        return animation

    def _start_box_animation(self, left_open: bool, right_open: bool) -> None:
        """
        Animate slide in/out of left or right column.

        This method will clear an ongoing animation (group), and create a new
        one based on the request parameters and state of the columns.
        """
        self._group.clear()

        # Animate if left_open is not the current value (XOR):
        # Open if closed and close if opened.
        if left_open is not self.left_column_is_visible():
            self._group.addAnimation(
                self._create_slide_animation(
                    self._left_column_frame, left_open
                )
            )

        # Same logic as above.
        if right_open is not self.right_column_is_visible():
            self._group.addAnimation(
                self._create_slide_animation(
                    self._right_column_frame, right_open
                )
            )

        self._group.start()

    def resizeEvent(  # pylint: disable=invalid-name
        self, event: QResizeEvent
    ) -> None:
        """List to QResizeEvents to adapt position of grips."""
        super().resizeEvent(event)
        for grip in self._grips:
            grip.adapt()

    def mousePressEvent(  # pylint: disable=invalid-name
        self, event: QMouseEvent
    ) -> None:
        """Event triggered on mouse button press."""
        log.debug("Storing last click at %s", event.globalPos())
        self.last_move_pos = event.globalPos()

    @pyqtSlot(type, name="on_main_widget")
    def on_main_widget(self, widget_class: Type[MainWidget]) -> None:
        """Handle display of the main widget that is of the given type."""
        current_widget = cast(
            Type[MainWidget],
            type(self._content.currentWidget()),
        )
        self._left_menu.set_button_active(current_widget, False)
        self._left_menu.set_button_active(widget_class, True)
        for idx in range(self._content.count()):
            widget = self._content.widget(idx)
            if isinstance(widget, widget_class):
                self._content.setCurrentWidget(widget)
                return
        raise ValueError(f"Could not find widget {widget_class}")

    @pyqtSlot(name="on_right_column")
    def on_right_column(self) -> None:
        """Handle a click on the button for the right column."""
        show = not self.right_column_is_visible()
        self._title_bar.set_right_button_active(show)
        self._start_box_animation(False, show)

    @pyqtSlot(type, name="on_left_column")
    def on_left_column(self, widget_class: Type[ColumnBaseWidget]) -> None:
        """Handle a click on the button for the left column."""
        self._left_menu.set_button_active(
            self._left_column.current_widget(), False
        )
        log.debug("Handling left column for %s", widget_class)
        show = (
            not self.left_column_is_visible()
            or widget_class != self._left_column.current_widget()
        )
        log.debug("Showing column: %s", show)
        self._left_column.set_column_widget(widget_class)
        self._start_box_animation(show, False)
        self._left_menu.set_button_active(widget_class, show)

    @pyqtSlot(name="on_close_left_column")
    def on_close_left_column(self) -> None:
        """Handle a click on the button for the left column."""
        widget_class = self._left_column.current_widget()
        self._left_menu.set_button_active(widget_class, False)
        self._start_box_animation(False, False)
