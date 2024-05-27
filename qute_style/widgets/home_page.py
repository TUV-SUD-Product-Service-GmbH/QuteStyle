"""HomePage for qute_style Apps."""

from __future__ import annotations

import pickle
from collections.abc import Callable
from enum import IntEnum
from typing import cast

from PySide6.QtCore import (
    QEasingCurve,
    QFile,
    QIODevice,
    QPropertyAnimation,
    QSettings,
    QSize,
    Qt,
    Signal,
    Slot,
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QLayout,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from qute_style.dev.dev_functions import VersionInfo
from qute_style.style import THEMES, _create_theme_drawing, log
from qute_style.widgets.base_widgets import MainWidget
from qute_style.widgets.icon import Icon


class WidgetType(IntEnum):
    """Definition of WidgetType."""

    HOMEPAGE = 0
    VERSION_HISTORY = 1
    STYLE_WIDGET = 2


class StackedWidget(QStackedWidget):
    """Stacked widget for homepage."""

    widget_selected = Signal(int, name="widget_selected")

    def __init__(self, parent: QWidget | None = None) -> None:
        """Create a new StackedWidget."""
        super().__init__(parent)
        self._animation_running = False
        self._animation = QPropertyAnimation(self, b"size")
        self._animation.setDuration(400)
        self._animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self._animation.finished.connect(self.on_animation_finished)

    def set_current_index(self, index: int, animate: bool = True) -> None:
        """Set page index."""
        if self._animation_running or index == self.currentIndex():
            # if index is changed during animation skip and revert to old index
            # if selection is current selection do not start animation
            self.widget_selected.emit(self.currentIndex())
            return
        super().setCurrentIndex(index)
        self.widget_selected.emit(index)
        if animate:
            self._animation.setStartValue(
                QSize(self.currentWidget().width(), 0)
            )
            self._animation.setEndValue(
                QSize(
                    self.currentWidget().width(), self.currentWidget().height()
                )
            )
            self._animation.start()
            self._animation_running = True

    @Slot(name="on_animation_finished")
    def on_animation_finished(self) -> None:
        """Animation finished."""
        self._animation_running = False


class HomePage(MainWidget):
    """HomePage for qute_style Apps."""

    ICON = ":/svg_icons/home.svg"
    NAME = "Information"

    change_theme = Signal(str, name="change_theme")

    def __init__(
        self,
        app_info: tuple[str, str, str],
        visible_widgets: list[type[MainWidget]],
        parent: QWidget | None = None,
    ) -> None:
        """Init Homepage."""
        super().__init__(parent)
        self._visible_widgets: list[type[MainWidget]] = visible_widgets
        self._app_name, self._app_logo, self._app_lang = app_info
        self._widget_stack = StackedWidget()
        self._select_buttons: dict[int, QPushButton] = {}
        self.setLayout(self._create_layout(self._create_welcome_widget()))
        if self._check_show_theme_selection_widget():
            self._widget_stack.set_current_index(
                WidgetType.STYLE_WIDGET, False
            )
        else:
            self._widget_stack.set_current_index(WidgetType.HOMEPAGE, False)

    def _create_welcome_widget(self) -> QWidget:
        """Add custom widget to as homepage."""
        widget = QWidget()
        layout = QGridLayout(widget)
        layout.setVerticalSpacing(100)
        widget.setLayout(layout)
        layout.addItem(
            QSpacerItem(
                0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

        label = QLabel(f"Willkommen zur {self._app_name}")
        label.setObjectName("heading_label")
        layout.addWidget(label, 1, 0)
        layout.setAlignment(label, Qt.AlignmentFlag.AlignCenter)

        logo_svg = QSvgWidget(self._app_logo)
        logo_svg.setFixedSize(QSize(200, 200))
        layout.addWidget(logo_svg, 2, 0)
        layout.setAlignment(logo_svg, Qt.AlignmentFlag.AlignCenter)

        layout.addItem(
            QSpacerItem(
                3, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            )
        )

        return widget

    @staticmethod
    def _check_show_theme_selection_widget() -> bool:
        """
        Check if theme selection widget should be displayed.

        Theme selection should be displayed only once at first start of app.
        """
        show_selection = cast(
            bool,
            QSettings().value("CustomThemeSelectionActive", True, type=bool),
        )
        QSettings().setValue("CustomThemeSelectionActive", False)
        return show_selection

    def _create_layout(self, welcome_widget: QWidget) -> QLayout:
        """Create layout."""
        self._widget_stack.addWidget(welcome_widget)
        self._widget_stack.addWidget(self._create_version_history_widget())
        self._widget_stack.addWidget(self._create_style_selection_widget())
        self._widget_stack.widget_selected.connect(self.on_index_changed)

        homepage_btn = QPushButton(self.tr("Homepage"))
        homepage_btn.setCheckable(True)
        homepage_btn.setAutoExclusive(True)
        self._select_buttons[WidgetType.HOMEPAGE] = homepage_btn
        version_history_btn = QPushButton(self.tr("Versionshistorie"))
        version_history_btn.setCheckable(True)
        version_history_btn.setAutoExclusive(True)
        self._select_buttons[WidgetType.VERSION_HISTORY] = version_history_btn
        stylesheet_btn = QPushButton(self.tr("Auswahl Style"))
        stylesheet_btn.setCheckable(True)
        stylesheet_btn.setAutoExclusive(True)
        self._select_buttons[WidgetType.STYLE_WIDGET] = stylesheet_btn

        homepage_btn.clicked.connect(
            lambda: self._widget_stack.set_current_index(WidgetType.HOMEPAGE)
        )
        version_history_btn.clicked.connect(
            lambda: self._widget_stack.set_current_index(
                WidgetType.VERSION_HISTORY
            )
        )
        stylesheet_btn.clicked.connect(
            lambda: self._widget_stack.set_current_index(
                WidgetType.STYLE_WIDGET
            )
        )
        layout = QGridLayout(self)
        layout.addWidget(self._widget_stack, 0, 0, 1, 3)
        layout.addWidget(homepage_btn, 1, 0)
        layout.addWidget(version_history_btn, 1, 1)
        layout.addWidget(stylesheet_btn, 1, 2)
        return layout

    @Slot(int, name="on_index_changed")
    def on_index_changed(self, index: int) -> None:
        """
        On index changed.

        Set the correct button if a stacked widget is selected.
        """
        self._select_buttons[index].setChecked(True)

    def _create_version_history_widget(self) -> QWidget:
        """Create the version history."""
        resource_path = ":/change_log_data.pickle"
        resource_file = QFile(resource_path)
        change_log_data: dict[VersionInfo, dict[str, list[dict[str, str]]]] = (
            {}
        )
        if resource_file.open(QIODevice.OpenModeFlag.ReadOnly):
            pickle_data = resource_file.readAll()
            change_log_data = pickle.loads(pickle_data.data())
            resource_file.close()
        else:
            log.debug("No changelog data found! %s", resource_path)

        widget = QWidget()
        vert_box_layout = QVBoxLayout(widget)
        widget.setLayout(vert_box_layout)
        label = QLabel(self.tr("Versionshistorie"))
        label.setObjectName("heading_label")
        label.setContentsMargins(0, 0, 0, 10)
        vert_box_layout.addWidget(label)
        vert_box_layout.setAlignment(label, Qt.AlignmentFlag.AlignCenter)

        scroll_area = QScrollArea()
        scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        vert_box_layout.addWidget(scroll_area)
        scroll_area.setWidgetResizable(True)
        central_widget = QWidget()
        central_widget.setObjectName("style_selection_widget")

        grid = QGridLayout()
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(20)
        central_widget.setLayout(grid)
        scroll_area.setWidget(central_widget)
        self.fill_version_info(grid, change_log_data, self._visible_widgets)
        return widget

    def fill_version_info(
        self,
        grid_layout: QGridLayout,
        change_log_data: dict[VersionInfo, dict[str, list[dict[str, str]]]],
        visible_widgets: list[type[MainWidget]],
    ) -> None:
        """Set up version grid from change_log_data."""
        log.debug("Fill version grid")
        # get the sorted version keys in descending order. Newest version first
        if not change_log_data:
            log.debug("No changelog data found")
            label = QLabel(self.tr("Keine Einträge vorhanden"))
            label.setObjectName("heading1_label")
            label.setMinimumHeight(30)
            grid_layout.addWidget(label, 0, 1)
            grid_layout.setAlignment(label, Qt.AlignmentFlag.AlignCenter)
            return

        grid_layout.addItem(
            QSpacerItem(
                0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            ),
            0,
            3,
        )
        grid_layout.addItem(
            QSpacerItem(
                0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            ),
            0,
            0,
        )

        row = 0
        for version_info, log_data_dict in change_log_data.items():
            version_info_text = (
                f"V {version_info.version} - {version_info.release_date}"
                if version_info.release_date
                else f"V {version_info.version}"
            )
            label = QLabel(version_info_text)
            label.setObjectName("heading1_label")
            label.setMinimumHeight(30)
            grid_layout.addWidget(label, row, 1, 1, 2)
            row += 1

            # handle version specific logs
            entries_available: bool = False
            if self._app_name in log_data_dict:
                # handle general app logs
                w_icon = self._app_logo
                w_name = self._app_name
                entries_available = True
                row = self._add_item_to_grid(
                    grid_layout,
                    row,
                    (w_name, w_icon),
                    [
                        entry[self._app_lang]
                        for entry in log_data_dict[self._app_name]
                    ],
                )

            # handle widget specific logs
            for widget in visible_widgets:
                if widget.__name__ not in log_data_dict:
                    # widget not present anymore. Ignore
                    continue
                w_icon = widget.ICON
                w_name = widget.NAME
                entries_available = True
                row = self._add_item_to_grid(
                    grid_layout,
                    row,
                    (w_name, w_icon),
                    [
                        entry[self._app_lang]
                        for entry in log_data_dict[widget.__name__]
                    ],
                )

            if not entries_available:
                label = QLabel(
                    self.tr(
                        "Keine relevanten Änderungen für Ihre "
                        "Benutzergruppe vorhanden."
                    )
                )
                label.setMinimumHeight(30)
                grid_layout.addWidget(label, row, 2)
                row += 1

        grid_layout.addItem(
            QSpacerItem(
                0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            ),
            row,
            0,
            -1,
            0,
        )

    def _add_item_to_grid(
        self,
        grid_layout: QGridLayout,
        row: int,
        widget_info: tuple[str, str],
        text_items: list[str],
    ) -> int:
        """Add changelog item to grid."""
        widget_name, widget_icon = widget_info
        if widget_name == self._app_name:
            # load as svg icon
            svg_widget = QSvgWidget(widget_icon)
            svg_widget.setFixedSize(QSize(18, 18))
            grid_layout.addWidget(svg_widget, row, 1)
        else:
            icon = Icon(radius=18)
            icon.set_icon(widget_icon)
            grid_layout.addWidget(icon, row, 1)

        label = QLabel(widget_name)
        label.setObjectName("heading2_label")
        label.setMinimumHeight(30)
        grid_layout.addWidget(label, row, 2)
        row += 1
        for text in text_items:
            label = QLabel(text)
            label.setWordWrap(True)
            label.setMinimumHeight(30)
            label.setMinimumWidth(700)
            label.setMaximumWidth(1000)
            grid_layout.addWidget(label, row, 2)
            row += 1
        return row

    def _create_style_selection_widget(  # pylint: disable=too-many-locals
        self,
    ) -> QWidget:
        """Add style selection."""
        widget = QWidget()
        vert_box_layout = QVBoxLayout()
        vert_box_layout.setSpacing(20)
        widget.setLayout(vert_box_layout)

        label = QLabel(f"Willkommen zur {self._app_name}")
        label.setObjectName("heading_label")
        label.setContentsMargins(0, 0, 0, 20)
        vert_box_layout.addWidget(label)
        vert_box_layout.setAlignment(label, Qt.AlignmentFlag.AlignCenter)

        label = QLabel(
            self.tr(
                "Bitte wählen Sie ein ToolBox-Design aus, "
                "das Sie verwenden wollen."
            ),
            self,
        )
        label.setObjectName("heading_label")
        vert_box_layout.addWidget(label)
        vert_box_layout.setAlignment(label, Qt.AlignmentFlag.AlignCenter)
        label = QLabel(
            self.tr(
                "(Der Design-Stil kann jederzeit über die "
                "Einstellungen geändert werden.)"
            ),
            self,
        )
        vert_box_layout.addWidget(label)
        vert_box_layout.setAlignment(label, Qt.AlignmentFlag.AlignCenter)

        scroll_area = QScrollArea(self)
        vert_box_layout.addWidget(scroll_area)
        scroll_area.setWidgetResizable(True)
        central_widget = QWidget()
        central_widget.setObjectName("style_selection_widget")

        grid = QGridLayout()
        grid.setHorizontalSpacing(40)
        grid.setVerticalSpacing(20)
        central_widget.setLayout(grid)
        scroll_area.setWidget(central_widget)

        def select_theme(theme_name: str) -> None:
            """Select the theme."""
            self.change_theme.emit(theme_name)

        def update_lambda(theme_name: str) -> Callable[[], None]:
            """Update lambda."""
            return lambda: select_theme(theme_name)

        icon_size = QSize(300, 200)
        grid.addItem(
            QSpacerItem(
                0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            ),
            0,
            0,
            -1,
            0,
        )
        grid.addItem(
            QSpacerItem(
                0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            ),
            0,
            3,
            -1,
            0,
        )
        grid_column = 1
        grid_row = 0
        for theme, color_names in THEMES.items():
            # check if the theme has a preview image otherwise don't use as
            # an option to select
            button = QPushButton(self)
            pixmap = QPixmap(_create_theme_drawing(icon_size, color_names))
            button.setIcon(QIcon(pixmap))
            button.setIconSize(icon_size)
            button.setSizePolicy(
                QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum
            )
            if grid_column > 2:
                grid_row += 2
                grid_column = 1
            button.clicked.connect(update_lambda(theme))
            grid.addWidget(button, grid_row, grid_column)
            grid.addWidget(QLabel(theme, self), grid_row + 1, grid_column)
            grid_column += 1
        grid.addItem(
            QSpacerItem(
                0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
            ),
            grid_row + 2,
            0,
            -1,
            0,
        )

        return widget
