from __future__ import annotations
from typing import TYPE_CHECKING, Callable, Optional

from utils.unique_id import generate_id

if TYPE_CHECKING:
    from PySide6.QtGui import QColor


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
        pass

    def render(self):
        pass

    def draw(self):
        for shape in self.children:
            shape.draw()

    def get_bounding_rect(self):
        return [self.left, self.top, self.right, self.bottom]


class Page(Shape):
    def __init__(self):
        super().__init__()


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
