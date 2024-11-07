from __future__ import annotations
from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from .editor import Editor
    from .shapes import Shape


class Selection():

    def __init__(self, editor: Editor):
        self._editor = editor
        self._shapes: List[Shape] = []

    def get_shapes(self):
        return self._shapes

    def size(self):
        return len(self._shapes)

    def is_selected(self, shape: Shape):
        return shape in self._shapes

    def select(self, shapes: List[Shape], clear = False):
        if clear:
            self._shapes.clear()

        for shape in shapes:
            if shape not in self._shapes:
                self._shapes.append(shape)

    def deselect(self, shapes: List[Shape]):
        for shape in shapes:
            if shape in self._shapes:
                self._shapes.remove(shape)