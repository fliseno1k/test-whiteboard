from __future__ import annotations
from typing import TYPE_CHECKING
from abc import ABC, abstractmethod

from utils.unique_id import generate_id

if TYPE_CHECKING:
    from PySide6.QtGui import QColor


class Shape(ABC):
    def __init__(self):
        self.id = generate_id()
        self.left: int = 0
        self.top: int = 0
        self.width: int = 0
        self.height: int = 0
        self.background_color: QColor | None

    @property
    @abstractmethod
    def right(self):
        return self.left + self.width

    @property
    @abstractmethod
    def bottom(self):
        return self.top + self.height

    @abstractmethod
    def draw(self): ...

    @abstractmethod
    def get_bounding_rect(self):
        return [self.left, self.top, self.right, self.bottom]


class Rectangle(Shape):
    def __init__(self):
        super().__init__()


class Connector(Shape):
    def __init__(self):
        super().__init__()
