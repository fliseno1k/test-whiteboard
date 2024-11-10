from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from PySide6.QtGui import QMouseEvent

    from ..editor import Editor


class AbstractHandler(ABC):
    def __init__(self, id: str):
        self._id = id

        self._dragging = False
        self._drag_point: List[int] = [-1, -1]
        self._drag_start_point: List[int] = [-1, -1]

    def id(self):
        return self._id

    def initialize(self, editor: Editor, event: QMouseEvent):
        pass

    def update(self, editor: Editor, event: QMouseEvent):
        pass

    def finalize(self, editor: Editor, event: QMouseEvent):
        pass

    def on_mouse_press_event(self, editor: Editor, event: QMouseEvent):
        position = event.position()

        self._reset()

        self._dragging = True
        self._drag_point = [position.x(), position.y()]
        self._drag_start_point = [position.x(), position.y()]

        self.initialize(editor, event)
        editor.updated()

    def on_mouse_move_event(self, editor: Editor, event: QMouseEvent):
        if not self._dragging:
            return

        position = event.position()

        self._drag_point = [position.x(), position.y()]

        self.update(editor, event)
        editor.updated()

    def on_mouse_release_event(self, editor: Editor, event: QMouseEvent):
        if not self._dragging:
            return

        self.finalize(editor, event)
        self._reset()
        editor.updated()

    def on_mouse_double_click_event(self, editor: Editor, event: QMouseEvent):
        pass

    def _reset(self):
        self._dragging = False
        self._drag_point = [-1, -1]
        self._drag_start_point = [-1, -1]
