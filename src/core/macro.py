from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .shapes import Shape
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
