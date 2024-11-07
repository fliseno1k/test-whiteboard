from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from PySide6.QtGui import QMouseEvent

    from ..editor import Editor
    from ..manipulators.abstract_manipulator import AbstractManipulator
    from ..shapes import Shape

    from .abstract_controller import AbstractController


class BoxMoveController(AbstractController):

    def __init__(self, manipulator: AbstractManipulator):
        super().__init__(manipulator)

    def active(self, editor: Editor, shape: Shape):
        return editor.selection.size() == 1 and editor.selection.is_selected(shape)

    def initialize(self, editor: Editor, shape: Shape, event: QMouseEvent):
        pass

    def update(self, editor: Editor, shape: Shape, event: QMouseEvent):
        pass

    def finalize(self, editor: Editor, shape: Shape, event: QMouseEvent):
        pass

    def draw(self, editor: Editor, shape: Shape, event: QMouseEvent):
        pass
