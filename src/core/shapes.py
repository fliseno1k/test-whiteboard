from __future__ import annotations
from typing import Callable, Optional, List

from PySide6.QtGui import QColor, QPainter, QPixmap, QBrush
from PySide6.QtCore import Qt, QPoint

from utils.unique_id import unique_id


class Shape:
    def __init__(self):
        self.__id = unique_id()

        self.left: int = 0
        self.top: int = 0
        self.width: int = 0
        self.height: int = 0

        self.background_color: Optional[QColor] = None

        self.parent: Optional[Shape] = None
        self.children: list[Shape] = []

        self._pixmap: Optional[QPixmap] = None
        self._memo_outline: List[List[int]] = []

    @property
    def id(self):
        self.__id

    @property
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height

    @property
    def outline(self):
        return self._memo_outline

    def traverse(
        self,
        fn: Callable[[Shape], None],
        parent: Optional[Shape] = None,
    ):
        fn(self, parent)

        for child in self.children:
            child.traverse(fn, self)

    def get_shape_at(self, point: QPoint) -> Optional[Shape]:
        for shape in self.children:
            result = shape.get_shape_at(point)

            if result:
                return result

        if self.contains_point(point):
            return self

        return None

    def update(self):
        del self._pixmap
        self._pixmap = QPixmap(self.width, self.height)
        self.render(self._pixmap)

        for child in self.children:
            child.update()

    def render(self, pixmap: QPixmap):
        self.render_outline(pixmap)
        self.render_default(pixmap)

    def render_default(self, pixmap: QPixmap): ...

    def render_outline(self, pixmap: QPixmap):
        self._memo_outline = []

    def draw(self, painter: QPainter):
        if not self._pixmap:
            return

        painter.drawPixmap(QPoint(self.left, self.top), self._pixmap)

        for shape in self.children:
            shape.draw(painter)
    
    def contains_point(self, point: QPoint):
        return False


class Page(Shape):
    def __init__(self):
        super().__init__()

    def update(self):
        for child in self.children:
            child.update()

    def draw(self, painter: QPainter):
        for shape in self.children:
            shape.draw(painter)


class Box(Shape):
    def __init__(self):
        super().__init__()

    def render_default(self, pixmap: QPixmap):
        painter = QPainter(pixmap)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(self.background_color))
        painter.drawRect(0, 0, self.width, self.height)
        painter.end()

    def render_outline(self, pixmap: QPixmap):
        self._memo_outline = [
            [self.left, self.top],
            [self.right, self.top],
            [self.right, self.bottom],
            [self.left, self.bottom],
            [self.left, self.top],
        ]

    def contains_point(self, point: QPoint):
        x = point.x()
        y = point.y()

        return (self.top < y and self.bottom > y) and (self.left < x and self.right > x)


class Rectangle(Box):
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
