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

        self._selected: List[Shape] = []

    def initialize(self, editor: Editor, event: QMouseEvent):
        shape = self._get_shape_at(editor, event)
        if not shape:
            return

        self._selected.append(shape)

        editor.updated()

    def update(self, editor: Editor, event: QMouseEvent):
        pass

    def finalize(self, editor: Editor, event: QMouseEvent):
        pass

    def _get_shape_at(self, editor: Editor, event: QMouseEvent):
        if not editor.current_page():
            return None
        
        return editor.current_page().get_shape_at(event.position())

    def _reset(self):
        self._selected.clear()

        super()._reset()