# src/QMarkdownWidget/qm_view.py

from qtpy.QtWebEngineWidgets import QWebEngineView
from qtpy.QtWebChannel import QWebChannel
from qtpy.QtCore import QObject, Signal, QTimer, Slot
from qtpy.QtGui import QPalette, QColor
from markdown_it import MarkdownIt

class Resizer(QObject):
    resized = Signal(int, int)

    @Slot(int, int)
    def resize_slot(self, width: int, height: int):
        self.resized.emit(width, height)

class QMView(QWebEngineView):
    """
    A widget based on QWebEngineView for displaying complex Markdown documents.
    It supports rich content including code blocks and LaTeX formulas,
    as well as scrolling and text selection.
    """
    def __init__(self, text: str = "", parent=None):
        """
        Initialize the QMView.

        Args:
            text (str, optional): The initial Markdown text. Defaults to "".
            parent (QWidget, optional): The parent widget. Defaults to None.
        """
        super().__init__(parent)
        self._md = MarkdownIt(
            'gfm-like',
            {'html': True, 'linkify': True, 'typographer': True, 'highlight': self._highlight}
        )
        self._html_style = ""
        self._text = text
        
        self._auto_size_enabled = False
        self._as_max_width = -1
        self._as_max_height = -1

        # --- Resizing mechanism ---
        self._resizer = Resizer()
        self._channel = QWebChannel()
        self._channel.registerObject('resizer', self._resizer)
        self.page().setWebChannel(self._channel)
        
        self._resizer.resized.connect(self._handle_resize)
        
        # Set default white background
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('white'))
        self.setPalette(palette)

        self.setMarkdown(text)

    def _highlight(self, code, lang, attrs):
        """Custom highlighter function for markdown-it."""
        if lang:
            return f'<pre><code class="language-{lang}">{code}</code></pre>'
        return f'<pre><code>{code}</code></pre>'

    def setMarkdown(self, text: str):
        """
        Renders and displays a Markdown string.

        Args:
            text (str): The Markdown string to render.
        """
        self._text = text
        body_html = self._md.render(text)
        full_html = self._create_html_template(body_html)
        self.setHtml(full_html)

    def setHtmlStyle(self, style: str):
        """
        Set the CSS style for the HTML content.

        Args:
            style (str): The CSS style string.
        """
        self._html_style = style
        self.setMarkdown(self._text)  # Re-render with new style

    def _create_html_template(self, content: str) -> str:
        """Creates a full HTML document with CSS and MathJax for styling."""
        
        content_style_parts = ["padding: 20px;", "display: inline-block;"]
        if self._auto_size_enabled:
            # This forces the div to its natural width, preventing the parent
            # layout from squashing it before its size is reported.
            content_style_parts.append("width: max-content;")
            
            if self._as_max_width > 0:
                # This will override `width: max-content` if the content is wider,
                # which is the desired wrapping behavior.
                content_style_parts.append(f"max-width: {self._as_max_width}px;")
        
        content_style = " ".join(content_style_parts)

        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <script src="qrc:///qtwebchannel/qwebchannel.js"></script>
    <script>
        document.addEventListener("DOMContentLoaded", function() {{
            new QWebChannel(qt.webChannelTransport, function (channel) {{
                window.resizer = channel.objects.resizer;
                
                const contentDiv = document.getElementById('content');
                if (!contentDiv) return;

                const observer = new ResizeObserver(entries => {{
                    for (let entry of entries) {{
                        const width = Math.ceil(entry.borderBoxSize[0].inlineSize);
                        const height = Math.ceil(entry.borderBoxSize[0].blockSize);
                        window.resizer.resize_slot(width, height);
                    }}
                }});
                
                observer.observe(contentDiv);
            }});
        }});
    </script>
    <script>
        MathJax = {{
            tex: {{
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']]
            }},
            svg: {{
                fontCache: 'global'
            }}
        }};
    </script>
    <script type="text/javascript" id="MathJax-script" async
        src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js">
    </script>
    <style>
        {self._html_style}
        html, body {{
            margin: 0;
            padding: 0;
            background-color: transparent; /* Let Python side control background */
            overflow-x: hidden; /* Prevent horizontal scrollbar on the main view */
        }}
        #content {{
            {content_style}
        }}
        /* Basic styles */
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        h1, h2, h3, h4, h5, h6, p, ul, ol {{
            margin-top: 0;
            margin-bottom: 0;
        }}
        h1, h2, h3, h4, h5, h6 {{
            font-weight: 600;
            line-height: 1.25;
        }}
        pre {{
            background-color: #f6f8fa;
            border-radius: 3px;
            font-size: 85%;
            line-height: 1.45;
            overflow: auto;
            padding: 16px;
        }}
        code {{
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
        }}
        th, td {{
            border: 1px solid #dfe2e5;
            padding: 6px 13px;
        }}
        th {{
            font-weight: 600;
        }}
    </style>
</head>
<body>
    <div id="content">
        {content}
    </div>
</body>
</html>
        """

    def setAutoSize(self, enabled: bool, max_width: int = -1, max_height: int = -1):
        """
        Enable or disable auto-sizing for the widget. When enabled, the widget
        will attempt to shrink to fit its content.

        Args:
            enabled (bool): True to enable auto-sizing, False to disable.
            max_width (int, optional): Constrains the content's max width,
                                       forcing text to wrap and affecting height.
            max_height (int, optional): Constrains the content's max height,
                                        which can affect its width.
        """
        self._auto_size_enabled = enabled
        self._as_max_width = max_width
        self._as_max_height = max_height

        if not enabled:
            # Revert to expanding behavior
            self.setMinimumSize(0, 0)
            self.setMaximumSize(16777215, 16777215)
        
        # Trigger a re-render to apply new CSS constraints
        self.setMarkdown(self._text)

    def _handle_resize(self, width: int, height: int):
        """Handles the resize signal from JavaScript."""
        if self._auto_size_enabled:
            final_width = width
            final_height = height

            # If a max_height constraint is set, apply it to the widget's height,
            # not the content's. This lets the main QWebEngineView scrollbar work.
            if self._as_max_height > 0:
                final_height = min(height, self._as_max_height)

            self.setFixedWidth(final_width)
            self.setFixedHeight(final_height) 