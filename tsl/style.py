"""Style handling for TSLStyleWindow."""
import logging
from typing import Dict, Optional

from PyQt5.QtCore import QSettings

log = logging.getLogger(f"tsl.{__name__}")  # pylint: disable=invalid-name

# Use this variable when referencing a default style so that adapting to a new
# default style will only require changes in the lib.
DEFAULT_STYLE = "Darcula"

CURRENT_STYLE: Optional[str] = None


def get_current_style() -> str:
    """Return the currently set style."""
    global CURRENT_STYLE  # pylint: disable=global-statement
    if CURRENT_STYLE is None:
        CURRENT_STYLE = QSettings().value("style", DEFAULT_STYLE)
        log.debug("Loaded current style from registry: %s", CURRENT_STYLE)
        if CURRENT_STYLE not in THEMES:
            log.warning("Invalid style stored in registry: %s", CURRENT_STYLE)
            # If an invalid style is set, revert to DEFAULT_STYLE
            CURRENT_STYLE = DEFAULT_STYLE
    return CURRENT_STYLE


def set_current_style(style: str) -> None:
    """
    Set the current style

    One should only use this method to change the style. This will correctly
    set CURRENT_STYLE to be used as a lazy variable.
    """
    log.debug("Setting current style to %s", style)
    global CURRENT_STYLE  # pylint: disable=global-statement
    CURRENT_STYLE = style
    QSettings().setValue("style", style)


THEMES: Dict[str, Dict[str, str]] = {
    "Snow White": {
        "dark_one": "#1b1e23",
        "dark_two": "#1e2229",
        "dark_three": "#21252d",
        "dark_four": "#272c36",
        "bg_one": "#D3E0F7",
        "bg_two": "#E2E9F7",
        "bg_three": "#EFF1F7",
        "bg_disabled": "#4a4d5f",
        "fg_disabled": "#575a6d",
        "icon_color": "#6C7C96",
        "icon_hover": "#8CB8FF",
        "icon_pressed": "#6c99f4",
        "icon_active": "#8CB8FF",
        "context_color": "#568af2",
        "context_hover": "#2b467a",
        "context_pressed": "#4B5469",
        "text_title": "#606C85",
        "text_foreground": "#6B7894",
        "text_description": "#7887A6",
        "text_active": "#8797BA",
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
        "dark_one": "#282a36",
        "dark_two": "#2B2E3B",
        "dark_three": "#333645",
        "dark_four": "#3C4052",
        "bg_one": "#44475a",
        "bg_two": "#4D5066",
        "bg_three": "#595D75",
        "bg_disabled": "#4a4d5f",
        "fg_disabled": "#575a6d",
        "icon_color": "#c3ccdf",
        "icon_hover": "#dce1ec",
        "icon_pressed": "#ff79c6",
        "icon_active": "#f5f6f9",
        "context_color": "#ff79c6",
        "context_hover": "#c55e99",
        "context_pressed": "#FF90DD",
        "text_title": "#dce1ec",
        "text_foreground": "#f8f8f2",
        "text_description": "#979EC7",
        "text_active": "#dce1ec",
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
        "dark_one": "#1b1e23",
        "dark_two": "#1e2229",
        "dark_three": "#21252d",
        "dark_four": "#272c36",
        "bg_one": "#2c313c",
        "bg_two": "#343b48",
        "bg_three": "#3c4454",
        "bg_disabled": "#4a4d5f",
        "fg_disabled": "#575a6d",
        "icon_color": "#c3ccdf",
        "icon_hover": "#dce1ec",
        "icon_pressed": "#6c99f4",
        "icon_active": "#f5f6f9",
        "context_color": "#568af2",
        "context_hover": "#6c99f4",
        "context_pressed": "#3f6fd1",
        "text_title": "#dce1ec",
        "text_foreground": "#8a95aa",
        "text_description": "#4f5b6e",
        "text_active": "#dce1ec",
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
    color: {text_foreground};
    background-color: {dark_one};
    border-radius: 5px;
    border: 2px solid {dark_one};
    padding: 5px;
    padding-left: 10px;
}}
QComboBox:hover{{
    border: 2px solid {dark_three};
}}
QComboBox::drop-down {{
    width: 25px;
    border-left-width: 3px;
    border-left-color: {bg_one};
    border-left-style: solid;
    border-top-right-radius: 3px;
    border-bottom-right-radius: 3px;
}}
QComboBox::down-arrow {{
    image: url(":/svg_icons/down.svg");
    width: 14px;
    height: 14px;
}}
QComboBox QAbstractItemView {{
    color: {text_foreground};
    background-color: {dark_one};
    padding: 10px;
    selection-background-color: {context_color};
}}
QComboBox:disabled {{
    color: {fg_disabled};
    background-color: {bg_disabled};
    border: {bg_disabled};
}}

