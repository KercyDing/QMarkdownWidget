# src/QMarkdownWidget/qm_label.py

from qtpy.QtWidgets import QLabel, QSizePolicy
from qtpy.QtGui import QPalette, QColor, QFont
from markdown_it import MarkdownIt

class QMLabel(QLabel):
    """
    A lightweight widget for rendering simple Markdown.
    It is efficient but does not support complex rendering, scrolling, or text selection.
    """
    def __init__(self, text: str = "", parent=None):
        """
        Initialize the QMLabel.

        Args:
            text (str, optional): The initial Markdown text. Defaults to "".
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self._md = MarkdownIt()
        
        # Set default white background
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('white'))
        self.setPalette(palette)

        self.setMarkdown(text)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setWordWrap(True)
        self.setFont(QFont("Arial", 12))

    def setMarkdown(self, text: str):
        """
        Sets the widget's text from a Markdown string.

        Args:
            text (str): The Markdown string to render.
        """
        html = self._md.render(text)
        self.setText(html)