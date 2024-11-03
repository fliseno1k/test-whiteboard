from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from PySide6.QtGui import QMouseEvent, QKeyEvent

if TYPE_CHECKING:
    from core.editor import Editor


class AbstractHandler(ABC):
    def __init__(self, id: int, name: str):
        self._id = id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @abstractmethod
    def activate(self, editor: Editor):
        self._on_activate(editor)

    @abstractmethod
    def deactivate(self, editor: Editor):
        self._on_deactivate(editor)

    @abstractmethod
    def on_event(self, editor: Editor, event: QMouseEvent | QKeyEvent): ...

    @abstractmethod
    def _on_activate(self, editor: Editor): ...

    @abstractmethod
    def _on_deactivate(self, editor: Editor): ...
