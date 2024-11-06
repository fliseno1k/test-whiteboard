from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, List

if TYPE_CHECKING:
    from .handlers.abstract_handler import AbstractHandler


@dataclass
class Options:
    grid_size: int = 20

    grid_visible: bool = True

    default_handler_id: Optional[str] = None

    handlers: List[AbstractHandler] = field(default_factory=list)


class OptionsBuilder:
    def __init__(self):
        self.__options = Options()

    def set_default_handler_id(self, id: str):
        self.__options.default_handler_id = id
        return self

    def set_handlers(self, handlers: list[AbstractHandler]):
        self.__options.handlers += handlers
        return self

    def build(self):
        return Options(
            default_handler_id=self.__options.default_handler_id,
            handlers=self.__options.handlers,
        )
