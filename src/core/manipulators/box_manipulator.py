from __future__ import annotations
from typing import TYPE_CHECKING

from ..controllers.box_move_controller import BoxMoveController
from ..shapes import ShapeKind

from .abstract_manipulator import AbstractManipulator

if TYPE_CHECKING:
    from .manipulator_manager import ManipulatorManager


class BoxManipulator(AbstractManipulator):

    @classmethod
    def define(cls, manager: ManipulatorManager):
        manager.define(ShapeKind.RECTANGLE, cls())

    def __init__(self):
        super().__init__()

        self._controllers.append(BoxMoveController(self))
