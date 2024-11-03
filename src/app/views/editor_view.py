from PySide6.QtWidgets import QWidget, QVBoxLayout

from app.widgets.canvas_widget import CanvasWidget
from app.widgets.events_handler_widget import EventsHandlerWidget
from app.widgets.toolbar_widget import ToolBarWidget

from core.editor import Editor
from core.options import OptionsBuilder


class EditorView(QWidget):
    def __init__(self):
        super().__init__()

        self.__init_editor()
        self.__init_UI()

    def __init_editor(self):
        options_builder = OptionsBuilder()
        self.__editor = Editor(options_builder.build())

    def __init_UI(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        toolbar = ToolBarWidget(self.__editor, self)
        layout.addWidget(toolbar)

        canvas = CanvasWidget(self)
        layout.addWidget(canvas)

        events_handler_widget = EventsHandlerWidget(self.__editor, canvas)
        events_handler_widget.show()

        self.setLayout(layout)
