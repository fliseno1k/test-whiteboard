from __future__ import annotations
from copy import copy
from typing import TYPE_CHECKING, Optional

from ..macro import add_shape, set_path
from ..shapes import Shape, Connector
from ..transform import ActionKind

from .abstract_handler import AbstractHandler

if TYPE_CHECKING:
    from PySide6.QtGui import QMouseEvent

    from ..editor import Editor
    from ..transaction import Transaction


class ConnectorHandler(AbstractHandler):
    def __init__(self, id: str):
        super().__init__(id)

        self.__tail: Optional[Shape] = None
        self.__head: Optional[Shape] = None
        self.__shape: Optional[Connector] = None

    def initialize(self, editor: Editor, event: QMouseEvent):
        page = editor.current_page()
        position = event.position()

        self.__tail = page.get_shape_at([position.x(), position.y()])
        self.__shape = editor.shape_factory.create_connector(
            self.__tail,
            self.__head,
            [self._drag_start_point, self._drag_point],
        )

        editor.transform.start_action(ActionKind.INSERT)
        editor.transform.transact(lambda tx: add_shape(tx, self.__shape, page))

    def update(self, editor: Editor, event: QMouseEvent):
        page = editor.current_page()
        position = event.position()
        shape = page.get_shape_at([position.x(), position.y()], [self.__shape])

        if not isinstance(shape, Connector):
            self.__head = shape

        editor.transform.transact(lambda tx: self.__transaction_fn(tx))

    def finalize(self, editor: Editor, event: QMouseEvent):
        if not self.__shape:
            return

        if not self.__head or not self.__tail:
            editor.transform.cancel_action()
        else:
            editor.transform.end_action()

        self.__shape = None
        self.__head = None
        self.__tail = None

    def __transaction_fn(self, tx: Transaction):
        new_path = copy(self.__shape.path)
        new_path[1] = self._drag_point

        set_path(tx, self.__shape, new_path)
        tx.assign_ref(self.__shape, "head", self.__head)
