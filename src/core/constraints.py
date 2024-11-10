from __future__ import annotations
from typing import TYPE_CHECKING, List

from .geometry import is_inside, intersects

if TYPE_CHECKING:
    from .shapes import Shape


def inside(parent: Shape, shape: Shape):
    return is_inside(shape.bounding_rect(), parent.bounding_rect())


def intersects_any(shape: Shape, neighbours: List[Shape]):
    return not any(
        map(
            lambda child: intersects(shape.bounding_rect(), child.bounding_rect()),
            neighbours,
        )
    )
