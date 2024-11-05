from __future__ import annotations
from typing import TYPE_CHECKING

from core.handlers.abstract_handler import AbstractHandler

if TYPE_CHECKING:
    from PySide6.QtGui import QMouseEvent

    from core.editor import Editor


class ConnectorHandler(AbstractHandler):
    def __init__(self, id: str):
        super().__init__(id)

    def initialize(self, editor: Editor, event: QMouseEvent):
        return super().initialize(editor, event)

    def update(self, editor: Editor, event: QMouseEvent):
        return super().update(editor, event)

    def finalize(self, editor: Editor, event: QMouseEvent):
        return super().finalize(editor, event)