/* QHeaderView */
QHeaderView{{
    background-color: {bg_two};
}}
QHeaderView::section{{
    color: {text_foreground};
    background-color: {bg_two};
    max-width: 30px;
    border: 0px;
    padding: 3px;
}}
QHeaderView::section:horizontal{{
    border-right: 1px solid {dark_three};
    border-bottom: 1px solid {dark_three};
}}
QHeaderView::section:horizontal:only-one{{
    border-right: 0px;
}}
QHeaderView::section:horizontal:last{{
    border-right: 0px;
}}
QHeaderView::section:vertical{{
    border-bottom: 1px solid {dark_three};
    border-right: 1px solid {dark_three};
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
QLineEdit {{
    background-color: {bg_two};
    border-radius: 8px;
    border: 1px solid transparent;
    padding-left: 10px;
    padding-right: 10px;
    selection-color: {text_active};
    selection-background-color: {context_color};
    color: {text_foreground};
    height: 30px;
}}
QLineEdit#column_line_edit {{
    background-color: {bg_one};
    border-radius: 8px;
    border: 1px solid transparent;
    padding-left: 10px;
    padding-right: 10px;
    selection-color: {text_active};
    selection-background-color: {context_color};
    color: {text_foreground};
}}
QLineEdit:focus {{
    border: 1px solid {context_color};
    background-color: {bg_one};
}}
QLineEdit#column_line_edit:focus {{
    border: 1px solid {context_color};
    background-color: {bg_two};
}}

/* QMenu */
QMenu{{
    background-color: {dark_one};
}}
QMenu QCheckBox{{
    color: {text_foreground};
    border-radius: 17px;
    border: 10px solid transparent;
}}
QMenu QCheckBox:hover {{
    background-color: {context_hover};
    color: {text_active};
}}
QMenu QCheckBox:pressed {{
    background-color: {context_pressed};
    color: {text_active};
}}
QMenu::separator {{
    background: {bg_three};
    height: 3px;
    margin-left: 5px;
    margin-right: 5px;
}}

/* QScrollBar */
QScrollBar:horizontal {{
    border: none;
    background: {bg_one};
    height: 8px;
    margin: 0px 21px 0 21px;
    border-radius: 0px;
}}
QScrollBar::handle:horizontal {{
    background: {context_color};
    min-width: 25px;
    border-radius: 4px
}}
QScrollBar::add-line:horizontal {{
    border: none;
    background: {dark_four};
    width: 20px;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    subcontrol-position: right;
    subcontrol-origin: margin;
}}
QScrollBar::sub-line:horizontal {{
    border: none;
    background: {dark_four};
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
    background: {bg_one};
    width: 8px;
    margin: 21px 0 21px 0;
    border-radius: 0px;
}}
QScrollBar::handle:vertical {{
    background: {context_color};
    min-height: 25px;
    border-radius: 4px
}}
QScrollBar::add-line:vertical {{
    border: none;
    background: {dark_four};
    height: 20px;
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
    subcontrol-position: bottom;
    subcontrol-origin: margin;
}}
QScrollBar::sub-line:vertical {{
    border: none;
    background: {dark_four};
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
    background-color: {dark_one};
}}
QSlider::groove:horizontal:hover {{
    background-color: {dark_two};
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
    background-color: {dark_one};
}}
QSlider::groove:vertical:hover {{
    background-color: {dark_two};
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
    background-color: {bg_three};
}}
QSplitter[orientation='1']::handle:hover {{
    background-color: {context_color};
}}

