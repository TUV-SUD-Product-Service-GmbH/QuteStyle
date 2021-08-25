"""Test script to validate TSL style."""
import logging
import sys

from PyQt5.QtCore import QCoreApplication, QSize, Qt, pyqtSignal
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QSpacerItem,
    QTableWidget,
    QVBoxLayout,
    QWidget,
)

from tsl.init import SETTINGS, init
from tsl.style import THEMES, get_current_style, get_style, set_current_style
from tsl.tsl_main_gui import TSLStyledMainWindow
from tsl.widgets.base_widgets import ColumnBaseWidget, MainWidget
from tsl.widgets.icon_button import IconButton
from tsl.widgets.toggle import Toggle

log = logging.getLogger(f"tsl.{__name__}")  # pylint: disable=invalid-name


class RightWidget(ColumnBaseWidget):
    """Test ColumnBaseWidget."""

    ICON = ":/svg_icons/icon_PSE.svg"
    NAME = "PSE Informationen"

    def __init__(self, parent: QWidget = None) -> None:
        """Create a new RightWidget."""
        super().__init__(parent)

        layout = QHBoxLayout()

        pse_info_button = IconButton(
            self, icon_path=":/svg_icons/icon_clipboard.svg"
        )
        layout.addWidget(pse_info_button)
        rcolumn_spacer1 = QSpacerItem(
            20, 40, QSizePolicy.Fixed, QSizePolicy.Fixed
        )
        layout.addItem(rcolumn_spacer1)
        toggle_test = Toggle()
        layout.addWidget(toggle_test)

        self.setLayout(layout)


class SettingsWidget(ColumnBaseWidget):
    """Test ColumnBaseWidget."""

    ICON = ":/svg_icons/icon_settings.svg"
    NAME = "Einstellungen"

    def __init__(self, parent: QWidget = None) -> None:
        """Create a new SettingsWidget."""
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Dies ist ein Text-Text \n" * 10))
        layout.addWidget(QTableWidget())


class InfoWidget(ColumnBaseWidget):
    """Test ColumnBaseWidget."""

    ICON = ":/svg_icons/icon_info.svg"
    NAME = "Info"

    switch_style = pyqtSignal(name="switch_style")

    def __init__(self, parent: QWidget = None) -> None:
        """Create a new SettingsWidget."""
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.addWidget(QLabel("Switch style"))
        button = IconButton(self, ":/svg_icons/icon_send.svg")
        layout.addWidget(button)
        button.clicked.connect(self.switch_style)


class TestWidget(MainWidget):
    """Test Widget."""

    ICON = ":/svg_icons/icon_heart.svg"
    NAME = "Test-Widget"

    def __init__(self, parent: QWidget = None) -> None:
        """Create a bew TestWidget."""
        super().__init__(parent)
        self.setStyleSheet("QFrame {\n" "	font-size: 16pt;\n" "}")
        layout = QVBoxLayout(self)
        empty_page_label = QLabel(self)
        empty_page_label.setAlignment(Qt.AlignCenter)
        empty_page_label.setText("hjuhuujuuu")
        layout.addWidget(empty_page_label)


class InfoPage(MainWidget):
    """Test Widget."""

    ICON = ":/svg_icons/icon_heart.svg"
    NAME = "Information"

    def __init__(self, parent: QWidget = None) -> None:
        """Create a new InfoPage."""
        super().__init__(parent)
        self.setStyleSheet("font-size: 14pt")
        self.setObjectName("home")
        self.page_1_layout = QVBoxLayout(self)
        self.page_1_layout.setContentsMargins(5, 5, 5, 5)
        self.page_1_layout.setSpacing(5)
        self.page_1_layout.setObjectName("page_1_layout")
        self.welcome_base = QFrame(self)
        self.welcome_base.setFrameShape(QFrame.NoFrame)
        self.welcome_base.setFrameShadow(QFrame.Raised)
        self.welcome_base.setObjectName("welcome_base")
        self.center_page_layout = QVBoxLayout(self.welcome_base)
        self.center_page_layout.setContentsMargins(0, 0, 0, 0)
        self.center_page_layout.setSpacing(10)
        self.center_page_layout.setObjectName("center_page_layout")
        self.logo = QFrame(self.welcome_base)
        self.logo.setFrameShape(QFrame.NoFrame)
        self.logo.setFrameShadow(QFrame.Raised)
        self.logo.setObjectName("logo")
        self.logo_layout = QVBoxLayout(self.logo)
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.logo_layout.setSpacing(0)
        self.logo_layout.setObjectName("logo_layout")
        self.center_page_layout.addWidget(self.logo)
        self.label = QLabel(self.welcome_base)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setObjectName("label")
        self.center_page_layout.addWidget(self.label)
        self.page_1_layout.addWidget(self.welcome_base, 0, Qt.AlignHCenter)

        self.label.setText("Willkommen zur Toolbox")
        self.logo_svg = QSvgWidget(":/svg_images/logo_toolbox.svg")
        self.logo_svg.setMinimumSize(250, 250)
        self.logo_layout.addWidget(
            self.logo_svg, Qt.AlignCenter, Qt.AlignCenter
        )


class StyledMainWindow(TSLStyledMainWindow):
    """Test StyledMainWindow for validation of TSL Darcula Style."""

    MAIN_WIDGET_CLASSES = [InfoPage, TestWidget]
    RIGHT_WIDGET_CLASS = RightWidget
    LEFT_WIDGET_CLASSES = [SettingsWidget, InfoWidget]

    MIN_SIZE = QSize(800, 600)

    def __init__(  # pylint: disable=too-many-arguments
        self,
        update: bool,
        help_text: str,
        name: str,
        version: str,
        force_whats_new: bool = False,
        parent: QWidget = None,
    ) -> None:
        """Create a new StyledMainWindow."""
        super().__init__(
            update, help_text, name, version, force_whats_new, parent
        )
        self._left_column.widget(InfoWidget).switch_style.connect(
            self.on_switch_style
        )
        try:
            self._current_idx = (
                "Snow White",
                "Darcula",
                "Princess Pink",
            ).index(get_current_style())
        except KeyError:
            self._current_idx = 0

    def on_switch_style(self) -> None:
        """Set the next available style."""
        self._current_idx += 1
        if self._current_idx == 3:
            self._current_idx = 0
        style_name = tuple(THEMES.keys())[self._current_idx]
        set_current_style(style_name)
        self.setStyleSheet(get_style())
        self.update()


if __name__ == "__main__":
    SETTINGS["log_level"] = logging.DEBUG
    APP_NAME = "TSL Test-App"
    init(APP_NAME, logs=True, hook=True, registry=True)
    # activate highdpi icons and scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    APP = QApplication(sys.argv)
    QCoreApplication.setApplicationName(APP_NAME)
    QCoreApplication.setOrganizationName("TÜV SÜD Product Service GmbH")
    QCoreApplication.setOrganizationDomain("tuvsud.com")
    WINDOW = StyledMainWindow(False, "", APP_NAME, "2.3.4", False)
    WINDOW.show()
    sys.exit(APP.exec())
