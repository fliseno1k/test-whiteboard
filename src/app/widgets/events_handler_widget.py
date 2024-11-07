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

    def mousePressEvent(self, event):
        self.__editor.on_mouse_press_event(event)

    def mouseDoubleClickEvent(self, event):
        self.__editor.on_mouse_double_click_event(event)

    def mouseMoveEvent(self, event):
        self.__editor.on_mouse_move_event(event)

    def mouseReleaseEvent(self, event):
        self.__editor.on_mouse_release_event(event)

    def resizeEvent(self, event):
        parent = self.parentWidget()

        if parent is None:
            return

        self.setGeometry(parent.rect())

    def __set_attributes(self):
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)
        self.setMouseTracking(True)
