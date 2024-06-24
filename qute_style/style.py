"""Style handling for QuteStyleWindow."""

import logging
from typing import cast

from PySide6.QtCore import QRect, QSettings, QSize
from PySide6.QtGui import QColor, QPainter, QPixmap

log = logging.getLogger(
    f"qute_style.{__name__}"
)  # pylint: disable=invalid-name


# Use this variable when referencing a default style so that adapting to a new
# default style will only require changes in the lib.
DEFAULT_STYLE = "Darcula"

CURRENT_STYLE: str | None = None


def _create_theme_drawing(
    icon_size: QSize, color_names: dict[str, str]
) -> QPixmap:
    """Create theme drawing."""
    pixmap = QPixmap(icon_size)
    painter = QPainter(pixmap)
    # draw background
    painter.fillRect(
        QRect(0, 0, pixmap.width(), pixmap.height()),
        QColor(color_names["bg_one"]),
    )
    # draw menu
    menu = QRect(0, 0, 20, pixmap.height())
    painter.fillRect(menu, QColor(color_names["dark_one"]))
    # draw menu icons
    for i in range(8):
        y_pos = i * 20 + 5
        if y_pos + 8 < menu.height():
            painter.fillRect(
                QRect(5, i * 20 + 5, 8, 8),
                QColor(color_names["active"]),
            )
    # draw toolbar
    toolbar = QRect(menu.width() + 5, 0, pixmap.width(), 15)
    painter.fillRect(toolbar, QColor(color_names["bg_two"]))

    # draw footer
    footer = QRect(menu.width() + 5, pixmap.height() - 10, pixmap.width(), 10)
    painter.fillRect(footer, QColor(color_names["bg_two"]))

    # draw widget
    widget = QRect(
        menu.width() + 5,
        toolbar.height() + 5,
        pixmap.width() - (menu.width() + 5),
        pixmap.height() - (toolbar.height() + footer.height() + 10),
    )
    painter.fillRect(widget, QColor(color_names["bg_two"]))

    # draw widget data
    for i in range(6):
        y_pos = i * 20 + 10
        if y_pos + 5 < widget.height():
            if i % 2:
                width = widget.width() - 40
                color = QColor(color_names["foreground"])
            else:
                width = widget.width() - 100
                color = QColor(color_names["context_color"])

            painter.fillRect(
                QRect(widget.x() + 10, y_pos + widget.y(), width, 5),
                color,
            )
    painter.end()
    return pixmap


def get_current_style() -> str:
    """Return the currently set style."""
    global CURRENT_STYLE  # noqa: PLW0603
    if CURRENT_STYLE is None:
        CURRENT_STYLE = cast(str, QSettings().value("style", DEFAULT_STYLE))
        log.debug("Loaded current style from registry: %s", CURRENT_STYLE)
        if CURRENT_STYLE not in THEMES:
            log.warning("Invalid style stored in registry: %s", CURRENT_STYLE)
            # If an invalid style is set, revert to DEFAULT_STYLE
            CURRENT_STYLE = DEFAULT_STYLE
    return CURRENT_STYLE


def set_current_style(style: str) -> None:
    """
    Set the current style.

    One should only use this method to change the style. This will correctly
    set CURRENT_STYLE to be used as a lazy variable.
    """
    log.debug("Setting current style to %s", style)
    global CURRENT_STYLE  # noqa: PLW0603
    CURRENT_STYLE = style
    QSettings().setValue("style", style)


