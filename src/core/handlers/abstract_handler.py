from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from PySide6.QtGui import QMouseEvent, QKeyEvent

if TYPE_CHECKING:
    from core.editor import Editor


class AbstractHandler(ABC):
    def __init__(self, id: str):
        self._id = id

    @property
    def id(self):
        return self._id

    @abstractmethod
    def activate(self, editor: Editor):
        self._on_activate(editor)

    @abstractmethod
    def deactivate(self, editor: Editor):
        self._on_deactivate(editor)

    @abstractmethod
    def initialize(self, editor: Editor, event: QMouseEvent): ...

    @abstractmethod
    def update(self, editor: Editor, event: QMouseEvent): ...

    @abstractmethod
    def finalize(self, editor: Editor, event: QMouseEvent): ...

    @abstractmethod
    def on_event(self, editor: Editor, event: QMouseEvent | QKeyEvent): ...

    @abstractmethod
    def _on_activate(self, editor: Editor): ...

    @abstractmethod
    def _on_deactivate(self, editor: Editor): ...
