from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from PySide6.QtGui import QMouseEvent

    from ..editor import Editor
    from ..manipulators.abstract_manipulator import AbstractManipulator
    from ..shapes import Shape


class AbstractController(ABC):

    def __init__(self, manipulator: AbstractManipulator):
        self._manipulator = manipulator
        self._reset()

    def is_dragging(self):
        return self._dragging

    def active(self, editor: Editor, shape: Shape):
        return False

    def mouse_in(self, editor: Editor, shape: Shape, event: QMouseEvent):
        return shape.contains_point(event.position())

    def initialize(self, editor: Editor, shape: Shape, event: QMouseEvent):
        pass

    def update(self, editor: Editor, shape: Shape, event: QMouseEvent):
        pass

    def finalize(self, editor: Editor, shape: Shape, event: QMouseEvent):
        pass

    def draw(self, editor: Editor, shape: Shape, event: QMouseEvent):
        pass

    def on_mouse_press_event(self, editor: Editor, shape: Shape, event: QMouseEvent):
        if not self.mouse_in(editor, shape, event):
            return False

        self._reset()

        self._dragging = True
        self._drag_start_point = event.position()
        self._drag_prev_point = event.position()
        self._drag_point = event.position()

        self.initialize(editor, shape, event)        
        self.update(editor, shape, event)

        editor.updated()

        return True

    def on_mouse_move_event(self, editor: Editor, shape: Shape, event: QMouseEvent):
        if not self._dragging:
            return False

        self._drag_prev_point = self._drag_point
        self._drag_point = event.position()

        self.update(editor, shape, event)

        editor.updated()

        return True

    def on_mouse_release_event(self, editor: Editor, shape: Shape, event: QMouseEvent):
        if not self._dragging:
            return False

        self.finalize(editor, shape, event)
        self._reset()

        editor.updated()

    def _reset(self):
        self._dragging = False
        self._drag_start_point: List[int] = [-1, -1]
        self._drag_prev_point: List[int] = [-1, -1]
        self._drag_point: List[int] = [-1, -1]
