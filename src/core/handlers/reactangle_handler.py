from __future__ import annotations
from typing import TYPE_CHECKING, Optional

from ..macro import add_shape
from ..transform import ActionKind
from .abstract_handler import AbstractHandler

if TYPE_CHECKING:
    from PySide6.QtGui import QMouseEvent

    from ..editor import Editor
    from ..shapes import Shape


class RectangleHandler(AbstractHandler):
    def __init__(self, id: str):
        super().__init__(id)

        self.__shape: Optional[Shape] = None

    def initialize(self, editor: Editor, event: QMouseEvent):
        if not editor.current_page:
            return

        center = event.position()
        self.__shape = editor.shape_factory.create_rectangle([center.x(), center.y()])

        editor.transform.start_action(ActionKind.INSERT)
        editor.transform.transact(
            lambda tx: add_shape(tx, self.__shape, editor.current_page)
        )

    def finalize(self, editor: Editor, event: QMouseEvent):
        if not self.__shape:
            return

        editor.transform.end_action()

    def on_mouse_double_click_event(self, editor: Editor, event: QMouseEvent):
        self.initialize(editor, event)
        self.finalize(editor, event)
