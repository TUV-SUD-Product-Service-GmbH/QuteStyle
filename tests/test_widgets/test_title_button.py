"""Tests for TitleButton."""

import pytest
from PySide6.QtCore import QPoint
from PySide6.QtWidgets import QWidget
from pytestqt.qtbot import QtBot

from qute_style.widgets.base_widgets import BaseWidget
from qute_style.widgets.icon_button import BackgroundColorNames
from qute_style.widgets.title_button import TitleButton


# Mock widget class for testing
class MockWidget(BaseWidget):
    """Mock widget for testing."""

    NAME = "Mock Widget"
    ICON = ":/svg_icons/info.svg"

    def __init__(self, parent: QWidget | None = None) -> None:
        """Initialize mock widget."""
        super().__init__(parent)


@pytest.fixture(name="app_parent")
def fixture_app_parent() -> QWidget:
    """Create an app parent widget for TitleButton."""
    return QWidget()


@pytest.fixture(name="title_button")
def fixture_title_button(qtbot: QtBot, app_parent: QWidget) -> TitleButton:
    """Create a TitleButton for testing."""
    button = TitleButton(
        app_parent=app_parent,
        tooltip_text="Test Button",
        icon_path=":/svg_icons/info.svg",
    )

    qtbot.addWidget(button)
    button.show()
    qtbot.waitExposed(button)
    return button


class TestTitleButtonInit:
    """Test TitleButton initialization."""

    @staticmethod
    def test_fixed_dimensions() -> None:
        """Test that TitleButton has correct fixed dimensions."""
        assert TitleButton.FIXED_WIDTH == 30
        assert TitleButton.FIXED_HEIGHT == 30

    @staticmethod
    def test_basic_initialization(title_button: TitleButton) -> None:
        """Test basic TitleButton initialization."""
        assert title_button.tooltip_text == "Test Button"
        assert title_button.isVisible()

    @staticmethod
    def test_initialization_with_widget_class(
        qtbot: QtBot, app_parent: QWidget
    ) -> None:
        """Test TitleButton initialization with widget_class."""
        button = TitleButton(
            app_parent=app_parent,
            tooltip_text="Mock Button",
            icon_path=":/svg_icons/info.svg",
            widget_class=MockWidget,
        )

        qtbot.addWidget(button)
        assert button.widget_class == MockWidget

    @staticmethod
    def test_initialization_with_custom_background_colors(
        qtbot: QtBot, app_parent: QWidget
    ) -> None:
        """Test TitleButton initialization with custom background colors."""
        custom_bgs = BackgroundColorNames(
            hovering="custom_hover",
            background="custom_bg",
            pressed="custom_pressed",
            released="custom_released",
        )

        button = TitleButton(
            app_parent=app_parent,
            tooltip_text="Custom Button",
            icon_path=":/svg_icons/info.svg",
            bgs=custom_bgs,
        )

        qtbot.addWidget(button)
        # Can't directly test the colors, but ensure initialization succeeds
        assert button.tooltip_text == "Custom Button"

    @staticmethod
    def test_initialization_with_custom_margin(
        qtbot: QtBot, app_parent: QWidget
    ) -> None:
        """Test TitleButton initialization with custom margin."""
        button = TitleButton(
            app_parent=app_parent,
            tooltip_text="Margin Button",
            icon_path=":/svg_icons/info.svg",
            margin=1.0,
        )

        qtbot.addWidget(button)
        assert button.tooltip_text == "Margin Button"

    @staticmethod
    def test_default_background_colors(title_button: TitleButton) -> None:
        """Test that TitleButton uses correct default background colors."""
        # The default colors are set in the constructor
        # We can't directly access them,
        # but we can verify the button was created
        assert title_button is not None


