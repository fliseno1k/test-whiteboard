from __future__ import annotations
from typing import TYPE_CHECKING

from ..macro import move_shapes
from ..transform import ActionKind

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
        return editor.selection.size() == 1 and editor.selection.is_selected(
            ActionKind.MOVE
        )

    def initialize(self, editor: Editor, shape: Shape, event: QMouseEvent):
        editor.transform.start_action()

    def update(self, editor: Editor, shape: Shape, event: QMouseEvent):
        page = editor.current_page()

        editor.transform.transact(lambda tx: move_shapes(tx, page, [shape], 0, 0))

    def finalize(self, editor: Editor, shape: Shape, event: QMouseEvent):
        editor.transform.end_action()

    def draw(self, editor: Editor, shape: Shape, event: QMouseEvent):
        pass