THEMES: dict[str, dict[str, str]] = {
    "Snow White": {
        "dark_one": "#b5c3dd",
        "dark_two": "#bfcde6",
        "bg_one": "#c9d7ef",
        "bg_two": "#d3e0f7",
        "bg_elements": "#e2e9f7",
        "bg_three": "#eff1f7",
        "bg_disabled": "#e5eaf4",
        "fg_disabled": "#adaeaf",
        "foreground": "#24263f",
        "active": "#121320",
        "context_pressed": "#90a5c7",
        "context_color": "#9bb1d0",
        "context_hover": "#b2c3d6",
        "white": "#f5f6f9",
        "pink": "#ff007f",
        "green": "#15c72a",
        "light_green": "#46ff5c",
        "dark_green": "#0b6315",
        "red": "#ff5555",
        "light_red": "#ffd4d4",
        "dark_red": "#7f2a2a",
        "yellow": "#fda600",
        "light_yellow": "#ffd27c",
        "dark_yellow": "#7e5300",
        "grey": "#d3d3d3",
    },
    "Princess Pink": {
        "active": "#fffefe",
        "dark_one": "#282a36",
        "dark_two": "#363948",
        "bg_elements": "#595D75",
        "bg_one": "#44475a",
        "bg_two": "#4f5268",
        "bg_three": "#63677d",
        "bg_disabled": "#585c6e",
        "fg_disabled": "#83849b",
        "context_color": "#ff79c6",
        "context_hover": "#ffacdc",
        "context_pressed": "#e86eb4",
        "foreground": "#f6e2f6",
        "white": "#f5f6f9",
        "pink": "#ff79c6",
        "green": "#00ff7f",
        "light_green": "#7fffbf",
        "dark_green": "#007f3f",
        "red": "#ff5555",
        "light_red": "#ffd4d4",
        "dark_red": "#7f2a2a",
        "yellow": "#f1fa8c",
        "light_yellow": "#ffffff",
        "dark_yellow": "#787d46",
        "grey": "#d3d3d3",
    },
    "Darcula": {
        "active": "#dfe4ed",
        "dark_one": "#1b1e23",
        "dark_two": "#242830",
        "bg_elements": "#3c4454",
        "bg_one": "#2c313c",
        "bg_two": "#343b48",
        "bg_three": "#444C5B",
        "bg_disabled": "#3e4150",
        "fg_disabled": "#606478",
        "context_color": "#568af2",
        "context_hover": "#81A8F6",
        "context_pressed": "#4e7ddc",
        "foreground": "#b0b7c7",
        "white": "#f5f6f9",
        "pink": "#ff007f",
        "green": "#00ff7f",
        "light_green": "#7fffbf",
        "dark_green": "#007f3f",
        "red": "#ff5555",
        "light_red": "#ffd4d4",
        "dark_red": "#7f2a2a",
        "yellow": "#f1fa8c",
        "light_yellow": "#ffffff",
        "dark_yellow": "#787d46",
        "grey": "#d3d3d3",
    },
    "Highbridge Gray": {
        "active": "#0e0e0e",
        "bg_disabled": "#d9d9d9",
        "bg_one": "#ffffff",
        "bg_three": "#e3e3e3",
        "bg_two": "#f7f7f7",
        "context_color": "#aaa7bf",
        "context_hover": "#bdbcc8",
        "context_pressed": "#9e9cb7",
        "bg_elements": "#ededed",
        "dark_two": "#dedede",
        "dark_green": "#007f3f",
        "dark_one": "#c6c6c6",
        "dark_red": "#7f2a2a",
        "dark_yellow": "#787d46",
        "fg_disabled": "#919191",
        "green": "#00ff7f",
        "grey": "#d3d3d3",
        "light_green": "#7fffbf",
        "light_red": "#ffd4d4",
        "light_yellow": "#ffffff",
        "pink": "#ff007f",
        "red": "#ff5555",
        "foreground": "#393939",
        "white": "#f5f6f9",
        "yellow": "#fda600",
    },
    "Ruby Red": {
        "dark_one": "#431e1e",
        "dark_two": "#4f2424",
        "bg_one": "#5f2d2d",
        "bg_two": "#6a3030",
        "bg_elements": "#773535",
        "bg_three": "#823d3d",
        "bg_disabled": "#783a3a",
        "fg_disabled": "#a95454",
        "foreground": "#cb8d8d",
        "active": "#f4dfdf",
        "context_pressed": "#cc4848",
        "context_color": "#e44e4e",
        "context_hover": "#ea7171",
        "dark_green": "#007f3f",
        "dark_red": "#7f2a2a",
        "dark_yellow": "#787d46",
        "green": "#00ff7f",
        "grey": "#d3d3d3",
        "light_green": "#7fffbf",
        "light_red": "#ffd4d4",
        "light_yellow": "#ffffff",
        "pink": "#ff007f",
        "red": "#ff5555",
        "white": "#f5f6f9",
        "yellow": "#f1fa8c",
    },
}


