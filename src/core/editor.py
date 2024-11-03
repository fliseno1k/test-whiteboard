from __future__ import annotations
from typing import TYPE_CHECKING
from event_emitter import EventEmitter

from core.factory import ShapeFactory

if TYPE_CHECKING:
    from core.options import BaseOptions
    from handlers.abstract_handler import AbstractHandler


class Editor:
    def __init__(self, options: "BaseOptions"):
        self.__options: BaseOptions = options

        self.__handlers: dict[str, AbstractHandler] = {}

        self.__active_handler: AbstractHandler | None = None

        self.__shape_factory = ShapeFactory(self)

        self.on_active_handler_change = EventEmitter()

        self.__initialize_handlers()

    @property
    def options(self):
        self.__options

    @property
    def active_handler(self):
        return self.__active_handler

    @property
    def handlers(self):
        return self.__handlers.items()

    @property
    def factory(self):
        return self.__shape_factory

    def activate_handler(self, handler_id: str):
        handler = self.__handlers.get(handler_id)

        if self.__active_handler:
            # TODO: deactivate current handler
            None

        if handler:
            self.__active_handler = handler
            # TODO: active handler & notify ui about changes

    def __initialize_handlers(self):
        for handler in self.__options.handlers:
            self.__handlers[handler.id] = handler
