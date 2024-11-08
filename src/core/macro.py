from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .shapes import Page, Shape
    from .transaction import Transaction


def add_shape(tx: Transaction, shape: Shape, parent: Shape):
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
        changed = move_single_shape(tx, shape, dx, dy) or changed

    return changed


def move_single_shape(tx: Transaction, shape: Shape, dx: int, dy: int):
    changed = tx.assign(shape, "left", shape.left + dx)
    changed = tx.assign(shape, "top", shape.top + dy) or changed

    return changed
