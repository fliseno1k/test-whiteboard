from __future__ import annotations
from copy import copy
from typing import TYPE_CHECKING, List

from .geometry import (
    path_bounding_rect,
    rect_width,
    rect_height,
    is_inside,
    intersects,
    move_rect,
)
from .shapes import Page, Path, Shape, Connector, Rectangle

if TYPE_CHECKING:
    from .transaction import Transaction


def add_shape(tx: Transaction, shape: Shape, parent: Shape):
    if isinstance(shape, Rectangle):
        inside_viewport = is_inside(shape.bounding_rect(), parent.bounding_rect())
        intersects_with_any = any(
            map(
                lambda child: intersects(shape.bounding_rect(), child.bounding_rect()),
                filter(lambda child: isinstance(child, Rectangle), parent.children),
            ),
        )

        if not inside_viewport or intersects_with_any:
            return False

    return tx.append_shape(shape) or change_parent(tx, shape, parent)


def change_parent(tx: Transaction, shape: Shape, parent: Shape):
    changed = False

    if parent:
        if shape.parent:
            changed = tx.remove_child(shape.parent, shape) or changed

        changed = tx.insert_child(parent, shape) or changed

    return changed


def move_shapes(tx: Transaction, page: Page, shapes: List[Shape], dx: int, dy: int):
    changed = False

    for shape in shapes:
        changed = move_single_shape(tx, page, shape, dx, dy) or changed

    if not changed:
        return

    connectors = filter(
        lambda connector: connector not in shapes, get_all_connectors(page, shapes)
    )

    for connector in connectors:
        if connector.head in shapes:
            changed = move_connector_end(tx, connector, dx, dy, True) or changed

        if connector.tail in shapes:
            changed = move_connector_end(tx, connector, dx, dy, False) or changed

    return changed


def move_single_shape(tx: Transaction, page: Page, shape: Shape, dx: int, dy: int):
    if isinstance(shape, Rectangle):
        moved = move_rect(shape.bounding_rect(), dx, dy)
        inside_viewport = is_inside(moved, page.bounding_rect())
        intersects_with_any = any(
            map(
                lambda child: child != shape
                and intersects(moved, child.bounding_rect()),
                filter(lambda child: isinstance(child, Rectangle), page.children),
            ),
        )

        if not inside_viewport or intersects_with_any:
            return False

    changed = tx.assign(shape, "left", shape.left + dx)
    changed = tx.assign(shape, "top", shape.top + dy) or changed

    if isinstance(shape, Path):
        changed = tx.assign(
            shape, "path", list(map(lambda x, y: [x + dx, y + dy], shape.path))
        )

    return changed


def move_connector_end(
    tx: Transaction, connector: Connector, dx: number, dy: number, is_head: bool
):
    point_index = 0
    if is_head:
        point_index = len(connector.path) - 1

    new_point = [
        connector.path[point_index][0] + dx,
        connector.path[point_index][1] + dy,
    ]
    new_path = copy(connector.path)
    new_path[point_index] = new_point

    return set_path(tx, connector, new_path)


def set_path(tx: Transaction, path_shape: Path, path: List[List[int]]):
    rect = path_bounding_rect(path)

    changed = tx.assign(path_shape, "path", path)
    changed = tx.assign(path_shape, "left", rect[0][0]) or changed
    changed = tx.assign(path_shape, "top", rect[0][1]) or changed
    changed = tx.assign(path_shape, "width", rect_width(rect)) or changed
    changed = tx.assign(path_shape, "height", rect_height(rect)) or changed

    return changed


def get_all_connectors(page: Page, shapes: List[Shape]):
    edges: List[Connector] = []

    def helper(shape: Shape, parent: Shape):
        nonlocal edges, shapes

        if not isinstance(shape, Connector):
            return

        if shape.tail in shapes:
            edges.append(shape)

        if shape.head in shapes:
            edges.append(shape)

    page.traverse(helper, page)

    return edges
