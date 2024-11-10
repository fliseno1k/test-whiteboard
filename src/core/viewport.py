from typing import List

from .geometry import path_bounding_rect, is_inside


class Viewport:

    def __init__(self, size: List[int] = [0, 0]):
        self.__top = 0
        self.__left = 0
        self.__width = size[0]
        self.__height = size[0]
        self.__memo_rect: List[List[int]] = self.__get_bounding_rect()

    def resize(self, size: List[int]):
        width, height = size
        self.__width = width
        self.__height = height
        self.__memo_rect = self.__get_bounding_rect()

    def rect_inside(self, rect: List[List[int]]):
        return is_inside(rect, self.__memo_rect)

    def __get_bounding_rect(self):
        return path_bounding_rect(
            [[self.__left, self.__top], [self.__width, self.__height]]
        )
