from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtGui import QColor

from core.shapes import Rectangle, Connector
from utils.rand_color import random_color_factory

if TYPE_CHECKING:
    from core.editor import Editor


class ShapeFactory:

    def __init__(self, editor: Editor):
        self.__random_color = random_color_factory(QColor)

    def create_rectangle(self):
        shape = Rectangle()
        shape.background_color = self.__random_color()

        return shape

    def create_connector(self):
        shape = Connector()

        return shape
