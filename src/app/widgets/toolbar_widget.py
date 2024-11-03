from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QAction

if TYPE_CHECKING:
    from core.editor import Editor


class ToolBarWidget(QToolBar):
    def __init__(self, editor: Editor, parent=None):
        super().__init__(parent)

        self.__editor = editor

        action1 = QAction("Action 1", self)
        self.addAction(action1)

        action2 = QAction("Action 2", self)
        self.addAction(action2)
