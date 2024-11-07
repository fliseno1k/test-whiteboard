from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from PySide6.QtGui import QMouseEvent

    from ..controllers.abstract_controller import AbstractController
    from ..editor import Editor
    from ..shapes import Shape


class AbstractManipulator(ABC):

    def __init__(self):
        self._controllers: List[AbstractController] = []
        self._dragging_controller: Optional[AbstractController] = []

    def is_dragging(self):
        return next((True for ctrl in self._controllers if ctrl.is_dragging()), False)

    def mouse_in(self, editor: Editor, shape: Shape, event: QMouseEvent):
        return next((True for ctrl in self._controllers if ctrl.mouse_in(editor, shape, event)), False)

    def on_mouse_press_event(self, editor: Editor, shape: Shape, event: QMouseEvent):
        handled = False

        for ctrl in self._controllers:
            if ctrl.active(editor, shape) and ctrl.mouse_in(editor, shape, event) and ctrl.on_mouse_press_event(editor, shape, event):
                handled = True
                self._dragging_controller = ctrl
                break

        return handled

    def on_mouse_move_event(self, editor: Editor, shape: Shape, event: QMouseEvent):
        if not self._dragging_controller:
            return False

        return self._dragging_controller.on_mouse_move_event(editor, shape, event)


    def on_mouse_release_event(self, editor: Editor, shape: Shape, event: QMouseEvent):
        if not self._dragging_controller:
            return False
        
        self._dragging_controller.on_mouse_release_event(editor, shape, event)
        self._dragging_controller = None

        return True

    def draw(self, editor: Editor, shape: Shape):
        if self._dragging_controller:
            return
        
        for ctrl in self._controllers:
            ctrl.active(editor, shape) and ctrl.draw(editor, shape)
