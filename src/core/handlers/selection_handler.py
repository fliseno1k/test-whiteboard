from __future__ import annotations
from typing import TYPE_CHECKING, List

from PySide6.QtCore import QPointF

from .abstract_handler import AbstractHandler

if TYPE_CHECKING:
    from PySide6.QtGui import QMouseEvent

    from ..editor import Editor
    from ..shapes import Shape


class SelectionHandler(AbstractHandler):

    def __init__(self, id: str):
        super().__init__(id)

        self._deselect_on_up: List[Shape] = []

    def on_mouse_press_event(self, editor: Editor, event: QMouseEvent):
        pass

    def on_mouse_move_event(self, editor: Editor, event: QMouseEvent):
        pass

    def on_mouse_release_event(self, editor: Editor, event: QMouseEvent):
        pass

    def _get_shape_at(self, editor: Editor, event: QMouseEvent):
        if not editor.current_page():
            return None
        
        return editor.current_page().get_shape_at(event.position())

    def _reset(self):
        self._selected.clear()

        super()._reset()