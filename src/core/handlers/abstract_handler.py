from __future__ import annotations
from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PySide6.QtGui import QMouseEvent

    from ..editor import Editor


class AbstractHandler(ABC):
    def __init__(self, id: str):
        self._id = id

    @property
    def id(self):
        return self._id

    def activate(self, editor: Editor):
        self._on_activate(editor)

    def deactivate(self, editor: Editor):
        self._on_deactivate(editor)

    def initialize(self, editor: Editor, event: QMouseEvent):
        pass

    def update(self, editor: Editor, event: QMouseEvent):
        pass

    def finalize(self, editor: Editor, event: QMouseEvent):
        pass

    def on_mouse_press_event(self, editor: Editor, event: QMouseEvent):
        pass

    def on_mouse_move_event(self, editor: Editor, event: QMouseEvent):
        pass

    def on_mouse_release_event(self, editor: Editor, event: QMouseEvent):
        pass

    def on_mouse_double_click_event(self, editor: Editor, event: QMouseEvent):
        pass

    def _on_activate(self, editor: Editor):
        pass

    def _on_deactivate(self, editor: Editor):
        pass

    def _reset(self):
        pass
