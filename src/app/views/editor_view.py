from PySide6.QtWidgets import QWidget, QVBoxLayout
from app.widgets.canvas_widget import CanvasWidget


class EditorView(QWidget):

    layout: QVBoxLayout

    canvas: CanvasWidget

    def __init__(self):
        super().__init__()

        self.canvas = CanvasWidget()
        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.canvas)

        self.setLayout(self.layout)
