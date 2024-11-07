from typing import TYPE_CHECKING, Dict

from utils.singleton import Singleton

if TYPE_CHECKING:
    from .abstract_manipulator import AbstractManipulator


class _ManipulatorManager(metaclass=Singleton):
    def __init__():
        self._manipulators: Dict[str, AbstractManipulator] = {}

    def define(self, type: str, manipulator: AbstractManipulator):
        self._manipulators[type] = manipulator

    def get(self, type: str):
        return self._manipulators.get(type)


manipulator_manager = _ManipulatorManager()