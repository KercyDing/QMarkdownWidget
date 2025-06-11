import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

# 假设 QMarkdownWidget 已正确安装并可直接导入
from QMarkdownWidget import QMView

# Example Markdown content with code and math
MARKDOWN = r"""
# QSS Styling Test

This is a **QMView** demo.

- List item 1
- List item 2

```python
print('Hello, QSS!')
```

Inline math: $a^2 + b^2 = c^2$

$$
\int_0^1 x^2 dx = \frac{1}{3}
$$
"""

# QSS style for QMView (widget itself)
QSS = """
QMView {
    border: 2px solid #0078d7;
    border-radius: 8px;
    background: #f8faff;
    padding: 8px;
}
"""

# CSS for internal HTML (to be injected via setHtmlStyle)
HTML_CSS = """
body {
    color: #222;
    font-family: 'Segoe UI', Arial, sans-serif;
    background: #f8faff;
    margin: 0;
    padding: 8px;
}
h1 {
    color: #0078d7;
}
"""

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("QMView QSS Styling Test")
    
    central = QWidget()
    layout = QVBoxLayout(central)
    layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    view = QMView()
    view.setMarkdown(MARKDOWN)
    view.setHtmlStyle(HTML_CSS)  # Ensure internal HTML matches QSS
    view.setMinimumWidth(400)
    view.setAutoHeight(True)

    # Apply QSS to QMView
    view.setStyleSheet(QSS)

    layout.addWidget(view)
    window.setCentralWidget(central)
    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 