def get_style() -> str:
    """Return the current style sheet that is stored in QSettings."""
    # Use the Darcula style if not style is stored yet as default.
    log.debug("Stored style: %s", get_current_style())
    return MAIN_STYLE.format(**THEMES[get_current_style()])


def get_color(name: str) -> str:
    """Return the color code for the given name."""
    return THEMES[get_current_style()][name]


MAIN_STYLE = """
/* QComboBox */
QComboBox{{
    color: {foreground};
    background-color: {bg_elements};
    border-radius: 5px;
    border: 1px solid {bg_elements};
    padding: 5px;
    padding-left: 10px;
}}
QComboBox:hover{{
    border: 1px solid {context_hover};
}}
QComboBox::drop-down {{
    width: 25px;
    border-left-width: 3px;
    border-left-color: {bg_two};
    border-left-style: solid;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
}}
QComboBox QAbstractItemView {{
    color: {foreground};
    background-color: {bg_elements};
    padding: 10px;
    selection-background-color: {context_color};
}}
QComboBox:disabled {{
    color: {fg_disabled};
    background-color: {bg_disabled};
    border: {bg_disabled};
}}
QComboBox[cssClass="transparent"] {{
    background-color: transparent;
}}
QComboBox::drop-down[cssClass="transparent"] {{
    border-left-color: transparent;
}}
QComboBox:disabled[cssClass="transparent"] {{
    color: {fg_disabled};
    background-color: transparent;
    border: {bg_disabled};
}}

/* QHeaderView */
QHeaderView{{
    background-color: {bg_two};
}}
QHeaderView::section{{
    color: {foreground};
    background-color: {bg_two};
    max-width: 30px;
    border: 0px;
    padding: 3px;
}}
QHeaderView::section:horizontal{{
    border-right: 1px solid {dark_two};
    border-right: 1px solid {dark_two};
    border-bottom: 1px solid {dark_two};
}}
QHeaderView::section:horizontal:only-one{{
    border-right: 0px;
}}
QHeaderView::section:horizontal:last{{
    border-right: 0px;
}}
QHeaderView::section:vertical{{
    border-bottom: 1px solid {dark_two};
    border-right: 1px solid {dark_two};
}}
QHeaderView::section:vertical:last{{
    border-bottom: 0px;
}}
QHeaderView::section:vertical:only-one{{
    border-bottom: 0px;
}}
QHeaderView::section:disabled{{
    color: {fg_disabled};
}}
QTableCornerButton::section {{
    background-color: {bg_two};
}}

/* QLineEdit */
QLineEdit,
QPlainTextEdit {{
    background-color: {bg_elements};
    border-radius: 8px;
    border: 1px solid transparent;
    padding-left: 10px;
    padding-right: 10px;
    selection-color: {active};
    selection-background-color: {context_color};
    color: {foreground};
    height: 30px;
}}
QLineEdit:read-only, QPlainTextEdit:read-only{{
    background-color: {bg_disabled};
    color: {fg_disabled};
}}
QLineEdit:read-only:focus,
QPlainTextEdit:read-only:focus {{
    border: 1px solid {bg_disabled};
    background-color: {bg_disabled};
}}

QLineEdit#column_line_edit {{
    background-color: {bg_elements};
    border-radius: 8px;
    border: 1px solid transparent;
    padding-left: 10px;
    padding-right: 10px;
    selection-color: {active};
    selection-background-color: {context_color};
    color: {foreground};
}}
QLineEdit:focus,
QPlainTextEdit:focus {{
    border: 1px solid {context_color};
    background-color: {bg_one};
}}
QLineEdit#column_line_edit:focus {{
    border: 1px solid {context_color};
    background-color: {bg_two};
}}

/* QMenu */
QMenu{{
    background-color: {bg_one};
    color: {foreground};
}}
QMenu::item:disabled {{
    color: {fg_disabled};
}}
QMenu::item:enabled:selected {{
    color: {active};
    background-color: {context_color};
}}
QMenu QCheckBox{{
    color: {foreground};
    border-radius: 17px;
    border: 10px solid transparent;
}}
QMenu QCheckBox:hover {{
    background-color: {context_hover};
    color: {active};
}}
QMenu QCheckBox:pressed {{
    background-color: {context_pressed};
    color: {active};
}}
QMenu::separator {{
    background: {bg_three};
    height: 3px;
    margin-left: 5px;
    margin-right: 5px;
}}
/* QScrollArea */
QScrollArea {{
    border: none;
}}
QWidget#scroll_widget {{
    background: {dark_one};
}}

QWidget#style_selection_widget
        {{ background-color:{bg_one}; }}

/* QProgressBar */
QProgressBar {{
    background-color: {bg_elements};
    color: {foreground};
    border-style: none;
    border-radius: 10px;
    text-align: center;
}}
QProgressBar::chunk {{
    background-color: {context_color};
    border-radius: 10px;
}}

/* QScrollBar */
QScrollBar:horizontal {{
    border: none;
    background: {bg_three};
    height: 8px;
    margin: 0px 21px 0 21px;
    border-radius: 0px;
}}
QScrollBar:horizontal:disabled {{
    background: {bg_disabled};
}}
QScrollBar::handle:horizontal {{
    background: {context_color};
    min-width: 25px;
    border-radius: 4px
}}
QScrollBar::handle:horizontal:disabled {{
    background: {fg_disabled};
}}
QScrollBar::handle:horizontal:hover {{
    background: {context_hover};
    min-width: 25px;
    border-radius: 4px
}}
QScrollBar::handle:horizontal:pressed {{
    background: {context_pressed};
    min-width: 25px;
    border-radius: 4px
}}
QScrollBar::add-line:horizontal {{
    border: none;
    background: {dark_two};
    width: 20px;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}}
QScrollBar::sub-line:horizontal {{
    border: none;
    background: {dark_two};
    width: 20px;
    border-top-left-radius: 4px;
    border-bottom-left-radius: 4px;
    subcontrol-position: left;
    subcontrol-origin: margin;
}}
QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal
{{
     background: none;
}}
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal
{{
     background: none;
}}
QScrollBar:vertical {{
    border: none;
    background: {bg_three};
    width: 8px;
    margin: 21px 0 21px 0;
    border-radius: 0px;
}}
QScrollBar:vertical:disabled {{
    background: {bg_disabled};
}}
QScrollBar::handle:vertical {{
    background: {context_color};
    min-height: 25px;
    border-radius: 4px
}}
QScrollBar::handle:vertical:disabled {{
    background: {fg_disabled};
}}
QScrollBar::handle:vertical:hover {{
    background: {context_hover};
    min-height: 25px;
    border-radius: 4px
}}
QScrollBar::handle:vertical:pressed {{
    background: {context_pressed};
    min-height: 25px;
    border-radius: 4px
}}
QScrollBar::add-line:vertical {{
    border: none;
    background: {dark_two};
    height: 20px;
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}}
QScrollBar::sub-line:vertical {{
    border: none;
    background: {dark_two};
    height: 20px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    subcontrol-position: top;
    subcontrol-origin: margin;
}}
QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
     background: none;
}}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
     background: none;
}}

/* QSlider */
QSlider {{
    margin: 0px;
}}
QSlider::groove:horizontal {{
    border-radius: 10px;
    height: 20px;
    margin: 0px;
    background-color: {bg_elements};
}}
QSlider::groove:horizontal:hover {{
    background-color: {bg_elements};
}}
QSlider::handle:horizontal {{
    border: none;
    height: 16px;
    width: 16px;
    margin: 2px;
    border-radius: 8px;
    background-color: {context_color};
}}
QSlider::handle:horizontal:hover {{
    background-color: {context_hover};
}}
QSlider::handle:horizontal:pressed {{
    background-color: {context_pressed};
}}
QSlider::groove:vertical {{
    border-radius: 10px;
    width: 20px;
    margin: 0px;
    background-color: {bg_elements};
}}
QSlider::groove:vertical:hover {{
    background-color: {bg_elements};
}}
QSlider::handle:vertical {{
    border: none;
    height: 16px;
    width: 16px;
    margin: 2px;
    border-radius: 8px;
    background-color: {context_color};
}}
QSlider::handle:vertical:hover {{
    background-color: {context_hover};
}}
QSlider::handle:vertical:pressed {{
    background-color: {context_pressed};
}}

/* QSplitter */

/* This activates the hover which isn't active by default */
QSplitterHandle:hover {{
}}

/* QSplitter can only be correctly addressed by it's orientation property.
Also, one must take care that the splitter in vertical direction is actually
turned by 90 degrees, so you'll need to use i.e. width as height etc. */

/* Horizontal QSplitter */
QSplitter[orientation='1']::handle {{
    height: 2px;
    background-color: {bg_elements};
}}
QSplitter[orientation='1']::handle:hover {{
    background-color: {context_color};
}}

/* Vertical QSplitter */
QSplitter[orientation='2']::handle {{
    height: 2px;
    background-color: {bg_elements};
}}
QSplitter[orientation='2']::handle:hover {{
    background-color: {context_color};
}}

/* QTabWidget */
/*
QTabWidget lacks of proper qss background-color support.
See:
https://bugreports.qt.io/browse/QTBUG-33344
https://bugreports.qt.io/browse/QTBUG-68642
https://codereview.qt-project.org/c/qt/qtbase/+/230769/
Because of not inheriting the values properly each
widget of QTabWidget needs to be set manually.
*/
QTabWidget > QStackedWidget {{
    background-color: {bg_two};
    border-top-right-radius: 8px;
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
}}
QTabWidget > QStackedWidget > QWidget {{
    background-color: {bg_two};
    border-top-right-radius: 8px;
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
}}
 QTabWidget::pane {{
    background-color: {bg_two};
    border-top-right-radius: 8px;
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
}}

/* QTabBar */
QTabBar::tab {{
    background-color: {bg_three};
    color: {foreground};
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 12px;
}}
QTabBar::tab:hover {{
    background-color: {context_color};
    color: {active};
}}
QTabBar::tab:selected {{
    background-color: {bg_two};
    color: {foreground};
}}

/* QTextEdit */
QTextEdit {{
    color: {foreground};
    background-color: {bg_elements};
    padding: 10px;
    border-radius: 5px;
}}
QTextEdit:disabled {{
    color: {fg_disabled};
    background-color: {bg_disabled};
}}

/* QToolTip */
QToolTip {{
    background-color: {dark_one};
    color:{foreground};
    padding-left: 10px;
    padding-right: 10px;
    border: 0px solid transparent;
    border-left: 3px solid {context_color};
}}

/* QTreeView, QListView, QTableView, QTableWidget, QTreeWidget */
QTreeView,
QListView,
QTableView,
QTableWidget,
QTreeWidget {{
    color: {foreground};
    background-color: {bg_two};
    alternate-background-color: {bg_one};
    padding: 10px;
    border-radius: 5px;
}}
#frozen_column_table_view {{
    /* This QTableView must fix exactly at it's position over the real table */
    padding: 0px;

}}
#frozen_column_table_view QHeaderView::section:horizontal:last{{
    /* The last section of the frozen table's header isn't the real last one */
    border-right: 1px solid {dark_two};
}}
QTreeView:disabled,
QListView:disabled,
QTableView:disabled,
QTableWidget:disabled,
QTreeWidget:disabled {{
    color: {fg_disabled};
}}

QTableView::item QComboBox{{
    border-radius: 0px;
}}


QFrame #_left_column_frame {{
    background-color: {bg_two};
}}

QFrame#app_background {{
    background-color: {bg_one};
    border-color: {bg_two};
    border-style: solid;
    /* Those are the default values that are applied when the app is not
    maximized */
    border-radius: 10;
    border: 2px;
}}
QFrame {{
    color: {foreground};
    font: 9pt 'Segoe UI';
}}
/* Used for Frames, and other space covering widgets like title bar,
credit bar and widgets in the right column (mostly QFrame) */
#bg_two_frame {{
    background-color: {bg_two};
    border-radius: 8px;
}}
QFrame#title_bg_frame {{
    background-color: {bg_one};
    border-radius: 8px;
}}

QFrame#div {{
    background: {dark_two};
    border-radius: 0;
}}

.QLabel {{
    font: 9pt "Segoe UI";
    color: {foreground};
    padding-left: 10px;
    padding-right: 10px;
}}
/* Label that has no padding on the left side */
QLabel#left_label {{
    font: 9pt "Segoe UI";
    color: {foreground};
    padding-left: 0px;
    padding-right: 10px;
}}
QLabel#heading_label {{
    font: 14pt "Segoe UI";
}}
QLabel#db_label {{
    color: red;
    font-weight: bold;
}}
QLabel:disabled {{
    color: {fg_disabled};
}}
QLabel#heading_label {{
    font: 14pt "Segoe UI";
}}
QLabel#heading1_label {{
    font: 12pt "Segoe UI";
    background: {dark_one};
    border-radius: 8px;
}}
QLabel#heading2_label {{
    font: 10pt "Segoe UI";
    background: {bg_two};
    border-radius: 8px;
}}
/* Completer */
#completer_popup{{
    border: 1px;
    border-color: {context_pressed};
    border-style: solid;
}}
QListView#completer_popup{{
    padding: 0px 10px 0px 10px;
}}

/* Background around the LeftMenu */
QFrame#menu_background {{
    background-color: {dark_one};
    border-radius: 8px;
}}

QLabel#column_title_label {{
    font-size: 10pt;
    color: {foreground};
    padding-bottom: 2px;
}}

/* CornerGrip and EdgeGrip are transparent. */
#grip {{
    background: transparent;
}}

/* Style for tooltips on buttons. */
QLabel#label_tooltip {{
    background-color: {dark_one};
    color: {foreground};
    padding-left: 10px;
    padding-right: 10px;
    border-radius: 17px;
    border: 0px solid transparent;
    border-left: 3px solid {context_color};
    font: 800 9pt "Segoe UI";
}}

QLabel#title_label {{
    font: 10pt "Segoe UI";
    color: {foreground};
}}
QLabel#about_toolbox {{
    font: 9pt "Segoe UI";
    color: {foreground};
}}
QMessageBox{{
    background-color: {dark_two};
    border-left: 3px solid {context_color};
    font: 9pt "Segoe UI";
    color: {foreground};
}}
QPushButton{{
    background-color: {bg_elements};
    color: {active};
    padding-left: 10px;
    padding-right: 10px;
    border-radius: 17px;
    border: 10px solid transparent;
    font: 600 9pt "Segoe UI";
}}
QPushButton:hover {{
    background-color: {context_color};
}}
QPushButton:pressed {{
    background-color: {context_pressed};
}}
QPushButton:checked {{
    background-color: {context_pressed};
}}
QPushButton#info_widget_btn{{
    background-color: {dark_one};
    color: {foreground};
    padding-left: 10px;
    padding-right: 10px;
    border-radius: 17px;
    border: 10px solid transparent;
    border-left: 3px solid {context_color};
    font: 800 9pt "Segoe UI";
}}

QPushButton[cssClass="red"] {{ background-color: {red}; color: black;}}
QPushButton[cssClass="red"]:hover {{ background-color: {light_red};
color: black;}}
QPushButton[cssClass="red"]:pressed {{ background-color: {dark_red};
color: black;}}

QPushButton[cssClass="green"] {{ background-color: {green};
color: black;}}
QPushButton[cssClass="green"]:hover {{ background-color: {light_green};
color: black;}}
QPushButton[cssClass="green"]:pressed {{ background-color: {dark_green};
color: black;}}

QPushButton[cssClass="yellow"] {{ background-color: {yellow};
color: black;}}
QPushButton[cssClass="yellow"]:hover {{ background-color: {light_yellow};
color: black;}}
QPushButton[cssClass="yellow"]:pressed {{ background-color: {dark_yellow};
color: black;}}

QPushButton#info_widget_btn:hover {{
    background-color: {dark_two};
}}
QPushButton#info_widget_btn:pressed {{
    background-color: {dark_one};
}}
QPushButton#info_widget_btn:disabled{{
    color: {fg_disabled};
    background-color: {bg_disabled};
}}
    """
