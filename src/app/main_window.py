from PySide6.QtWidgets import QMainWindow
from app.views.editor_view import EditorView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.editor_view = EditorView()

        self.setCentralWidget(self.editor_view)
        self.__update_meta()

    def __update_meta(self):
        self.setWindowTitle("Whiteboard")
