from __future__ import annotations
from typing import TYPE_CHECKING, Dict

from PySide6.QtWidgets import QToolBar
from PySide6.QtGui import QAction

from core.events import EventKind

if TYPE_CHECKING:
    from core.editor import Editor


class ToolBarWidget(QToolBar):
    def __init__(self, editor: Editor, parent=None):
        super().__init__(parent)

        self.__editor = editor
        self.__actions: Dict[str, QAction] = {}

        self.__init_actions()
        self.__update_actions()
        self.__set_stylesheet()

        self.__editor.add_listener(
            EventKind.ACTIVE_HANDLER_CHANGED, self.__update_actions
        )

    def __init_actions(self):
        for id, _ in self.__editor.handlers():
            action = QAction(id, self)
            action.setCheckable(True)
            action.triggered.connect(lambda _, id=id: self.__select_handler(id))

            self.__actions.update({id: action})
            self.addAction(action)

    def __select_handler(self, handler_id: str):
        self.__editor.activate_handler(handler_id)

    def __update_actions(self):
        for id, action in self.__actions.items():
            action.setChecked(self.__editor.active_handler().id() == id)

    def __set_stylesheet(self):
        self.setStyleSheet(
            """
            QToolBar {
                spacing: 4px;
                padding: 12px;
                margin: 0px;
            }

            QToolButton:checked {
                background-color: #5e9ed6;
                color: white;
            }
            QToolButton {
                padding: 4px 8px;
                border-radius: 4px;
                background-color: transparent;
                color: white;

            }
        """
        )
