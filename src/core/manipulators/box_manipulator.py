from __future__ import annotations
from typing import TYPE_CHECKING

from ..controllers.box_move_controller import BoxMoveController
from ..shapes import ShapeKind

from .manipulator_manager import manipulator_manager

if TYPE_CHECKING:
    from .abstract_manipulator import AbstractManipulator


class BoxManipulator(AbstractManipulator):

    def __init__(self):
        super().__init__()

        self._controllers.append(BoxMoveController(self))


manipulator_manager.define(ShapeKind.RECTANGLE, BoxManipulator())