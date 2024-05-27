"""TextTruncator is a widget that is able to truncate and store texts."""

from __future__ import annotations

from collections import defaultdict

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics, QStaticText


class TextTruncator:  # pylint: disable=too-few-public-methods
    """
    TextTruncator is a widget that is able to truncate and store texts.

    The class is intended to be used as a mixin for classes that will need to
    truncate their texts and store them as a QStaticText.
    """

    def __init__(self) -> None:
        """Create a new TextTruncator."""
        self._text_sizes: dict[str, dict[int, QStaticText]] = defaultdict(dict)
        self._font_metrics: QFontMetrics | None = None

    def truncate_text(
        self,
        text: str,
        width: int,
        font_metrics: QFontMetrics | None = None,
    ) -> QStaticText:
        """
        Truncate a text so that if fits into the text_rect.

        This function uses memoization based on the given text and width.

        If no font_metrics is given, one must be set with `font_metrics`
        """
        try:
            return self._text_sizes[text][width]
        except KeyError:
            if not font_metrics:
                font_metrics = self._font_metrics
            assert font_metrics
            elided_text = font_metrics.elidedText(
                text, Qt.TextElideMode.ElideRight, width
            )
            self._text_sizes[text][width] = QStaticText(elided_text)

            # Activate AggressiveCaching (better performance, more memory)
            self._text_sizes[text][width].setTextFormat(
                Qt.TextFormat.PlainText
            )
            self._text_sizes[text][width].setPerformanceHint(
                QStaticText.PerformanceHint.AggressiveCaching
            )
            return self._text_sizes[text][width]
