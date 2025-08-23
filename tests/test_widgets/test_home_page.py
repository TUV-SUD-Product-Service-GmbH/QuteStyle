"""Tests for HomePage."""

from unittest.mock import Mock, patch

import pytest
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget
from pytestqt.qtbot import QtBot

from qute_style.dev.dev_functions import VersionInfo
from qute_style.widgets.base_widgets import MainWidget
from qute_style.widgets.home_page import HomePage, StackedWidget, WidgetType


# Mock widget class for testing
class MockMainWidget(MainWidget):
    """Mock main widget for testing."""

    NAME = "Mock Widget"
    ICON = ":/svg_icons/info.svg"

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize mock widget."""
        super().__init__(parent)


@pytest.fixture(name="app_info")
def fixture_app_info() -> tuple[str, str, str]:
    """Return mock app info."""
    return ("Test App", ":/svg_images/test_logo.svg", "en")


@pytest.fixture(name="visible_widgets")
def fixture_visible_widgets() -> list[type[MainWidget]]:
    """Return mock visible widgets list."""
    return [MockMainWidget]


@pytest.fixture(name="mock_qsettings")
def fixture_mock_qsettings() -> Mock:  # type: ignore
    """Mock QSettings to control theme selection behavior."""
    with patch("qute_style.widgets.home_page.QSettings") as mock_settings:
        mock_instance = Mock()
        mock_settings.return_value = mock_instance
        yield mock_instance


@pytest.fixture(name="home_page")
def fixture_home_page(
    qtbot: QtBot,
    app_info: tuple[str, str, str],
    visible_widgets: list[type[MainWidget]],
    mock_qsettings: Mock,
) -> HomePage:
    """Create a HomePage for testing."""
    # Mock QSettings to not show theme selection initially
    mock_qsettings.value.return_value = False
    mock_qsettings.setValue = Mock()

    home_page = HomePage(app_info, visible_widgets)
    qtbot.addWidget(home_page)
    home_page.show()
    qtbot.waitExposed(home_page)
    return home_page


class TestWidgetType:
    """Test WidgetType enum."""

    @staticmethod
    def test_enum_values() -> None:
        """Test that WidgetType has correct values."""
        assert WidgetType.HOMEPAGE == 0  # type: ignore
        assert WidgetType.VERSION_HISTORY == 1  # type: ignore
        assert WidgetType.STYLE_WIDGET == 2  # type: ignore

    @staticmethod
    def test_enum_count() -> None:
        """Test that WidgetType has exactly 3 values."""
        assert len(list(WidgetType)) == 3


class TestStackedWidget:
    """Test StackedWidget functionality."""

    @staticmethod
    @pytest.fixture(name="stacked_widget")
    def fixture_stacked_widget(qtbot: QtBot) -> StackedWidget:
        """Create a StackedWidget for testing."""
        widget = StackedWidget()
        qtbot.addWidget(widget)

        # Add some test widgets
        test_widget1 = QWidget()
        test_widget2 = QWidget()
        test_widget3 = QWidget()

        widget.addWidget(test_widget1)
        widget.addWidget(test_widget2)
        widget.addWidget(test_widget3)

        return widget

    @staticmethod
    def test_initialization(stacked_widget: StackedWidget) -> None:
        """Test StackedWidget initialization."""
        assert not stacked_widget._animation_running
        assert stacked_widget._animation is not None
        assert stacked_widget._animation.duration() == 400

    @staticmethod
    def test_widget_selected_signal_exists(
        stacked_widget: StackedWidget,
    ) -> None:
        """Test that StackedWidget has widget_selected signal."""
        assert hasattr(stacked_widget, "widget_selected")

    @staticmethod
    def test_set_current_index_no_animation(
        qtbot: QtBot, stacked_widget: StackedWidget
    ) -> None:
        """Test set_current_index without animation."""
        with qtbot.waitSignal(stacked_widget.widget_selected) as blocker:
            stacked_widget.set_current_index(1, animate=False)

        assert stacked_widget.currentIndex() == 1
        assert blocker.args[0] == 1

    @staticmethod
    def test_set_current_index_with_animation(
        qtbot: QtBot, stacked_widget: StackedWidget
    ) -> None:
        """Test set_current_index with animation."""
        with qtbot.waitSignal(stacked_widget.widget_selected) as blocker:
            stacked_widget.set_current_index(2, animate=True)

        assert stacked_widget.currentIndex() == 2
        assert blocker.args[0] == 2
        # Animation should be running after calling with animate=True
        assert stacked_widget._animation_running

    @staticmethod
    def test_set_current_index_during_animation(
        stacked_widget: StackedWidget,
    ) -> None:
        """Test set_current_index while animation is running."""
        # Manually set animation running
        stacked_widget._animation_running = True
        original_index = stacked_widget.currentIndex()

        stacked_widget.set_current_index(2, animate=True)

        # Index should not change during animation
        assert stacked_widget.currentIndex() == original_index

    @staticmethod
    def test_set_current_index_same_index(
        stacked_widget: StackedWidget,
    ) -> None:
        """Test set_current_index with same index as current."""
        current_index = stacked_widget.currentIndex()
        stacked_widget.set_current_index(current_index, animate=True)

        # Should remain the same
        assert stacked_widget.currentIndex() == current_index

    @staticmethod
    def test_on_animation_finished(stacked_widget: StackedWidget) -> None:
        """Test animation finished callback."""
        stacked_widget._animation_running = True
        stacked_widget.on_animation_finished()
        assert not stacked_widget._animation_running


class TestHomePage:
    """Test HomePage functionality."""

    @staticmethod
    def test_initialization(home_page: HomePage) -> None:
        """Test HomePage initialization."""
        assert home_page.NAME == "Information"
        assert home_page.ICON == ":/svg_icons/home.svg"
        assert hasattr(home_page, "change_theme")

    @staticmethod
    def test_app_info_stored(
        qtbot: QtBot,
        app_info: tuple[str, str, str],
        visible_widgets: list[type[MainWidget]],
        mock_qsettings: Mock,
    ) -> None:
        """Test that app info is properly stored."""
        mock_qsettings.value.return_value = False

        home_page = HomePage(app_info, visible_widgets)
        qtbot.addWidget(home_page)

        assert home_page._app_name == "Test App"
        assert home_page._app_logo == ":/svg_images/test_logo.svg"
        assert home_page._app_lang == "en"

    @staticmethod
    def test_visible_widgets_stored(
        qtbot: QtBot,
        app_info: tuple[str, str, str],
        visible_widgets: list[type[MainWidget]],
        mock_qsettings: Mock,
    ) -> None:
        """Test that visible widgets are properly stored."""
        mock_qsettings.value.return_value = False

        home_page = HomePage(app_info, visible_widgets)
        qtbot.addWidget(home_page)

        assert home_page._visible_widgets == visible_widgets

    @staticmethod
    def test_widget_stack_created(home_page: HomePage) -> None:
        """Test that widget stack is created."""
        assert hasattr(home_page, "_widget_stack")
        assert isinstance(home_page._widget_stack, StackedWidget)

    @staticmethod
    def test_select_buttons_created(home_page: HomePage) -> None:
        """Test that selection buttons are created."""
        assert hasattr(home_page, "_select_buttons")
        assert WidgetType.HOMEPAGE in home_page._select_buttons
        assert WidgetType.VERSION_HISTORY in home_page._select_buttons
        assert WidgetType.STYLE_WIDGET in home_page._select_buttons

    @staticmethod
    def test_initial_widget_homepage(
        qtbot: QtBot,
        app_info: tuple[str, str, str],
        visible_widgets: list[type[MainWidget]],
        mock_qsettings: Mock,
    ) -> None:
        """Test initial widget when theme selection is disabled."""
        mock_qsettings.value.return_value = False

        home_page = HomePage(app_info, visible_widgets)
        qtbot.addWidget(home_page)

        assert home_page._widget_stack.currentIndex() == WidgetType.HOMEPAGE

    @staticmethod
    def test_initial_widget_theme_selection(
        qtbot: QtBot,
        app_info: tuple[str, str, str],
        visible_widgets: list[type[MainWidget]],
        mock_qsettings: Mock,
    ) -> None:
        """Test initial widget when theme selection is enabled."""
        mock_qsettings.value.return_value = True

        home_page = HomePage(app_info, visible_widgets)
        qtbot.addWidget(home_page)

        assert (
            home_page._widget_stack.currentIndex() == WidgetType.STYLE_WIDGET
        )
        # Should disable theme selection after showing it
        mock_qsettings.setValue.assert_called_with(
            "CustomThemeSelectionActive", False
        )

    @staticmethod
    def test_on_index_changed(home_page: HomePage) -> None:
        """Test on_index_changed method."""
        # Test changing to version history
        home_page.on_index_changed(WidgetType.VERSION_HISTORY)
        assert home_page._select_buttons[
            WidgetType.VERSION_HISTORY
        ].isChecked()

        # Test changing to style widget
        home_page.on_index_changed(WidgetType.STYLE_WIDGET)
        assert home_page._select_buttons[WidgetType.STYLE_WIDGET].isChecked()

    @staticmethod
    def test_button_connections(qtbot: QtBot, home_page: HomePage) -> None:
        """Test that buttons are connected to stack navigation."""
        # Test homepage button
        with qtbot.waitSignal(home_page._widget_stack.widget_selected):
            home_page._select_buttons[WidgetType.HOMEPAGE].clicked.emit()

        # Test version history button
        with qtbot.waitSignal(home_page._widget_stack.widget_selected):
            home_page._select_buttons[
                WidgetType.VERSION_HISTORY
            ].clicked.emit()

        # Test style widget button
        with qtbot.waitSignal(home_page._widget_stack.widget_selected):
            home_page._select_buttons[WidgetType.STYLE_WIDGET].clicked.emit()

    @staticmethod
    def test_widget_stack_signal_connection(home_page: HomePage) -> None:
        """Test that widget stack signal is connected."""
        # Simulate widget selection
        home_page._widget_stack.widget_selected.emit(
            WidgetType.VERSION_HISTORY
        )

        # Check that corresponding button is checked
        assert home_page._select_buttons[
            WidgetType.VERSION_HISTORY
        ].isChecked()


class TestHomePageWelcomeWidget:
    """Test HomePage welcome widget creation."""

    @staticmethod
    def test_create_welcome_widget(home_page: HomePage) -> None:
        """Test welcome widget creation."""
        welcome_widget = home_page._create_welcome_widget()

        assert welcome_widget is not None
        assert isinstance(welcome_widget, QWidget)

        # Check for expected layout and widgets
        layout = welcome_widget.layout()
        assert layout is not None

        # Should have label and SVG widget
        # Note: We can't easily test for QSvgWidget without more complex setup


class TestHomePageVersionHistory:
    """Test HomePage version history functionality."""

    @staticmethod
    @patch("qute_style.widgets.home_page.QFile")
    def test_create_version_history_no_data(
        mock_qfile: Mock,
        qtbot: QtBot,
        app_info: tuple[str, str, str],
        visible_widgets: list[type[MainWidget]],
        mock_qsettings: Mock,
    ) -> None:
        """Test version history creation with no data."""
        # Mock file operations to return no data
        mock_file_instance = Mock()
        mock_file_instance.open.return_value = False
        mock_qfile.return_value = mock_file_instance

        mock_qsettings.value.return_value = False

        home_page = HomePage(app_info, visible_widgets)
        qtbot.addWidget(home_page)

        version_widget = home_page._create_version_history_widget()
        assert version_widget is not None

    @staticmethod
    @patch("qute_style.widgets.home_page.pickle.loads")
    @patch("qute_style.widgets.home_page.QFile")
    def test_create_version_history_with_data(
        mock_qfile: Mock,
        mock_pickle_loads: Mock,
        home_page: HomePage,
    ) -> None:
        """Test version history creation with mock data."""
        # Mock file operations
        mock_file_instance = Mock()
        mock_file_instance.open.return_value = True
        mock_file_instance.readAll.return_value.data.return_value = (
            b"mock_data"
        )
        mock_qfile.return_value = mock_file_instance

        # Mock pickle data
        version_info = VersionInfo("1.0.0", "2023-01-01")
        mock_data = {
            version_info: {
                "Test App": [{"en": "Test change 1"}, {"en": "Test change 2"}],
                "MockMainWidget": [{"en": "Widget change 1"}],
            }
        }
        mock_pickle_loads.return_value = mock_data

        version_widget = home_page._create_version_history_widget()
        assert version_widget is not None

    @staticmethod
    def test_fill_version_info_no_data(home_page: HomePage) -> None:
        """Test fill_version_info with no data."""
        from PySide6.QtWidgets import QGridLayout, QWidget

        widget = QWidget()
        layout = QGridLayout(widget)

        home_page.fill_version_info(layout, {}, [])

        # Should add a "no entries" label
        assert layout.count() > 0

    @staticmethod
    def test_fill_version_info_with_data(home_page: HomePage) -> None:
        """Test fill_version_info with mock data."""
        from PySide6.QtWidgets import QGridLayout, QWidget

        widget = QWidget()
        layout = QGridLayout(widget)

        version_info = VersionInfo("1.0.0", "2023-01-01")
        mock_data = {
            version_info: {
                "Test App": [{"en": "Test change 1"}],
            }
        }

        home_page.fill_version_info(layout, mock_data, [MockMainWidget])

        # Should add version info and changes
        assert layout.count() > 0

    @staticmethod
    def test_add_item_to_grid_app_icon(home_page: HomePage) -> None:
        """Test _add_item_to_grid with app icon."""
        from PySide6.QtWidgets import QGridLayout, QWidget

        widget = QWidget()
        layout = QGridLayout(widget)

        row = home_page._add_item_to_grid(
            layout,
            0,
            ("Test App", ":/svg_images/test_logo.svg"),
            ["Test change"],
        )

        assert row > 0
        assert layout.count() > 0

    @staticmethod
    def test_add_item_to_grid_widget_icon(home_page: HomePage) -> None:
        """Test _add_item_to_grid with widget icon."""
        from PySide6.QtWidgets import QGridLayout, QWidget

        widget = QWidget()
        layout = QGridLayout(widget)

        row = home_page._add_item_to_grid(
            layout,
            0,
            ("Mock Widget", ":/svg_icons/info.svg"),
            ["Widget change"],
        )

        assert row > 0
        assert layout.count() > 0


class TestHomePageStyleSelection:
    """Test HomePage style selection functionality."""

    @staticmethod
    @patch("qute_style.widgets.home_page._create_theme_drawing")
    @patch("qute_style.widgets.home_page.THEMES")
    def test_create_style_selection_widget(
        mock_themes: Mock, mock_create_theme: Mock, home_page: HomePage
    ) -> None:
        """Test style selection widget creation."""
        # Mock themes with proper structure
        mock_themes.items.return_value = [
            ("Dark", {"bg_one": "#000000"}),
            ("Light", {"bg_one": "#ffffff"}),
        ]
        # Mock the theme drawing function to return a valid
        # pixmap-compatible object
        mock_create_theme.return_value = QSize(300, 200)

        style_widget = home_page._create_style_selection_widget()

        assert style_widget is not None
        assert isinstance(style_widget, QWidget)

    @staticmethod
    @patch("qute_style.widgets.home_page._create_theme_drawing")
    @patch("qute_style.widgets.home_page.THEMES")
    def test_theme_selection_signal(
        mock_themes: Mock,
        mock_create_theme: Mock,
        qtbot: QtBot,
        home_page: HomePage,
    ) -> None:
        """Test theme selection signal emission."""
        # Mock themes with proper structure
        mock_themes.items.return_value = [
            ("Test Theme", {"bg_one": "#000000"})
        ]
        # Mock the theme drawing to return QSize
        mock_create_theme.return_value = QSize(300, 200)

        style_widget = home_page._create_style_selection_widget()

        # Find theme buttons - they should be QPushButton instances
        from PySide6.QtWidgets import QPushButton

        buttons = style_widget.findChildren(QPushButton)

        # Filter for theme buttons (not the navigation buttons)
        theme_buttons = [
            btn
            for btn in buttons
            if btn.parent() != home_page and btn.iconSize().width() > 0
        ]

        if theme_buttons:
            with qtbot.waitSignal(home_page.change_theme) as blocker:
                theme_buttons[0].clicked.emit()

            assert blocker.args[0] == "Test Theme"

    @staticmethod
    def test_check_show_theme_selection_widget_true() -> None:
        """Test _check_show_theme_selection_widget returns True."""
        with patch("qute_style.widgets.home_page.QSettings") as mock_settings:
            mock_instance = Mock()
            mock_instance.value.return_value = True
            mock_settings.return_value = mock_instance

            result = HomePage._check_show_theme_selection_widget()

            assert result is True
            mock_instance.setValue.assert_called_with(
                "CustomThemeSelectionActive", False
            )

    @staticmethod
    def test_check_show_theme_selection_widget_false() -> None:
        """Test _check_show_theme_selection_widget returns False."""
        with patch("qute_style.widgets.home_page.QSettings") as mock_settings:
            mock_instance = Mock()
            mock_instance.value.return_value = False
            mock_settings.return_value = mock_instance

            result = HomePage._check_show_theme_selection_widget()

            assert result is False
            mock_instance.setValue.assert_called_with(
                "CustomThemeSelectionActive", False
            )


class TestHomePageEdgeCases:
    """Test HomePage edge cases and error conditions."""

    @staticmethod
    def test_empty_visible_widgets_list(
        qtbot: QtBot,
        app_info: tuple[str, str, str],
        mock_qsettings: Mock,
    ) -> None:
        """Test HomePage with empty visible widgets list."""
        mock_qsettings.value.return_value = False

        home_page = HomePage(app_info, [])
        qtbot.addWidget(home_page)

        assert home_page._visible_widgets == []
        assert isinstance(home_page._widget_stack, StackedWidget)

    @staticmethod
    def test_invalid_app_info(
        qtbot: QtBot,
        visible_widgets: list[type[MainWidget]],
        mock_qsettings: Mock,
    ) -> None:
        """Test HomePage with different app info formats."""
        mock_qsettings.value.return_value = False

        # Test with minimal info
        minimal_info = ("App", "logo.svg", "de")
        home_page = HomePage(minimal_info, visible_widgets)
        qtbot.addWidget(home_page)

        assert home_page._app_name == "App"
        assert home_page._app_logo == "logo.svg"
        assert home_page._app_lang == "de"

    @staticmethod
    def test_multiple_theme_changes(qtbot: QtBot, home_page: HomePage) -> None:
        """Test multiple rapid theme changes."""
        # Simulate multiple theme change signals
        themes = ["Dark", "Light", "Blue"]

        for theme in themes:
            home_page.change_theme.emit(theme)
            # Should not cause any errors

    @staticmethod
    def test_widget_stack_with_many_index_changes(home_page: HomePage) -> None:
        """Test widget stack with rapid index changes."""
        for _i in range(3):
            for widget_type in WidgetType:
                home_page._widget_stack.set_current_index(
                    widget_type, animate=False
                )
                assert home_page._widget_stack.currentIndex() == widget_type
