from typing import Dict

from utils.singleton import Singleton

from .abstract_manipulator import AbstractManipulator


class ManipulatorManager(metaclass=Singleton):
    def __init__(self):
        self._manipulators: Dict[str, AbstractManipulator] = {}

    def define(self, type: str, manipulator: AbstractManipulator):
        self._manipulators[type] = manipulator

    def get(self, type: str):
        return self._manipulators.get(type)


manipulator_manager = ManipulatorManager()
