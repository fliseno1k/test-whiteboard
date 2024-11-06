from __future__ import annotations
from typing import Callable, Optional

from PySide6.QtGui import QColor, QPainter, QPixmap, QBrush
from PySide6.QtCore import Qt, QPoint

from utils.unique_id import generate_id


class Shape:
    def __init__(self):
        self.id = generate_id()

        self.left: int = 0
        self.top: int = 0
        self.width: int = 0
        self.height: int = 0

        self.background_color: Optional[QColor] = None

        self.parent: Optional[Shape] = None
        self.children: list[Shape] = []

        self.pixmap: Optional[QPixmap] = None

    def traverse(
        self,
        fn: Callable[[Shape], None],
        parent: Optional[Shape] = None,
    ):
        fn(self, parent)

        for child in self.children:
            child.traverse(fn, self)

    @property
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height

    def update(self):
        del self.pixmap
        self.pixmap = QPixmap(self.width, self.height)
        self.render(self.pixmap)

        for child in self.children:
            child.update()

    def render(self, pixmap: QPixmap):
        painter = QPainter(pixmap)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(self.background_color))
        painter.drawRect(0, 0, self.width, self.height)
        painter.end()

    def draw(self, painter: QPainter):
        if not self.pixmap:
            return

        painter.drawPixmap(QPoint(self.left, self.top), self.pixmap)

        for shape in self.children:
            shape.draw(painter)


class Page(Shape):
    def __init__(self):
        super().__init__()

    def update(self):
        for child in self.children:
            child.update()

    def draw(self, painter: QPainter):
        for shape in self.children:
            shape.draw(painter)


class Rectangle(Shape):
    def __init__(self):
        super().__init__()


class Connector(Shape):
    def __init__(self):
        super().__init__()

        self.head: Optional[Shape] = None
        self.head_anchor: list[int] = []
        self.head_margin: int = 0

        self.tail: Optional[Shape] = None
        self.tail_anchor: list[int] = []
        self.tail_margin: int = 0
