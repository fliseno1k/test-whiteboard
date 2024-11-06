from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Dict, Callable

from .events import EventEmitter, EventKind
from .factory import ShapeFactory
from .store import Store
from .transform import Transform

if TYPE_CHECKING:
    from PySide6.QtGui import QPainter

    from .handlers.abstract_handler import AbstractHandler
    from .options import BaseOptions


class Editor:
    def __init__(self, options: "BaseOptions"):
        self.__options: BaseOptions = options

        self.__events: Dict[EventKind, EventEmitter] = {}
        self.__handlers: dict[str, AbstractHandler] = {}
        self.__active_handler: Optional[AbstractHandler] = None

        self.__store = Store()
        self.__transform = Transform(self.__store)
        self.__shape_factory = ShapeFactory(self)

        self.__initialize_state()
        self.__initialize_events()
        self.__initialize_handlers()

    @property
    def active_handler(self):
        return self.__active_handler

    @property
    def handlers(self):
        return self.__handlers.values()

    @property
    def shape_factory(self):
        return self.__shape_factory

    @property
    def transform(self):
        return self.__transform

    @property
    def current_page(self):
        return self.__store.root

    def add_listener(self, event: EventKind, fn: Callable):
        self.__events[event].add_listener(fn)

    def remove_listener(self, event: EventKind, fn: Callable):
        self.__events[event].remove_listener(fn)

    def draw(self, painter: QPainter):
        self.__store.root.draw(painter)

    def emit_repaint(self):
        self.__events[EventKind.UPDATE].emit()

    def activate_handler(self, handler_id: str):
        handler = self.__handlers.get(handler_id)

        if self.__active_handler:
            # TODO: deactivate current handler
            None

        if handler:
            self.__active_handler = handler
            # TODO: active handler & notify ui about changes

    def __initialize_state(self):
        self.__transform.on_action.add_listener(self.emit_repaint)
        self.__transform.on_transaction.add_listener(self.emit_repaint)

    def __initialize_events(self):
        self.__events.update({EventKind.UPDATE: EventEmitter()})

    def __initialize_handlers(self):
        for handler in self.__options.handlers:
            self.__handlers[handler.id] = handler

        default_handler = self.__options.default_handler_id
        if default_handler and default_handler in self.__handlers:
            self.__active_handler = self.__handlers.get(default_handler)
