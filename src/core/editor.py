from __future__ import annotations
from typing import TYPE_CHECKING
from event_emitter import EventEmitter

if TYPE_CHECKING:
    from core.options import BaseOptions
    from handlers.abstract_handler import AbstractHandler


class Editor:
    def __init__(self, options: "BaseOptions"):
        self.__options: BaseOptions = options
        self.__handlers: dict[str, AbstractHandler] = {}
        self.__active_handler: AbstractHandler | None = None

        self.on_active_handler_change = EventEmitter()

        self.__initialize_handlers()

    @property
    def options(self):
        self.__options

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
