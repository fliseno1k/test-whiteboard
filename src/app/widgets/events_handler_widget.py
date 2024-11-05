from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

if TYPE_CHECKING:
    from core.editor import Editor


class EventsHandlerWidget(QWidget):
    def __init__(self, editor: Editor, parent=None):
        super().__init__(parent)

        self.__editor = editor

        self.__set_attributes()

    def resizeEvent(self, event):
        parent = self.parentWidget()

        if parent is None:
            return

        self.setGeometry(parent.rect())

    def mouseDoubleClickEvent(self, event):
        active_handler = self.__editor.active_handler

        if active_handler:
            active_handler.on_mouse_double_click_event(self.__editor, event)

    def __set_attributes(self):
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)
        self.setMouseTracking(True)
