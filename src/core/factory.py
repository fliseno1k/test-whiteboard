from __future__ import annotations
from typing import TYPE_CHECKING

from core.shapes import Rectangle, Connector

if TYPE_CHECKING:
    from core.editor import Editor


class ShapeFactory:

    def __init__(self, editor: Editor):
        self

    def create_rectangle(self):
        shape = Rectangle()

        return shape

    def create_connector(self):
        shape = Connector()

        return shape
