from __future__ import annotations
from copy import copy
from enum import Enum
from typing import Callable, Optional, List

from PySide6.QtGui import QColor, QPainter, QPixmap, QBrush, QPen
from PySide6.QtCore import Qt, QPoint

from utils.unique_id import unique_id

from .geometry import get_nearest_segment, path_bounding_rect


class ShapeKind(Enum):
    BOX = "box"
    CONNECTOR = "connector"
    LINE = "line"
    PAGE = "page"
    PATH = "path"
    RECTANGLE = "rectangle"


class Shape:

    def __init__(self, type: ShapeKind):
        self._id = unique_id()
        self._type = type

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
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height

    @property
    def outline(self):
        return copy(self._memo_outline)

    def id(self):
        return self._id

    def type(self):
        return self._type

    def traverse(
        self,
        fn: Callable[[Shape], None],
        parent: Optional[Shape] = None,
    ):
        fn(self, parent)

        for child in self.children:
            child.traverse(fn, self)

    def get_shape_at(
        self, point: List[int], exceptions: List[Shape] = []
    ) -> Optional[Shape]:
        for shape in self.children:
            result = shape.get_shape_at(point)

            if result and result not in exceptions:
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

    def contains_point(self, point: List[int]):
        return False


class Page(Shape):

    def __init__(self, type: ShapeKind = ShapeKind.PAGE):
        super().__init__(type)

    def update(self):
        for child in self.children:
            child.update()

    def draw(self, painter: QPainter):
        for shape in self.children:
            shape.draw(painter)


class Box(Shape):

    def __init__(self, type: ShapeKind = ShapeKind.BOX):
        super().__init__(type)

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

    def contains_point(self, point: List[int]):
        x, y = point[0], point[1]

        return (self.top < y and self.bottom > y) and (self.left < x and self.right > x)


class Path(Shape):

    def __init__(self, type: Shape = ShapeKind.PATH):
        super().__init__(type)

        self.path: List[List[int]] = []

    def contains_point(self, point: List[int]):
        return get_nearest_segment(point, self.outline, 10) > -1

    def render_outline(self, pixmap):
        self._memo_outline = copy(self.path)


class Line(Path):

    def __init__(self, type=ShapeKind.LINE):
        super().__init__(type)

    def render_default(self, pixmap: QPixmap):
        if len(self.path) < 2:
            return

        rect = path_bounding_rect(self.path)

        pixmap.fill(Qt.GlobalColor.transparent)

        pen = QPen()
        pen.setWidth(2)
        pen.setColor(Qt.GlobalColor.black)
        pen.setStyle(Qt.PenStyle.SolidLine)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(pen)
        painter.setBackground(Qt.BrushStyle.NoBrush)

        painter.drawLine(
            self.path[0][0] - rect[0][0],
            self.path[0][1] - rect[0][1],
            self.path[1][0] - rect[0][0],
            self.path[1][1] - rect[0][1],
        )
        painter.end()


class Rectangle(Box):

    def __init__(self, type: ShapeKind = ShapeKind.RECTANGLE):
        super().__init__(type)

        self.path: List[List[int]] = []


class Connector(Line):
    def __init__(self, type: ShapeKind = ShapeKind.CONNECTOR):
        super().__init__(type)

        self.head: Optional[Shape] = None
        self.tail: Optional[Shape] = None
