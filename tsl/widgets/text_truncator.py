"""TextTruncator is a widget that is able to truncate and store texts."""
from collections import defaultdict
from typing import Dict, Optional

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFontMetrics, QStaticText


class TextTruncator:  # pylint: disable=too-few-public-methods
    """
    TextTruncator is a widget that is able to truncate and store texts.

    The class is intended to be used as a mixin for classes that will need to
    truncate their texts and store them as a QStaticText.
    """

    def __init__(self) -> None:
        """Create a new TextTruncator."""
        self._text_sizes: Dict[str, Dict[int, QStaticText]] = defaultdict(dict)
        self._font_metrics: Optional[QFontMetrics] = None

    def truncate_text(
        self,
        text: str,
        width: int,
        font_metrics: QFontMetrics = None,
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
            elided_text = font_metrics.elidedText(text, Qt.ElideRight, width)
            self._text_sizes[text][width] = QStaticText(elided_text)

            # Activate AggressiveCaching (better performance, more memory)
            self._text_sizes[text][width].setTextFormat(Qt.PlainText)
            self._text_sizes[text][width].setPerformanceHint(
                QStaticText.AggressiveCaching
            )
            return self._text_sizes[text][width]