/* Vertical QSplitter */
QSplitter[orientation='2']::handle {{
    height: 2px;
    background-color: {bg_three};
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
    background-color: {bg_three};
    border-top-right-radius: 8px;
    border-bottom-left-radius: 8px;
    border-bottom-right-radius: 8px;
}}
QTabWidget > QStackedWidget > QWidget {{
    background-color: {bg_three};
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
    background-color: {bg_two};
    color: {text_foreground};
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 10px;
}}
QTabBar::tab:hover {{
    background-color: {context_color};
    color: {text_active};
}}
QTabBar::tab:selected {{
    background-color: {bg_three};
    color: {text_foreground};
}}

/* QTextEdit */
QTextEdit {{
    color: {text_foreground};
    background-color: {bg_two};
    padding: 10px;
    border-radius: 5px;
}}
QTextEdit:disabled {{
    color: {text_foreground};
    background-color: {bg_two};
}}

/* QToolTip */
QToolTip {{
    background-color: {dark_one};
    color:{text_foreground};
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
    color: {text_foreground};
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
    border-right: 1px solid {dark_three};
}}
QTreeView::item:hover,
QListView::item:hover,
QTableView::item:hover,
QTableWidget::item:hover,
QTreeWidget::item:hover{{
color: {text_active};
background-color: {context_hover};
}}
QTreeView::item:selected,
QListView::item:selected,
QTableView::item:selected,
QTableWidget::item:selected,
QTreeWidget::item:selected{{
color: {text_active};
background-color: {context_color};
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
    color: {text_foreground};
    font: 9pt 'Segoe UI';
}}
QFrame#title_bar_background {{
    background-color: {bg_two};
    border-radius: 8px;
}}

#bg_frame {{ /* background for the CreditBar */
    border-radius: 8px;
    background-color: {bg_two};
}}

QFrame#div {{
    background: {dark_four};
    border-radius: 0;
}}

.QLabel {{
    font: 9pt "Segoe UI";
    color: {text_description};
    padding-left: 10px;
    padding-right: 10px;
}}
/* Label that has no padding on the left side */
QLabel#left_label {{
    font: 9pt "Segoe UI";
    color: {text_description};
    padding-left: 0px;
    padding-right: 10px;
}}
QLabel#welcome_label {{
    font: 14pt "Segoe UI";
}}
/* Completer*/
#completer_popup{{
    color: {text_foreground};
    background-color: {dark_one};
    padding-left: 10px;
    width: 25px;
  }}
QFrame#title_bg_frame {{
    background-color: {bg_one};
    border-radius: 8px;
}}

/* Background around the LeftMenu */
QFrame#menu_background {{
    background-color: {dark_one};
    border-radius: 8px;
}}

QLabel#column_title_label {{
    font-size: 10pt;
    color: {text_foreground};
    padding-bottom: 2px;
}}

/* CornerGrip and EdgeGrip are transparent. */
#grip {{
    background: transparent;
}}

/* Style for tooltips on buttons. */
QLabel#label_tooltip {{
    background-color: {dark_one};
    color: {text_foreground};
    padding-left: 10px;
    padding-right: 10px;
    border-radius: 17px;
    border: 0px solid transparent;
    border-left: 3px solid {context_color};
    font: 800 9pt "Segoe UI";
}}

QLabel#title_label {{
    font: 10pt "Segoe UI";
    color: {text_foreground};
}}
QLabel#about_toolbox {{
    font: 9pt "Segoe UI";
    color: {text_foreground};
}}
QMessageBox{{
    background-color: {dark_four};
    border-left: 3px solid {context_color};
    font: 9pt "Segoe UI";
    text-color: {text_active};
}}
QPushButton{{
    background-color: {context_color};
    color: {text_active};
    padding-left: 10px;
    padding-right: 10px;
    border-radius: 17px;
    border: 10px solid transparent;
    font: 600 9pt "Segoe UI";
}}
QPushButton:hover {{
    background-color: {context_hover};
}}
QPushButton:pressed {{
    background-color: {context_pressed};
}}
QPushButton#info_widget_btn{{
    background-color: {dark_one};
    color: {text_foreground};
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
    background-color: {dark_four};
}}
QPushButton#info_widget_btn:pressed {{
    background-color: {dark_one};
}}
QPushButton#info_widget_btn:disabled{{
    color: {fg_disabled};
    background-color: {bg_disabled};
}}
    """
