"""Custom qute_style (QStyle)."""

from __future__ import annotations

import contextlib
import logging
from collections.abc import Generator
from typing import cast

from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QBrush, QColor, QPainter, QPalette, QPen
from PySide6.QtWidgets import (
    QCheckBox,
    QProxyStyle,
    QStyle,
    QStyleOption,
    QStyleOptionButton,
    QStyleOptionViewItem,
    QWidget,
)

from qute_style.style import get_color, get_current_style
from qute_style.widgets.custom_icon_engine import PixmapStore

log = logging.getLogger(
    f"qute_style.{__name__}"
)  # pylint: disable=invalid-name


@contextlib.contextmanager
def painter_save(painter: QPainter) -> Generator[QPainter, None, None]:
    """
    Context manager that saves and restores the state of a QPainter.

    Usage:
    ```py
    with painter(painter):
        painter.setBrush(QColor(Qt.red))
        painter.drawRectangle(QRect(0, 0, 10, 10))
    ```
    """
    painter.save()
    yield painter
    painter.restore()


class ToggleOptionButton(  # pylint: disable=too-few-public-methods
    QStyleOptionButton
):
    """
     Custom QStyleOptionButton to allow transport of position.

    This class is necessary so that we will not need to pass the Toggle element
    to QStyle (and to create a circular reference) to get the current position
    of the switch. Obviously and additionally, this is also the correct way of
    passing properties from a QWidget to QStyle for painting.
    """

    def __init__(self) -> None:
        """Create a new ToggleOptionButton."""
        super().__init__()
        self._position = 0

    @property
    def position(self) -> int:
        """Get the position of the Toggle."""
        return self._position

    @position.setter
    def position(self, value: int) -> None:
        """Set the position of the Toggle."""
        self._position = value


