from PySide6.QtWidgets import QMainWindow
from app.views.editor_view import EditorView

from core.editor import Editor
from core.options import OptionsBuilder
from core.handlers.reactangle_handler import RectangleHandler
from core.handlers.connector_handler import ConnectorHandler
from core.handlers.select_handler import SelectHandler


def setup_editor() -> Editor:
    options = OptionsBuilder()
    options.set_handlers(
        [
            SelectHandler("select-handler"),
            RectangleHandler("rectangle-handler"),
            ConnectorHandler("connector-handler"),
        ]
    )
    options.set_default_handler_id("rectangle-handler")

    return Editor(options.build())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.editor_view = EditorView(setup_editor())
        self.setCentralWidget(self.editor_view)

        self.__update_meta()

    def __update_meta(self):
        self.setWindowTitle("Whiteboard")
