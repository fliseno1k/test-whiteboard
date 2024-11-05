from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING, Callable, cast, List, Optional

from core.transaction import Transaction

if TYPE_CHECKING:
    from core.store import Store


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

    @property
    def name(self):
        return self.__name

    @property
    def length(self):
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

    def transact(self, fn: Callable[[Transaction], None]):
        transaction = Transaction(self.__store)
        fn(transaction)

        if not transaction.length:
            return

        if self.__action:
            self.__action.push(transaction)
        else:
            self.startAction(ActionKind.UNKNOWN)
            cast(Action, self.__action).push(transaction)
            self.endAction()

    def start_action(self, name: str):
        if self.__action is not None and self.__action.length > 0:
            self.endAction()

        self.__action = Action(name)

    def end_action(self):
        self.__action = None

    def cancel_action(self):
        if self.__action is None:
            return

        self.__action.unapply()
        self.__action = None
