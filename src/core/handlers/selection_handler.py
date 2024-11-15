from __future__ import annotations
from typing import TYPE_CHECKING, List

from .abstract_handler import AbstractHandler

if TYPE_CHECKING:
    from PySide6.QtGui import QMouseEvent

    from ..editor import Editor


class SelectionHandler(AbstractHandler):

    def __init__(self, id: str):
        super().__init__(id)

    def on_mouse_press_event(self, editor: Editor, event: QMouseEvent):
        position = event.position()
        shape = self._get_shape_at(editor, [position.x(), position.y()])

        if shape:
            if not editor.selection.is_selected(shape):
                editor.selection.select([shape], True)
        else:
            editor.selection.deselect_all()

        if editor.selection.size() == 1:
            shape = editor.selection.get_shapes()[0]
            manipulator = editor.manipulator_manager.get(shape.type())

            if manipulator:
                manipulator.on_mouse_press_event(editor, shape, event)

    def on_mouse_move_event(self, editor: Editor, event: QMouseEvent):
        if editor.selection.size() == 1:
            shape = editor.selection.get_shapes()[0]

            manipulator = editor.manipulator_manager.get(shape.type())
            if manipulator:
                manipulator.on_mouse_move_event(editor, shape, event)

    def on_mouse_release_event(self, editor: Editor, event: QMouseEvent):
        if editor.selection.size() == 1:
            shape = editor.selection.get_shapes()[0]

            manipulator = editor.manipulator_manager.get(shape.type())
            if manipulator:
                manipulator.on_mouse_release_event(editor, shape, event)

    def _get_shape_at(self, editor: Editor, point: List[int]):
        return editor.current_page().get_shape_at(point)

    def _reset(self):
        self._deselect_on_up.clear()

        super()._reset()
