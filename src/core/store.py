from __future__ import annotations
from typing import Optional, Dict

from .shapes import Page, Shape


class Store:
    def __init__(self):
        self.__idIndex: Dict[str, Shape] = {}
        self.__root: Optional[Page] = Page()

    def root(self):
        return self.__root

    def get_by_id(self, id: str):
        return self.__idIndex.get(id)

    def add_to_index(self, shape: Shape):
        def helper(shape: Shape):
            self.__idIndex[shape.id] = shape
            shape.update()

        shape.traverse(helper)

    def remove_from_index(self, shape: Shape):
        def helper(shape: Shape):
            del self.__idIndex[shape.id]
            shape.update()

        shape.traverse(helper)

    def update(self, shape: Shape):
        shape.update()
