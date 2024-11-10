from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt

from core.events import EventKind

if TYPE_CHECKING:
    from core.editor import Editor


class CanvasWidget(QWidget):

    def __init__(self, editor: Editor, parent=None):
        super().__init__(parent)

        self.__editor = editor
        self.__editor.add_listener(EventKind.UPDATED, self.update)

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.scale(1, 1)
        painter.translate(0, 0)
        painter.fillRect(self.rect(), Qt.white)

        self.__draw_grid(painter)
        self.__editor.draw(painter)

        painter.end()

    def resizeEvent(self, event):
        size = self.size()

        self.__editor.resize([size.width(), size.height()])

    def __draw_grid(self, painter: QPainter):
        rect = self.rect()
        left = rect.left()
        top = rect.top()
        right = rect.right()
        bottom = rect.bottom()
        grid_size = 20

        painter.setPen(QPen(QColor(200, 200, 200), 1))

        x = left
        while x <= right:
            painter.drawLine(x, top, x, bottom)
            x += grid_size

        y = top
        while y <= bottom:
            painter.drawLine(left, y, right, y)
            y += grid_size
