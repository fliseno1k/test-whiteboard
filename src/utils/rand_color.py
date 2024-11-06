import random
from typing import Callable, TypeVar

from PySide6.QtGui import QColor

T = TypeVar("T")


def __random_color_factory(constructor: Callable[[int, int, int], T]):
    def create_color():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)

        return constructor(r, g, b)

    return create_color


random_color = __random_color_factory(QColor)
