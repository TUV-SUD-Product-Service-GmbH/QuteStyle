"""TSLStyledMessageBox definition for custom Darcula style."""
from typing import Optional, Union, cast

from PyQt5.QtCore import QPoint, QRect, Qt
from PyQt5.QtGui import QBitmap, QColor, QPainter, QPalette
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsDropShadowEffect,
    QMessageBox,
    QWidget,
)

from tsl.style import get_color


class TSLMessageBox(QMessageBox):
    """Custom TSLMessageBox."""

    # The desired border radius
    _radius = 12

    def __init__(
        self, parent: Optional[QWidget] = None, title: str = "", text: str = ""
    ) -> None:
        """Init function."""
        super().__init__(parent)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setMinimumSize(300, 300)
        self.setWindowTitle(title)
        self.setText(f"<h3>{title}</h3>\n{text}")

        # Here come the styling bits...First need the frameless window flag
        # hint
        self.setWindowFlags(
            self.windowFlags()  # type: ignore
            | Qt.FramelessWindowHint
            | Qt.WindowSystemMenuHint
        )

        # Style the box with CSS. Set the border radius here.
        # The border style helps blend the corners, but could be omitted.
        # The background is optional... could add other styling here too.
        stylesheet = """
            QDialog {{
                border-radius: {}px;
                border: 2px solid {};
                background-color: palette(base);
                }}
            QMessageBox {{
                background-color:{};
                }}
            .QLabel {{
                color: {};
                }}
            """

        border_color = get_color("context_color")
        background_color = get_color("bg_one")
        text_color = get_color("foreground")
        self.setStyleSheet(
            stylesheet.format(
                TSLMessageBox._radius,
                border_color,
                background_color,
                text_color,
            )
        )

        # The effect will not be actually visible outside the rounded window,
        # but it does help get rid of the pixelated rounded corners.
        effect = QGraphicsDropShadowEffect()
        # The color should match the border color set in CSS.
        effect.setColor(QApplication.palette().color(QPalette.Shadow))
        effect.setBlurRadius(5)
        self.setGraphicsEffect(effect)

    @staticmethod
    def information(
        parent: Optional[QWidget],
        title: str,
        text: str,
        buttons: Union[
            QMessageBox.StandardButtons, QMessageBox.StandardButton
        ] = QMessageBox.Ok,
        default_button: QMessageBox.StandardButton = QMessageBox.Ok,
    ) -> QMessageBox.StandardButton:
        """Show information message box."""
        return TSLMessageBox._show_message_box(
            parent,
            title,
            text,
            QMessageBox.Information,
            buttons,
            default_button,
        )

    @staticmethod
    def warning(
        parent: Optional[QWidget],
        title: str,
        text: str,
        buttons: Union[
            QMessageBox.StandardButtons, QMessageBox.StandardButton
        ] = QMessageBox.Ok,
        default_button: QMessageBox.StandardButton = QMessageBox.Ok,
    ) -> QMessageBox.StandardButton:
        """Show warning message box."""
        return TSLMessageBox._show_message_box(
            parent, title, text, QMessageBox.Warning, buttons, default_button
        )

    @staticmethod
    def critical(
        parent: Optional[QWidget],
        title: str,
        text: str,
        buttons: Union[
            QMessageBox.StandardButtons, QMessageBox.StandardButton
        ] = QMessageBox.Ok,
        default_button: QMessageBox.StandardButton = QMessageBox.Ok,
    ) -> QMessageBox.StandardButton:
        """Show warning message box."""
        return TSLMessageBox._show_message_box(
            parent, title, text, QMessageBox.Critical, buttons, default_button
        )

    @staticmethod
    def question(
        parent: Optional[QWidget],
        title: str,
        text: str,
        buttons: Union[
            QMessageBox.StandardButtons, QMessageBox.StandardButton
        ] = QMessageBox.Yes
        | QMessageBox.No,
        default_button: QMessageBox.StandardButton = QMessageBox.Yes,
    ) -> QMessageBox.StandardButton:
        """Show warning message box."""
        return TSLMessageBox._show_message_box(
            parent,
            title,
            text,
            QMessageBox.Question,
            buttons,
            default_button,
        )

    @staticmethod
    def _show_message_box(  # pylint: disable=too-many-arguments
        parent: Optional[QWidget],
        title: str,
        text: str,
        icon: QMessageBox.Icon,
        buttons: Union[
            QMessageBox.StandardButtons, QMessageBox.StandardButton
        ] = QMessageBox.Ok,
        default_button: QMessageBox.StandardButton = QMessageBox.Ok,
    ) -> QMessageBox.StandardButton:
        """Show message box."""
        msg_box = TSLMessageBox(parent, title, text)
        msg_box.setIcon(icon)
        msg_box.setStandardButtons(buttons)
        msg_box.setDefaultButton(default_button)
        # Need to show the box before to get it's proper dimensions.
        msg_box.show()
        # Here we draw the mask to cover the "cut off" corners,
        # otherwise they show through. The mask is sized based on the
        # current window geometry. If the window were resizable (somehow)
        # then the mask would need to be set in resizeEvent().
        rect = QRect(QPoint(0, 0), msg_box.geometry().size())
        bitmap = QBitmap(rect.size())
        bitmap.fill(QColor(Qt.color0))
        painter = QPainter(bitmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.color1)
        # this radius should match the CSS radius
        painter.drawRoundedRect(
            rect,
            TSLMessageBox._radius,
            TSLMessageBox._radius,
            Qt.AbsoluteSize,
        )
        painter.end()
        msg_box.setMask(bitmap)
        return cast(QMessageBox.StandardButton, msg_box.exec())