class QuteStyle(QProxyStyle):
    """Custom style for a Qute Style application."""

    # Custom ControlElement for drawControl method.
    CE_Toggle = QStyle.ControlElement(QStyle.ControlElement.CE_CustomBase + 1)

    # This is the cache that holds QPalettes already created, since they will
    # not change unless the user changes the theme.
    PALETTE_CACHE: dict[str, QPalette] = {}

    # The different color names from which a QPalette for a style is created.
    # The comments reflect the description within the Qt documentation, for the
    # sake of completeness all descriptions are present, even if we set no
    # color for the ColorGroup and ColorRole

    PALETTE_COLOR_NAMES = (
        # QPalette::Window: A general background color.
        # QPalette::WindowText: A general foreground color.
        (
            QPalette.ColorGroup.Normal,
            QPalette.ColorRole.WindowText,
            "foreground",
        ),
        (
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.WindowText,
            "fg_disabled",
        ),
        (
            QPalette.ColorGroup.Inactive,
            QPalette.ColorRole.WindowText,
            "foreground",
        ),
        # QPalette::Base: Used mostly as the background color for text entry
        # widgets, but can also be used for other painting - such as the
        # background of combobox drop down lists and toolbar handles.
        # It is usually white or another light color.
        (QPalette.ColorGroup.Normal, QPalette.ColorRole.Base, "dark_one"),
        (QPalette.ColorGroup.Disabled, QPalette.ColorRole.Base, "bg_disabled"),
        (QPalette.ColorGroup.Inactive, QPalette.ColorRole.Base, "dark_one"),
        # QPalette::AlternateBase: Used as the alternate background color in
        # views with alternating row colors
        # (see QAbstractItemView::setAlternatingRowColors()).
        (
            QPalette.ColorGroup.Normal,
            QPalette.ColorRole.AlternateBase,
            "bg_elements",
        ),
        (
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.AlternateBase,
            "bg_disabled",
        ),
        (
            QPalette.ColorGroup.Inactive,
            QPalette.ColorRole.AlternateBase,
            "bg_three",
        ),
        # QPalette::ToolTipBase: Used as the background color for QToolTip and
        # QWhatsThis. Tool tips use the Inactive color group of QPalette,
        # because tool tips are not active windows.
        # QPalette::ToolTipText: Used as the foreground color for QToolTip and
        # QWhatsThis. Tool tips use the Inactive color group of QPalette,
        # because tool tips are not active windows.
        # QPalette::PlaceholderText: Used as the placeholder color for various
        # text input widgets. This enum value has been introduced in Qt 5.12
        # QPalette::Text: The foreground color used with Base. This is usually
        # the same as the WindowText, in which case it must provide good
        # contrast with Window and Base.
        (QPalette.ColorGroup.Normal, QPalette.ColorRole.Text, "foreground"),
        (QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, "fg_disabled"),
        (QPalette.ColorGroup.Inactive, QPalette.ColorRole.Text, "foreground"),
        # QPalette::Button: The general button background color. This
        # background can be different from Window as some styles require a
        # different background color for buttons.
        (QPalette.ColorGroup.Normal, QPalette.ColorRole.Button, "bg_one"),
        (QPalette.ColorGroup.Disabled, QPalette.ColorRole.Button, "bg_two"),
        (QPalette.ColorGroup.Inactive, QPalette.ColorRole.Button, "bg_three"),
        # QPalette::ButtonText: A foreground color used with the Button color.
        (
            QPalette.ColorGroup.Normal,
            QPalette.ColorRole.ButtonText,
            "foreground",
        ),
        (
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.ButtonText,
            "fg_disabled",
        ),
        (
            QPalette.ColorGroup.Inactive,
            QPalette.ColorRole.ButtonText,
            "foreground",
        ),
        # QPalette::BrightText: A text color that is very different from
        # WindowText, and contrasts well with e.g. Dark. Typically, used for
        # text that needs to be drawn where Text or WindowText would give poor
        # contrast, such as on pressed push buttons. Note that text colors
        # can be used for things other than just words; text colors are
        # usually used for text, but it's quite common to use the text color
        # roles for lines, icons, etc.
        # QPalette::Highlight: A color to indicate a selected item or the
        # current item. By default, the highlight color is Qt::darkBlue.
        (
            QPalette.ColorGroup.Normal,
            QPalette.ColorRole.Highlight,
            "context_color",
        ),
        (
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.Highlight,
            "context_color",
        ),
        (
            QPalette.ColorGroup.Inactive,
            QPalette.ColorRole.Highlight,
            "context_color",
        ),
        # QPalette::HighlightedText: A text color that contrasts with
        # Highlight. By default, the highlighted text color is Qt::white.
        (
            QPalette.ColorGroup.Normal,
            QPalette.ColorRole.HighlightedText,
            "foreground",
        ),
        (
            QPalette.ColorGroup.Disabled,
            QPalette.ColorRole.HighlightedText,
            "fg_disabled",
        ),
        (
            QPalette.ColorGroup.Inactive,
            QPalette.ColorRole.HighlightedText,
            "foreground",
        ),
    )

    class QCheckBoxOptions:  # pylint: disable=too-few-public-methods
        """QCheckBox configuration."""

        # Space between the checkbox and the text.
        SPACER = 3

        ICON_PATH = {
            Qt.CheckState.PartiallyChecked: ":/svg_icons/partial_checked.svg",
            Qt.CheckState.Checked: ":/svg_icons/checked.svg",
        }

        @staticmethod
        def text_option(option: QStyleOptionButton) -> QStyleOptionButton:
            """Return the option to draw the text for a QCheckBox."""
            text_option = QStyleOptionButton(option)
            offset = (
                option.iconSize.width() + QuteStyle.QCheckBoxOptions.SPACER
            )
            text_option.rect = QRect(
                offset,
                0,
                option.rect.width() - offset,
                option.rect.height(),
            )
            return text_option

    class ToggleOptions:  # pylint: disable=too-few-public-methods
        """Toggle configuration."""

        # This is the offset with which the circle is shown on both sides and
        # on top and bottom of the box.
        CIRCLE_OFFSET = 3

        # Diameter of the circle.
        CIRCLE_SIZE = 16

        # Font definitions
        FONT_SIZE = 9
        # Todo: This font is not a good font for the ui. fix with 70912
        FONT_NAME = "Segoe UI"

        # Width and height of the Box
        BOX_WIDTH = 40
        BOX_HEIGHT = CIRCLE_SIZE + (2 * CIRCLE_OFFSET)

        # Spacer between the text and the toggle box.
        SPACER = 5

        # Duration of the animation.
        ANIM_DURATION = 500

        # Corner radius to draw the rounded background rect
        BACKGROUND_RECT_RADIUS = 12

        @staticmethod
        def toggle_x(option: QStyleOption) -> int:
            """Calculate x position of Toggle box."""
            if option.direction == Qt.LayoutDirection.LeftToRight:
                return 0
            # cast Qt.RightToLeft
            return (
                cast(int, option.rect.width())
                - QuteStyle.ToggleOptions.BOX_WIDTH
            )

        @staticmethod
        def label_x(option: QStyleOption) -> int:
            """Calculate x position of label."""
            if option.direction == Qt.LayoutDirection.LeftToRight:
                return (
                    QuteStyle.ToggleOptions.BOX_WIDTH
                    + QuteStyle.ToggleOptions.SPACER
                )
            # cast Qt.RightToLeft
            return 0

        @staticmethod
        def text_option(option: ToggleOptionButton) -> QStyleOptionButton:
            """Return the option to draw the text for a QCheckBox."""
            text_option = QStyleOptionButton(option)
            text_option.rect = QRect(
                QuteStyle.ToggleOptions.label_x(option),
                0,
                option.rect.width()
                - QuteStyle.ToggleOptions.BOX_WIDTH
                - QuteStyle.ToggleOptions.SPACER,
                option.rect.height(),
            )
            return text_option

        @staticmethod
        def toggle_rect(option: ToggleOptionButton) -> QRect:
            """Create the Toggle's rect for drawing the background."""
            return QRect(
                QuteStyle.ToggleOptions.toggle_x(option),
                0,
                QuteStyle.ToggleOptions.BOX_WIDTH,
                QuteStyle.ToggleOptions.BOX_HEIGHT,
            )

    def standardPalette(  # noqa: N802
        self,
    ) -> QPalette:
        """Return the QStyle's standard QPalette."""
        style = get_current_style()
        try:
            return QuteStyle.PALETTE_CACHE[style]
        except KeyError:
            QuteStyle.PALETTE_CACHE[style] = self._create_palette()
            return QuteStyle.PALETTE_CACHE[style]

    def _create_palette(self) -> QPalette:
        """Create a Palette for the color names for the current style."""
        palette = super().standardPalette()
        for group, role, name in QuteStyle.PALETTE_COLOR_NAMES:
            palette.setColor(group, role, QColor(get_color(name)))
        return palette

    def drawControl(  # noqa: N802
        self,
        element: QStyle.ControlElement,
        option: QStyleOption,
        painter: QPainter,
        widget: QWidget | None = None,
    ) -> None:
        """Draw a control element."""
        if element == self.CE_Toggle:
            if isinstance(option, ToggleOptionButton):
                self._draw_toggle(option, painter, widget)
                return
        elif element == self.ControlElement.CE_CheckBox:
            if isinstance(option, QStyleOptionButton) and isinstance(
                widget, QCheckBox
            ):
                self._draw_checkbox(option, painter, widget)
                return
        elif element == QStyle.ControlElement.CE_CheckBoxLabel and isinstance(
            option, QStyleOptionButton
        ):
            self._draw_check_box_label(option, painter, widget)
            return
        super().drawControl(element, option, painter, widget)

    def _draw_checkbox(
        self, option: QStyleOptionButton, painter: QPainter, widget: QCheckBox
    ) -> None:
        """Draw a QCheckBox."""
        self._draw_indicator_checkbox(option, painter, widget)
        text_option = QuteStyle.QCheckBoxOptions.text_option(option)
        self.drawControl(
            QStyle.ControlElement.CE_CheckBoxLabel,
            text_option,
            painter,
            widget,
        )

    def _draw_check_box_label(
        self,
        option: QStyleOptionButton,
        painter: QPainter,
        widget: QWidget | None,
    ) -> None:
        option.text = option.fontMetrics.elidedText(
            option.text, Qt.TextElideMode.ElideRight, option.rect.width()
        )
        # Qt will use the Normal color, no matter what (this is visible in
        # the Qt source code for QStyle::drawItemText). Therefore, we need
        # to set the correct text color for a disabled text element into
        # the QPalette.Normal role.
        if not option.state & QStyle.StateFlag.State_Enabled:
            role = QPalette.ColorRole.WindowText
            disabled_color = option.palette.color(
                QPalette.ColorGroup.Disabled, role
            )
            option.palette.setColor(
                QPalette.ColorGroup.Normal, role, disabled_color
            )
        super().drawControl(
            QStyle.ControlElement.CE_CheckBoxLabel, option, painter, widget
        )

    def _draw_indicator_checkbox(
        self, option: QStyleOptionButton, painter: QPainter, widget: QWidget
    ) -> None:
        # Get Qt's default rectangle for drawing a CheckBox
        check_option = QStyleOptionButton(option)
        check_option.rect = self.subElementRect(
            self.SubElement.SE_CheckBoxIndicator, option, widget
        )
        self.drawPrimitive(
            self.PrimitiveElement.PE_IndicatorCheckBox,
            check_option,
            painter,
            widget,
        )

    def _draw_toggle(
        self,
        option: ToggleOptionButton,
        painter: QPainter,
        widget: QWidget | None,
    ) -> None:
        self._draw_toggle_background(option, painter)
        self._draw_toggle_circle(option, painter)

        if option.text:
            self.drawControl(
                QStyle.ControlElement.CE_CheckBoxLabel,
                QuteStyle.ToggleOptions.text_option(option),
                painter,
                widget,
            )

    @staticmethod
    def _draw_toggle_circle(
        option: ToggleOptionButton, painter: QPainter
    ) -> None:
        """Draw the Toggle's circle."""
        with painter_save(painter):
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(QuteStyle.button_foreground(option)))
            painter.drawEllipse(
                QuteStyle.ToggleOptions.toggle_x(option) + option.position,
                QuteStyle.ToggleOptions.CIRCLE_OFFSET,
                QuteStyle.ToggleOptions.CIRCLE_SIZE,
                QuteStyle.ToggleOptions.CIRCLE_SIZE,
            )

    @staticmethod
    def _draw_toggle_background(
        option: ToggleOptionButton, painter: QPainter
    ) -> None:
        """Draw the Toggle's background."""
        with painter_save(painter):
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QColor(QuteStyle.button_background(option)))
            painter.drawRoundedRect(
                QuteStyle.ToggleOptions.toggle_rect(option),
                QuteStyle.ToggleOptions.BACKGROUND_RECT_RADIUS,
                QuteStyle.ToggleOptions.BACKGROUND_RECT_RADIUS,
            )

    def drawPrimitive(  # noqa: N802
        self,
        element: QStyle.PrimitiveElement,
        option: QStyleOption,
        painter: QPainter,
        widget: QWidget | None = None,
    ) -> None:
        """Draw a primitive Element."""
        if element == self.PrimitiveElement.PE_FrameFocusRect:
            # Disable the drawing of a rectangle with a dashed line around a
            # focussed item. This was disabled when implementing the QStyle
            # to replace StyledCheckboxDelegate.
            return
        if element == self.PrimitiveElement.PE_PanelItemViewItem:
            if isinstance(option, QStyleOptionViewItem):
                self._panel_draw_item_view_item(option, painter, widget)
                return
        elif element == self.PrimitiveElement.PE_IndicatorCheckBox:
            if isinstance(option, QStyleOptionButton | QStyleOptionViewItem):
                self._draw_primitive_indicator_checkbox(option, painter)
                return
        elif element == self.PrimitiveElement.PE_IndicatorBranch:
            self._draw_branch(option, painter)
            return
        super().drawPrimitive(element, option, painter, widget)

    @staticmethod
    def _get_branch_color(option: QStyleOption) -> str:
        """Select the right Branch color."""
        if option.state & QStyle.StateFlag.State_MouseOver:
            return get_color("context_hover")
        return get_color("foreground")

    @staticmethod
    def _get_branch_icon(option: QStyleOption) -> str:
        """Select the right Branch Icon."""
        if option.state & QStyle.StateFlag.State_Open:
            return ":/svg_icons/arrow_down.svg"
        return ":/svg_icons/arrow_right.svg"

    def _draw_branch(self, option: QStyleOption, painter: QPainter) -> None:
        """Draw the branch arrow."""
        if not option.state & QStyle.StateFlag.State_Children:
            return

        self.draw_pixmap(
            painter,
            option.rect.adjusted(
                option.rect.width() - option.rect.height(), 0, 0, 0
            ),
            self._get_branch_icon(option),
            self._get_branch_color(option),
        )

    @staticmethod
    def _draw_primitive_indicator_checkbox(
        option: QStyleOptionButton | QStyleOptionViewItem,
        painter: QPainter,
    ) -> None:
        """Draw a checkbox."""
        QuteStyle._draw_checkbox_background(option, painter)
        QuteStyle._draw_checkbox_frame(option, painter)

        # Draw check mark if checkbox is checked. Note that State_NoChange
        # indeed is the QStyle.State for Qt.PartiallyChecked.
        if (
            option.state & QStyle.StateFlag.State_On  # type: ignore
            or option.state & QStyle.StateFlag.State_NoChange  # type: ignore
        ):
            QuteStyle._draw_checkbox_check(option, painter)

    @staticmethod
    def _draw_checkbox_background(
        option: QStyleOptionButton | QStyleOptionViewItem,
        painter: QPainter,
    ) -> None:
        """Draw the checkbox background rectangle."""
        with painter_save(painter):
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(QuteStyle._cb_background_color(option)))
            painter.drawRoundedRect(option.rect, 2, 2)  # type: ignore

    @staticmethod
    def _draw_checkbox_frame(
        option: QStyleOptionButton | QStyleOptionViewItem,
        painter: QPainter,
    ) -> None:
        # Draw the frame around the rectangle depending on mouse over
        with painter_save(painter):
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.setPen(QPen(QuteStyle._cb_frame_color(option)))
            painter.drawRoundedRect(
                option.rect.adjusted(1, 1, -1, -1), 1, 1  # type: ignore
            )

    @staticmethod
    def _draw_checkbox_check(
        option: QStyleOptionButton | QStyleOptionViewItem,
        painter: QPainter,
    ) -> None:
        """Draw the check of the checkbox."""
        state = (
            Qt.CheckState.Checked
            if option.state & QStyle.StateFlag.State_On  # type: ignore
            else Qt.CheckState.PartiallyChecked
        )
        QuteStyle.draw_pixmap(
            painter,
            option.rect.adjusted(1, 1, -1, -1),  # type: ignore
            QuteStyle.QCheckBoxOptions.ICON_PATH[state],
            QuteStyle.button_foreground(option).name(),
        )

    @staticmethod
    def _cb_frame_color(
        option: QStyleOptionButton | QStyleOptionViewItem,
    ) -> QColor:
        """Get the frame color of a checkbox."""
        if not option.state & QStyle.StateFlag.State_Enabled:  # type: ignore
            role = QPalette.ColorRole.Window
        elif option.state & QStyle.StateFlag.State_MouseOver:  # type: ignore
            role = QPalette.ColorRole.Highlight
        else:
            role = QPalette.ColorRole.WindowText
        return cast(
            QColor,
            option.palette.color(  # type: ignore
                QPalette.ColorGroup.Normal, role
            ),
        )

    @staticmethod
    def _cb_background_color(
        option: QStyleOptionButton | QStyleOptionViewItem,
    ) -> QColor:
        """Get the background color of a checkbox."""
        if option.state & QStyle.StateFlag.State_Enabled:  # type: ignore
            group = QPalette.ColorGroup.Normal
        else:
            group = QPalette.ColorGroup.Disabled
        return cast(
            QColor,
            option.palette.color(  # type: ignore
                group, QPalette.ColorRole.AlternateBase
            ),
        )

    def _panel_draw_item_view_item(
        self,
        option: QStyleOptionViewItem,
        painter: QPainter,
        widget: QWidget | None,
    ) -> None:
        """Draw a view item for a QAbstractItemView."""
        painter.save()
        brush = self._item_view_item_background_brush(option)
        if option.showDecorationSelected and (
            option.state & QStyle.StateFlag.State_Selected
            or option.state & QStyle.StateFlag.State_MouseOver
        ):
            painter.fillRect(option.rect, brush)
        else:
            if (
                cast(QBrush, option.backgroundBrush).style()
                != Qt.BrushStyle.NoBrush
            ):
                old_brush_origin = painter.brushOrigin()
                painter.setBrushOrigin(option.rect.topLeft())
                painter.fillRect(option.rect, option.backgroundBrush)
                painter.setBrushOrigin(old_brush_origin)

            if option.state & QStyle.StateFlag.State_Selected:
                assert widget
                text_rect = self.subElementRect(
                    QStyle.SubElement.SE_ItemViewItemText, option, widget
                )
                painter.fillRect(text_rect, brush)
        painter.restore()

    @staticmethod
    def _item_view_item_background_brush(
        option: QStyleOptionViewItem,
    ) -> QBrush:
        """Return the brush for painting an ItemView's item background."""
        if (
            option.state & QStyle.StateFlag.State_MouseOver
            and not option.state & QStyle.StateFlag.State_Selected
        ):
            return QBrush(QColor(get_color("context_hover")))
        if option.state & QStyle.StateFlag.State_Enabled:
            if option.state & QStyle.StateFlag.State_Active:
                color_group = QPalette.ColorGroup.Normal
            else:
                color_group = QPalette.ColorGroup.Inactive
        else:
            color_group = QPalette.ColorGroup.Disabled
        return cast(
            QBrush,
            option.palette.brush(color_group, QPalette.ColorRole.Highlight),
        )

    @staticmethod
    def draw_pixmap(
        painter: QPainter, rect: QRect, path: str, color: str
    ) -> None:
        """Draws a picture into the given rect respecting scale of screen."""
        painter.save()
        scale = painter.device().devicePixelRatio()
        pixmap = PixmapStore.inst().get_pixmap(
            path,
            int(scale * rect.width()),
            int(scale * rect.height()),
            color,
        )
        painter.drawPixmap(rect, pixmap)
        painter.restore()

    @staticmethod
    def button_foreground(option: QStyleOption) -> QColor:
        """Return a button's foreground color depending on option."""
        if (
            option.state & QStyle.StateFlag.State_Selected
            or option.state & QStyle.StateFlag.State_MouseOver
        ):
            return cast(
                QColor,
                option.palette.color(
                    QPalette.ColorGroup.Normal, QPalette.ColorRole.ButtonText
                ),
            )
        if option.state & QStyle.StateFlag.State_Enabled:
            return cast(
                QColor,
                option.palette.color(
                    QPalette.ColorGroup.Normal, QPalette.ColorRole.ButtonText
                ),
            )
        return cast(
            QColor,
            option.palette.color(
                QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText
            ),
        )

    @staticmethod
    def button_background(option: QStyleOptionButton) -> QColor:
        """Return a button's background color depending on option."""
        if option.state & QStyle.StateFlag.State_On:
            return cast(
                QColor,
                option.palette.color(
                    QPalette.ColorGroup.Normal, QPalette.ColorRole.Highlight
                ),
            )
        return (
            cast(
                QColor,
                option.palette.color(
                    QPalette.ColorGroup.Normal,
                    QPalette.ColorRole.AlternateBase,
                ),
            )
            if option.state & QStyle.StateFlag.State_Enabled
            else cast(
                QColor,
                option.palette.color(
                    QPalette.ColorGroup.Disabled,
                    QPalette.ColorRole.AlternateBase,
                ),
            )
        )
