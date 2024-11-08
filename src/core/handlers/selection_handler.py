from __future__ import annotations
from typing import TYPE_CHECKING, List

from ..manipulators.manipulator_manager import manipulator_manager

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
        shape = self._get_shape_at(editor, event)
        page = editor.current_page()

        if shape:
            if not editor.selection.is_selected(shape):
                editor.selection.select([shape])
        else:
            editor.selection.deselect_all()

        if page and editor.selection.size() == 1:
            shape = editor.selection.get_shapes()[0]
            manipulator = manipulator_manager.get(shape.type())

            if manipulator:
                manipulator.on_mouse_press_event(editor, page, event)

    def on_mouse_move_event(self, editor: Editor, event: QMouseEvent):
        page = editor.current_page()
        if page and editor.selection.size() == 1:
            shape = editor.selection.get_shapes()[0]

            manipulator = manipulator_manager.get(shape.type())
            if manipulator and manipulator.on_mouse_move_event(editor, shape, event):
                self._deselect_on_up.clear()

    def on_mouse_release_event(self, editor: Editor, event: QMouseEvent):
        editor.selection.deselect(self._deselect_on_up)
        self._deselect_on_up.clear()

        if editor.selection.size() == 1:
            shape = editor.selection.get_shapes()[0]

            manipulator = manipulator_manager.get(shape.type())
            if manipulator:
                manipulator.on_mouse_release_event(editor, shape, event)

    def _get_shape_at(self, editor: Editor, event: QMouseEvent):
        if not editor.current_page():
            return None

        return editor.current_page().get_shape_at(event.position())

    def _reset(self):
        self._deselect_on_up.clear()

        super()._reset()
