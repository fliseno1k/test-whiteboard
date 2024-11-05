from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from core.handlers.abstract_handler import AbstractHandler
from core.macro import add_shape

if TYPE_CHECKING:
    from PySide6.QtGui import QMouseEvent

    from core.editor import Editor
    from core.shapes import Shape
    from core.transform import ActionKind


class RectangleHandler(AbstractHandler):
    def __init__(self, id: str):
        super().__init__(id)

        self.__shape: Optional[Shape] = None

    def initialize(self, editor: Editor, event: QMouseEvent):
        center = event.position()

        self.__shape = editor.factory.create_rectangle([center.x(), center.y()])

        editor.transform.start_action(ActionKind.INSERT)
        editor.transform.transact(
            lambda transaction: add_shape(
                transaction, self.__shape, self.__shape.parent
            )
        )

    def finalize(self, editor: Editor, event: QMouseEvent):
        editor.transform.end_action()

    def on_mouse_double_click_event(self, editor: Editor, event: QMouseEvent):
        print("dblclick")
        # self.initialize(editor, event)
        # self.finalize(editor, event)
