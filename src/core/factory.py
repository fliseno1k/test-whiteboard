from __future__ import annotations
from copy import copy
from typing import TYPE_CHECKING, Optional, List

from utils.rand_color import random_color

from .geometry import path_bounding_rect, rect_width, rect_height
from .shapes import Connector, Rectangle

if TYPE_CHECKING:
    from .editor import Editor
    from .shapes import Shape


class ShapeFactory:
    def __init__(self, editor: Editor):
        self.__editor = editor

    def create_rectangle(self, center: list[int]):
        shape = Rectangle()

        shape.left = round(center[0]) - 60
        shape.top = round(center[1]) - 30
        shape.width = 120
        shape.height = 60

        shape.background_color = random_color()

        return shape

    def create_connector(
        self,
        tail: Optional[Shape],
        head: Optional[Shape],
        points: List[List[int]],
    ):
        shape = Connector()
        shape.tail = tail
        shape.head = head
        shape.path = copy(points)

        rect = path_bounding_rect(shape.path)
        shape.left = rect[0][0]
        shape.top = rect[0][1]
        shape.width = rect_width(rect)
        shape.height = rect_height(rect)

        return shape
