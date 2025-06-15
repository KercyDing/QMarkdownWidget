import sys
from qtpy.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, 
    QSplitter, QTextEdit, QTabWidget, QScrollArea
)
from qtpy.QtCore import Qt
from QMarkdownWidget import QMLabel, QMView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QMarkdownWidget Interactive Demo")
        self.setGeometry(100, 100, 1000, 700)

        # --- Central Splitter ---
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(main_splitter)

        # --- Left Panel (Input) ---
        self.editor = QTextEdit()
        self.editor.setPlaceholderText("Type your Markdown here...")
        self.editor.textChanged.connect(self.update_markdown)
        main_splitter.addWidget(self.editor)

        # --- Right Panel (Output Tabs) ---
        self.tabs = QTabWidget()
        
        # QMLabel Tab
        self.label = QMLabel()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.label)
        self.tabs.addTab(scroll_area, "QMLabel")
        
        # QMView Tab
        self.view = QMView()
        self.view.setAutoSize(True, max_width=600)
        self.tabs.addTab(self.view, "QMView")
        
        main_splitter.addWidget(self.tabs)

        # --- Initial Content ---
        initial_text = """
# Interactive Markdown Demo

Type in the editor on the left to see the output update in real-time.

---

## Features

- **Styling**: Bold, Italic, `Code`
- **Lists**:
  - Unordered lists
  - Ordered lists
- **Code Blocks**:
```python
def greet(name):
    print(f"Hello, {name}!")

greet("World")
```
- **LaTeX (via MathJax in QMView)**:
  - Inline math: $E = mc^2$
  - Display math: $$ \\sum_{i=1}^{N} w_i x_i $$

Switch between the **QMLabel** and **QMView** tabs to see the differences in rendering.
        """
        self.editor.setText(initial_text)
        
        # --- Final Setup ---
        main_splitter.setSizes([400, 600])

    def update_markdown(self):
        markdown_text = self.editor.toPlainText()
        self.label.setMarkdown(markdown_text)
        self.view.setMarkdown(markdown_text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 