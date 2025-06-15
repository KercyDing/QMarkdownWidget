import sys
from qtpy.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QTextEdit, QPushButton, QHBoxLayout, QLabel, QSplitter, QScrollArea
from qtpy.QtCore import Qt
from QMarkdownWidget import QMView

class StyleTester(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QMView 样式测试工具")
        self.resize(1200, 800)

        # --- 读取 Markdown 内容 ---
        try:
            with open('examples/qss_test.md', 'r', encoding='utf-8') as f:
                self.markdown_content = f.read()
        except FileNotFoundError:
            self.markdown_content = "# 错误\n\n`qss_test.md` 文件未找到。"

        # --- 主控件 ---
        self.central_widget = QWidget()
        self.main_layout = QHBoxLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # --- QSS 和 CSS 编辑器 ---
        editor_layout = QVBoxLayout()
        
        self.qss_editor = QTextEdit()
        self.qss_editor.setPlaceholderText("在这里输入QMView的QSS样式...")
        
        self.css_editor = QTextEdit()
        self.css_editor.setPlaceholderText("在这里输入HTML内容的CSS样式...")
        
        apply_button = QPushButton("应用样式")
        apply_button.clicked.connect(self.apply_styles)

        editor_layout.addWidget(QLabel("QMView QSS (控件样式)"))
        editor_layout.addWidget(self.qss_editor)
        editor_layout.addWidget(QLabel("HTML CSS (内容样式)"))
        editor_layout.addWidget(self.css_editor)
        editor_layout.addWidget(apply_button)

        # --- QMView 预览 ---
        self.view = QMView()
        self.view.setMarkdown(self.markdown_content)
        # 根据用户要求，启用自动尺寸调整
        self.view.setAutoSize(True)

        # --- 创建一个 QScrollArea 来容纳 QMView ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.view)
        # 设置滚动区域的样式，使其本身不可见，以便显示 QMView 的边框和背景
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")

        # --- 使用 QSplitter 分割编辑器和预览 ---
        splitter = QSplitter(Qt.Horizontal)
        editor_container = QWidget()
        editor_container.setLayout(editor_layout)
        
        splitter.addWidget(editor_container)
        splitter.addWidget(scroll_area) # 将 scroll_area 添加到 splitter
        splitter.setSizes([400, 800]) # 初始大小

        self.main_layout.addWidget(splitter)

        # --- 加载初始样式 ---
        self.load_initial_styles()
        self.apply_styles()

    def load_initial_styles(self):
        # 初始 QSS 样式 (针对 QMView 控件本身)
        initial_qss = """
QMView {
    /* 边框: 2像素宽的蓝色实线边框，圆角8像素 */
    border: 2px solid #0078d7;
    border-radius: 8px;

    /* 背景色 */
    background-color: #ffffff; 
    
    /* 内边距 */
    padding: 10px;
}
"""
        self.qss_editor.setText(initial_qss)

        # 初始 CSS 样式 (针对 QMView 内部的 HTML 内容)
        initial_css = """
/* 全局文本样式 */
body {
    color: #333;
    font-family: 'Microsoft YaHei', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background-color: #f0f0f0; /* 与QSS背景色保持一致 */
}

/* 标题样式 */
h1 { color: #005a9e; }
h2 { color: #0078d7; }
h3 { color: #2b88d8; }

/* 链接样式 */
a {
    color: #0066cc;
    text-decoration: none; /* 去掉下划线 */
}
a:hover {
    text-decoration: underline; /* 鼠标悬停时显示下划线 */
}

/* 代码块样式 */
pre {
    background-color: #2d2d2d; /* 深色背景 */
    color: #6180e0; /* 亮色文字 */
    border-radius: 5px;
    padding: 1em;
    overflow-x: auto;
}
code {
    font-family: "Consolas", "Monaco", monospace;
}

/* 引用块样式 */
blockquote {
    border-left: 4px solid #ccc;
    padding-left: 1em;
    color: #666;
    margin-left: 0;
}

/* 表格样式 */
table {
    border-collapse: collapse;
    width: 100%;
}
th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
}
th {
    background-color: #e9ecef;
}
"""
        self.css_editor.setText(initial_css)

    def apply_styles(self):
        qss = self.qss_editor.toPlainText()
        css = self.css_editor.toPlainText()

        # 1. 应用 QSS 到 QMView 控件
        self.view.setStyleSheet(qss)

        # 2. 应用 CSS 到 HTML 内容
        self.view.setHtmlStyle(css)
        
        # 重新加载 Markdown 以确保 CSS 生效
        self.view.setMarkdown(self.markdown_content)

def main():
    app = QApplication(sys.argv)
    
    # 启用高清屏支持 (兼容不同Qt版本)
    if hasattr(Qt.ApplicationAttribute, 'AA_EnableHighDpiScaling'):
        app.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling)
    if hasattr(Qt.ApplicationAttribute, 'AA_UseHighDpiPixmaps'):
        app.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps)

    tester = StyleTester()
    tester.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 