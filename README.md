# QMarkdownWidget

[![PyPI version](https://img.shields.io/pypi/v/QMarkdownWidget?p=1)](https://pypi.org/project/QMarkdownWidget/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`QMarkdownWidget` is a Python library that provides modern and feature-rich widgets for rendering Markdown and LaTeX in PyQt and PySide applications. It offers two distinct components tailored for different use cases.

## Features

- **`QMLabel`**: A lightweight and efficient widget based on `QLabel` for rendering simple Markdown. It's fast and ideal for displaying basic formatted text without the overhead of a full web engine.
- **`QMView`**: A powerful widget based on `QWebEngineView` for displaying complex Markdown documents. 
- They offer:
    - **Full GFM (GitHub-Flavored Markdown) support**.
    - **High-quality LaTeX rendering** via MathJax(**only QMView supports**).
    - **Advanced auto-sizing** to precisely fit its content.
    - **Full styling capabilities** using both QSS and internal CSS.

## Installation

You can install `QMarkdownWidget` from PyPI:
```bash
pip install QMarkdownWidget
```

## Usage

Here are some examples of how to use the widgets.

### Basic `QMLabel` Usage

`QMLabel` is as simple to use as a standard `QLabel`.

```python
import sys
from qtpy.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from QMarkdownWidget import QMLabel

app = QApplication(sys.argv)
window = QMainWindow()
central_widget = QWidget()
layout = QVBoxLayout(central_widget)

label_text = """
# This is a QMLabel
- Renders **basic** Markdown.
- Very *lightweight*.
"""
label = QMLabel(label_text)
layout.addWidget(label)

window.setCentralWidget(central_widget)
window.show()
sys.exit(app.exec())
```

### Basic `QMView` Usage

`QMView` can handle much more complex content, including LaTeX and code blocks.

```python
import sys
from qtpy.QtWidgets import QApplication, QMainWindow
from QMarkdownWidget import QMView

app = QApplication(sys.argv)
window = QMainWindow()

view_text = r"""
# This is a QMView
It supports **Markdown** and LaTeX, like $E=mc^2$
"""
view = QMView(view_text)
window.setCentralWidget(view)
window.show()
sys.exit(app.exec())
```

### Advanced: `QMView` Auto-Sizing

The `setAutoSize` method gives you powerful control over the widget's layout.

```python
import sys
from qtpy.QtWidgets import QApplication, QMainWindow
from QMarkdownWidget import QMView

# 1. Basic auto-sizing: shrinks to fit content
view1 = QMView("Shrinks to fit.")
view1.setAutoSize(True)

# 2. Width-constrained: content wraps at 300px, height adjusts
view2 = QMView("This long text will wrap...")
view2.setAutoSize(True, max_width=300)

# 3. Height-constrained: content is clipped at 150px with a scrollbar
view3 = QMView("This tall content will be scrollable...")
view3.setAutoSize(True, max_height=150)

...
```

## API Reference

### `QMLabel`
A lightweight widget for simple Markdown.

- `__init__(self, text: str = "", parent=None)`
  - Initializes the label with optional Markdown text.

- `setMarkdown(self, text: str)`
  - Renders and displays a new Markdown string.

### `QMView`
A full-featured widget for complex Markdown, code, and LaTeX.

- `__init__(self, text: str = "", parent=None)`
  - Initializes the view with optional Markdown text.

- `setMarkdown(self, text: str)`
  - Renders and displays a new Markdown string.

- `setAutoSize(self, enabled: bool, max_width: int = -1, max_height: int = -1)`
  - Enables or disables auto-sizing.
  - **`enabled`**: If `True`, the widget shrinks to fit its content. If `False`, it expands to fill available space.
  - **`max_width`**: Constrains the content's width, forcing text to wrap. The widget's height will adjust accordingly.
  - **`max_height`**: Constrains the widget's height. If content is taller, a vertical scrollbar will appear.

- `setHtmlStyle(self, style: str)`
  - Injects a custom CSS string to style the internal HTML content. This is useful for changing fonts, colors, etc., beyond what QSS can target.

## Contributing

Contributions, issues, and feature requests are welcome! Please feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. 