from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Dict, Callable

from .events import EventKind, setup_events
from .factory import ShapeFactory
from .manipulators.manipulator_manager import ManipulatorManager
from .manipulators.box_manipulator import BoxManipulator
from .selection import Selection
from .store import Store
from .transform import Transform


if TYPE_CHECKING:
    from PySide6.QtGui import QPainter, QMouseEvent

    from utils.event_emmiter import EventEmitter

    from .handlers.abstract_handler import AbstractHandler
    from .options import BaseOptions


class Editor:
    def __init__(self, options: "BaseOptions"):
        self.__options: BaseOptions = options

        self.__events: Dict[EventKind, EventEmitter] = {}
        self.__handlers: Dict[str, AbstractHandler] = {}
        self.__active_handler: Optional[AbstractHandler] = None

        self.store = Store()
        self.selection = Selection(self)
        self.transform = Transform(self.store)
        self.shape_factory = ShapeFactory(self)
        self.manipulator_manager = ManipulatorManager()

        self.__initialize_action_handlers()
        self.__initialize_events()
        self.__initialize_handlers()
        self.__initialize_manipulators()

    def active_handler(self):
        return self.__active_handler

    def handlers(self):
        return self.__handlers.items()

    def current_page(self):
        return self.store.root()

    def add_listener(self, event: EventKind, fn: Callable):
        self.__events[event].add_listener(fn)

    def remove_listener(self, event: EventKind, fn: Callable):
        self.__events[event].remove_listener(fn)

    def draw(self, painter: QPainter):
        self.store.root().draw(painter)

    def updated(self):
        self.__events[EventKind.UPDATED].emit()

    def activate_handler(self, handler_id: str):
        self.__active_handler = None

        handler = self.__handlers.get(handler_id)
        if handler:
            self.__active_handler = handler

        self.__events[EventKind.ACTIVE_HANDLER_CHANGED].emit()

    def on_mouse_press_event(self, event: QMouseEvent):
        if not self.__active_handler:
            return

        self.__active_handler.on_mouse_press_event(self, event)

    def on_mouse_move_event(self, event: QMouseEvent):
        if not self.__active_handler:
            return

        self.__active_handler.on_mouse_move_event(self, event)

    def on_mouse_release_event(self, event: QMouseEvent):
        if not self.__active_handler:
            return

        self.__active_handler.on_mouse_release_event(self, event)

    def on_mouse_double_click_event(self, event: QMouseEvent):
        if not self.__active_handler:
            return

        self.__active_handler.on_mouse_double_click_event(self, event)

    def __initialize_action_handlers(self):
        self.transform.on_action.add_listener(self.updated)
        self.transform.on_transaction.add_listener(self.updated)

    def __initialize_events(self):
        self.__events = setup_events()

    def __initialize_handlers(self):
        handler_id = self.__options.default_handler_id

        for handler in self.__options.handlers:
            self.__handlers.update({handler.id(): handler})

        if handler_id and (handler_id in self.__handlers.keys()):
            self.__active_handler = self.__handlers.get(handler_id)
            self.__events[EventKind.ACTIVE_HANDLER_CHANGED].emit()

    def __initialize_manipulators(self):
        BoxManipulator.define(self.manipulator_manager)
