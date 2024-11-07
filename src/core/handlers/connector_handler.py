from __future__ import annotations
from typing import TYPE_CHECKING

from .abstract_handler import AbstractHandler

if TYPE_CHECKING:
    from PySide6.QtGui import QMouseEvent

    from ..editor import Editor


class ConnectorHandler(AbstractHandler):
    def __init__(self, id: str):
        super().__init__(id)