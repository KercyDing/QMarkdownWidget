import sys
from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout, QLabel
)
from qtpy.QtCore import Qt
from QMarkdownWidget import QMView

class SizingComparisonDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QMView - setAutoSize Comparison")
        self.setGeometry(100, 100, 900, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        grid_layout = QGridLayout(central_widget)

        markdown_content = """
### Auto-Sizing Demo
This is a block of text to demonstrate different sizing behaviors.

- Unordered list item 1
- Unordered list item 2
- This is a slightly longer item to ensure wrapping occurs.
        """

        # --- 1. No Auto-Sizing (Default) ---
        label1 = QLabel("<h3>1. Default Behavior</h3><code>setAutoSize(False)</code><br>Widget expands to fill available space.")
        label1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        view1 = QMView(markdown_content)
        view1.setStyleSheet("border: 2px solid #ccc;")
        # setAutoSize is False by default
        grid_layout.addWidget(label1, 0, 0)
        grid_layout.addWidget(view1, 1, 0)

        # --- 2. Basic Auto-Sizing ---
        label2 = QLabel("<h3>2. Basic Auto-Sizing</h3><code>setAutoSize(True)</code><br>Widget shrinks to fit content's natural size.")
        label2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        view2 = QMView(markdown_content)
        view2.setStyleSheet("border: 2px solid #3498db;")
        view2.setAutoSize(True)
        grid_layout.addWidget(label2, 0, 1)
        grid_layout.addWidget(view2, 1, 1)

        # --- 3. Width-Constrained Sizing ---
        label3 = QLabel("<h3>3. Width-Constrained</h3><code>setAutoSize(True, max_width=250)</code><br>Content wraps at 250px; height adjusts.")
        label3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        view3 = QMView(markdown_content)
        view3.setStyleSheet("border: 2px solid #2ecc71;")
        view3.setAutoSize(True, max_width=250)
        grid_layout.addWidget(label3, 2, 0)
        grid_layout.addWidget(view3, 3, 0)

        # --- 4. Height-Constrained Sizing ---
        label4 = QLabel("<h3>4. Height-Constrained</h3><code>setAutoSize(True, max_height=80)</code><br>Content is clipped at 100px; width adjusts.")
        label4.setAlignment(Qt.AlignmentFlag.AlignCenter)
        view4 = QMView(markdown_content)
        view4.setStyleSheet("border: 2px solid #e74c3c;")
        view4.setAutoSize(True, max_height=80)
        grid_layout.addWidget(label4, 2, 1)
        grid_layout.addWidget(view4, 3, 1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = SizingComparisonDemo()
    demo.show()
    sys.exit(app.exec()) 