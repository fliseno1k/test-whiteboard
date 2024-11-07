from __future__ import annotations
from typing import TYPE_CHECKING, List

from PySide6.QtCore import QPointF

from .abstract_handler import AbstractHandler

if TYPE_CHECKING:
    from PySide6.QtGui import QMouseEvent

    from ..editor import Editor
    from ..shapes import Shape


class SelectHandler(AbstractHandler):
    def __init__(self, id: str):
        super().__init__(id)

        self._dragging: bool = False
        self._drag_start_point: QPointF = QPointF()

        self._selected: List[Shape] = []

    def initialize(self, editor: Editor, event: QMouseEvent):
        self._dragging = True
        self._drag_start_point = event.position()

    def update(self, editor: Editor, event: QMouseEvent):
        pass

    def finalize(self, editor: Editor, event: QMouseEvent):
        return super().finalize(editor, event)

    def on_mouse_press_event(self, editor: Editor, event: QMouseEvent):
        self.initialize(editor, event)
        editor.updated()

    def on_mouse_move_event(self, editor: Editor, event: QMouseEvent):
        self.update(editor, event)
        editor.updated()

    def on_mouse_release_event(self, editor, event):
        self.finalize(editor, event)
        self._reset()
        editor.updated()

    def get_shape_at(self, event: QMouseEvent): ...

    def _reset(self):
        self._dragging = False
        self._drag_start_point = QPointF()

        self._selected = []