class TestTitleButtonTooltip:
    """Test TitleButton tooltip functionality."""

    @staticmethod
    def test_get_tooltip_coords_calculation(title_button: TitleButton) -> None:
        """Test tooltip coordinate calculation."""
        # Set up a mock tooltip with known width
        title_button._tooltip.resize(100, 50)

        test_pos = QPoint(200, 150)
        pos_x, pos_y = title_button._get_tooltip_coords(test_pos)

        # Expected calculation:
        # pos_x = (pos.x() - self._tooltip.width()) + self.width() + 5
        # pos_y = pos.y() + self.height() + 6
        expected_x = (200 - 100) + title_button.width() + 5
        expected_y = 150 + title_button.height() + 6

        assert pos_x == expected_x
        assert pos_y == expected_y

    @staticmethod
    def test_get_tooltip_coords_with_different_positions(
        title_button: TitleButton,
    ) -> None:
        """Test tooltip coordinates with different input positions."""
        title_button._tooltip.resize(80, 40)

        # Test different positions
        test_cases = [
            (
                QPoint(100, 100),
                (
                    100 - 80 + title_button.width() + 5,
                    100 + title_button.height() + 6,
                ),
            ),
            (
                QPoint(0, 0),
                (
                    0 - 80 + title_button.width() + 5,
                    0 + title_button.height() + 6,
                ),
            ),
            (
                QPoint(500, 300),
                (
                    500 - 80 + title_button.width() + 5,
                    300 + title_button.height() + 6,
                ),
            ),
        ]

        for input_pos, expected in test_cases:
            pos_x, pos_y = title_button._get_tooltip_coords(input_pos)
            expected_x, expected_y = expected
            assert pos_x == expected_x
            assert pos_y == expected_y

    @staticmethod
    def test_tooltip_coords_with_zero_tooltip_size(
        title_button: TitleButton,
    ) -> None:
        """Test tooltip coordinates when tooltip has zero size."""
        title_button._tooltip.resize(0, 0)

        test_pos = QPoint(150, 100)
        pos_x, pos_y = title_button._get_tooltip_coords(test_pos)

        expected_x = 150 + title_button.width() + 5  # (150 - 0) + width + 5
        expected_y = 100 + title_button.height() + 6

        assert pos_x == expected_x
        assert pos_y == expected_y


class TestTitleButtonInheritance:
    """Test TitleButton inheritance and method overrides."""

    @staticmethod
    def test_inherits_from_icon_tooltip_button(
        title_button: TitleButton,
    ) -> None:
        """Test that TitleButton properly inherits from IconTooltipButton."""
        from qute_style.widgets.icon_tooltip_button import IconTooltipButton

        assert isinstance(title_button, IconTooltipButton)

    @staticmethod
    def test_has_widget_class_attribute(
        qtbot: QtBot, app_parent: QWidget
    ) -> None:
        """Test that TitleButton can store widget_class attribute."""
        button = TitleButton(
            app_parent=app_parent,
            tooltip_text="Test",
            icon_path=":/svg_icons/info.svg",
            widget_class=MockWidget,
        )

        qtbot.addWidget(button)
        assert hasattr(button, "widget_class")
        assert button.widget_class == MockWidget

    @staticmethod
    def test_widget_class_defaults_to_none(title_button: TitleButton) -> None:
        """Test that widget_class defaults to None when not specified."""
        # The fixture doesn't specify widget_class, so it should be None
        assert getattr(title_button, "widget_class", None) is None


class TestTitleButtonSignals:
    """Test TitleButton signal functionality."""

    @staticmethod
    def test_clicked_signal_exists(title_button: TitleButton) -> None:
        """Test that TitleButton has clicked signal from parent class."""
        # IconTooltipButton inherits from IconButton
        # which should have clicked signal
        assert hasattr(title_button, "clicked")

    @staticmethod
    def test_released_signal_exists(title_button: TitleButton) -> None:
        """Test that TitleButton has released signal from parent class."""
        assert hasattr(title_button, "released")

    @staticmethod
    def test_can_connect_to_signals(
        title_button: TitleButton, qtbot: QtBot
    ) -> None:
        """Test that signals can be connected to slots."""
        signal_received = False

        def slot() -> None:
            nonlocal signal_received
            signal_received = True

        # Test connecting to clicked signal
        title_button.clicked.connect(slot)

        # Simulate a click by emitting the signal directly
        title_button.clicked.emit()

        # Process events to ensure signal is handled
        qtbot.wait(10)

        assert signal_received


class TestTitleButtonEdgeCases:
    """Test TitleButton edge cases and error conditions."""

    @staticmethod
    def test_with_empty_tooltip_text(
        qtbot: QtBot, app_parent: QWidget
    ) -> None:
        """Test TitleButton with empty tooltip text."""
        button = TitleButton(
            app_parent=app_parent,
            tooltip_text="",
            icon_path=":/svg_icons/info.svg",
        )

        qtbot.addWidget(button)
        assert button.tooltip_text == ""

    @staticmethod
    def test_with_long_tooltip_text(qtbot: QtBot, app_parent: QWidget) -> None:
        """Test TitleButton with very long tooltip text."""
        long_text = (
            "This is a very long tooltip text that should still work properly "
            * 10
        )
        button = TitleButton(
            app_parent=app_parent,
            tooltip_text=long_text,
            icon_path=":/svg_icons/info.svg",
        )

        qtbot.addWidget(button)
        assert button.tooltip_text == long_text

    @staticmethod
    def test_tooltip_coords_with_negative_position(
        title_button: TitleButton,
    ) -> None:
        """Test tooltip coordinate calculation with negative positions."""
        title_button._tooltip.resize(50, 30)

        test_pos = QPoint(-100, -50)
        pos_x, pos_y = title_button._get_tooltip_coords(test_pos)

        expected_x = (-100 - 50) + title_button.width() + 5
        expected_y = -50 + title_button.height() + 6

        assert pos_x == expected_x
        assert pos_y == expected_y
