from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING, Callable, List, Optional, cast

from utils.event_emmiter import EventEmitter

from .transaction import Transaction

if TYPE_CHECKING:
    from .store import Store


class ActionKind(Enum):
    UNKNOWN = "uknown"
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
    MOVE = "move"


class Action:
    def __init__(self, name: str):
        self.__name = name
        self.__transactions: List[Transaction] = []

    def name(self):
        return self.__name

    def size(self):
        return len(self.__transactions)

    def push(self, tx: Transaction):
        self.__transactions.append(tx)

    def apply(self):
        for tx in self.__transactions:
            tx.apply()

    def unapply(self):
        None


class Transform:
    def __init__(self, store: Store):
        self.__store = store
        self.__action: Optional[Action] = None

        self.on_action = EventEmitter()
        self.on_transaction = EventEmitter()

    def transact(self, fn: Callable[[Transaction], None]):
        transaction = Transaction(self.__store)
        fn(transaction)

        if transaction.size() == 0:
            return

        self.on_transaction.emit()

        if self.__action:
            self.__action.push(transaction)
        else:
            self.startAction(ActionKind.UNKNOWN)
            cast(Action, self.__action).push(transaction)
            self.endAction()

    def start_action(self, name: str):
        if self.__action is not None and self.__action.size() > 0:
            self.endAction()

        self.__action = Action(name)

    def end_action(self):
        if not self.__action:
            return

        if self.__action.size():
            self.on_action.emit()

        self.__action = None

    def cancel_action(self):
        if not self.__action:
            return

        self.__action.unapply()
        self.__action = None
