"""HomePage for TSL Apps."""
from typing import Callable, cast

from PyQt5.QtCore import QSettings, QSize, Qt, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QGridLayout,
    QLabel,
    QLayout,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from tsl.style import THEMES, _create_theme_drawing
from tsl.widgets.base_widgets import MainWidget


class HomePage(MainWidget):
    """HomePage for TSL Apps."""

    ICON = ":/svg_icons/home.svg"
    NAME = "Information"
    APP_NAME = "App"

    change_theme = pyqtSignal(str, name="change_theme")

    def __init__(self, parent: QWidget = None) -> None:
        """Create a new HomePage."""
        super().__init__(parent)

        if self._check_show_theme_selection_widget():
            # Show style selection
            self._add_style_selection()
        else:
            self.setLayout(self._create_layout())

    def _create_layout(self) -> QLayout:
        """Add custom layout."""
        raise NotImplementedError("Subclasses must implement this method.")

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

    def _add_style_selection(self) -> None:
        """Add style selection."""
        vert_box_layout = QVBoxLayout(self)
        vert_box_layout.setSpacing(20)
        self.setLayout(vert_box_layout)

        label = QLabel(f"Willkommen zur {self.APP_NAME}")
        label.setObjectName("heading_label")
        label.setContentsMargins(0, 0, 0, 20)
        vert_box_layout.addWidget(label)
        vert_box_layout.setAlignment(label, Qt.AlignCenter)

        label = QLabel(
            self.tr(
                "Bitte wählen Sie ein ToolBox-Design aus, "
                "das Sie verwenden wollen."
            ),
            self,
        )
        label.setObjectName("heading_label")
        vert_box_layout.addWidget(label)
        vert_box_layout.setAlignment(label, Qt.AlignCenter)
        label = QLabel(
            self.tr(
                "(Der Design-Stil kann jederzeit über die "
                "Einstellungen geändert werden.)"
            ),
            self,
        )
        vert_box_layout.addWidget(label)
        vert_box_layout.setAlignment(label, Qt.AlignCenter)

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
            QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum),
            0,
            0,
            -1,
            0,
        )
        grid.addItem(
            QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum),
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
            button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
            if grid_column > 2:
                grid_row += 2
                grid_column = 1
            button.clicked.connect(update_lambda(theme))
            grid.addWidget(button, grid_row, grid_column)
            grid.addWidget(QLabel(theme, self), grid_row + 1, grid_column)
            grid_column += 1
        grid.addItem(
            QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding),
            grid_row + 2,
            0,
            -1,
            0,
        )
