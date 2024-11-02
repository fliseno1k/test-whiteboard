from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt


class CanvasWidget(QWidget):

    grid_size: int = 20

    def __init__(self, parent=None):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.scale(1, 1)
        painter.translate(0, 0)
        painter.fillRect(self.rect(), Qt.white)

        self.draw_grid(painter)

        painter.end()

    def draw_grid(self, painter: QPainter):
        rect = self.rect()
        left = rect.left()
        top = rect.top()
        right = rect.right()
        bottom = rect.bottom()

        painter.setPen(QPen(QColor(200, 200, 200), 1))

        x = left
        while x <= right:
            painter.drawLine(x, top, x, bottom)
            x += self.grid_size

        y = top
        while y <= bottom:
            painter.drawLine(left, y, right, y)
            y += self.grid_size
