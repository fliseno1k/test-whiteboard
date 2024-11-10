import math
from copy import copy
from typing import List


def path_bounding_rect(path: List[List[int]]):
    xs = list(map(lambda point: point[0], path))
    ys = list(map(lambda point: point[1], path))

    return [
        [min(xs), min(ys)],
        [max(xs), max(ys)],
    ]


def rect_width(rect: List[List[int]]):
    return abs(rect[1][0] - rect[0][0])


def rect_height(rect: List[List[int]]):
    return abs(rect[1][1] - rect[0][1])


def get_nearest_segment(point: List[int], path: List[List[int]], buffer_distance: int):
    for index in range(0, len(path) - 1):
        distance = distance_to_line(point, [path[index], path[index + 1]])

        if distance < buffer_distance:
            return index

    return -1


def distance2(point1, point2):
    return (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2


def distance_to_line(point: List[int], line: List[List[int]]):
    sp = line[0]
    ep = line[1]
    l2 = distance2(sp, ep)
    if l2 == 0:
        return distance2(point, sp)

    t = (
        (point[0] - sp[0]) * (ep[0] - sp[0]) + (point[1] - sp[1]) * (ep[1] - sp[1])
    ) / l2
    t = max(0, min(1, t))

    squared = distance2(
        point,
        [
            sp[0] + t * (ep[0] - sp[0]),
            sp[1] + t * (ep[1] - sp[1]),
        ],
    )

    return math.sqrt(squared)


def is_inside(inner_rect: List[List[int]], outer_rect: List[List[int]]):
    return (
        inner_rect[0][0] >= outer_rect[0][0]
        and inner_rect[1][0] <= outer_rect[1][0]
        and inner_rect[0][1] >= outer_rect[0][1]
        and inner_rect[1][1] <= outer_rect[1][1]
    )


def intersects(rect1: List[List[int]], rect2: List[List[int]]):
    return not (
        rect1[1][0] <= rect2[0][0]
        or rect1[0][0] >= rect2[1][0]
        or rect1[1][1] <= rect2[0][1]
        or rect1[0][1] >= rect2[1][1]
    )


def move_rect(rect: List[List[int]], dx: int, dy: int):
    rect_copy = copy(rect)

    return [
        [rect_copy[0][0] + dx, rect_copy[0][1] + dy],
        [rect_copy[1][0] + dx, rect_copy[1][1] + dy],
    ]
