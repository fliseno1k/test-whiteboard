from __future__ import annotations
from typing import TYPE_CHECKING
from dataclasses import dataclass

if TYPE_CHECKING:
    from core.handlers.abstract_handler import AbstractHandler


class BaseOptions:
    grid_size: int = 20

    grid_visible: bool = True

    default_handler_id: str = None

    handlers: list[AbstractHandler] = []


@dataclass(frozen=True)
class ImmutableOptions(BaseOptions):
    pass


@dataclass(frozen=False)
class MutableOptions(BaseOptions):
    pass


class OptionsBuilder:
    def __init__(self):
        self.__options = MutableOptions()

    def set_default_handler_id(self, id: str):
        self.__options.default_handler_id = id
        return self

    def set_handlers(self, handlers: list[AbstractHandler]):
        self.__options.handlers += handlers
        return self

    def build(self):
        return ImmutableOptions(*vars(self.__options))
