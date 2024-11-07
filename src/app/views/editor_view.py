from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QWidget, QVBoxLayout

from ..widgets.canvas_widget import CanvasWidget
from ..widgets.events_handler_widget import EventsHandlerWidget
from ..widgets.toolbar_widget import ToolBarWidget

if TYPE_CHECKING:
    from core.editor import Editor


class EditorView(QWidget):
    def __init__(self, editor: Editor):
        super().__init__()

        self.__editor = editor

        self.__init_UI()

    def __init_UI(self):
        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        toolbar = ToolBarWidget(self.__editor, self)
        layout.addWidget(toolbar)

        canvas = CanvasWidget(self.__editor, self)
        layout.addWidget(canvas)

        events_handler_widget = EventsHandlerWidget(self.__editor, canvas)
        events_handler_widget.show()

        self.setLayout(layout)
