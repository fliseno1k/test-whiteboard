from __future__ import annotations
from abc import ABC, abstractmethod
from copy import copy
from enum import Enum
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .shapes import Shape
    from .store import Store


class MutationType(Enum):
    CREATE = "create"
    DELETE = "delete"
    ASSIGN = "assign"
    INSERT_CHILD = "insert-child"
    REMOVE_CHILD = "remove-child"


class Mutation(ABC):
    def __init__(self, type: MutationType):
        self.__type: type

    def type(self):
        return self.__type

    @abstractmethod
    def apply(self, store: Store): ...

    @abstractmethod
    def unapply(self, store: Store): ...


class CreateMutation(Mutation):
    def __init__(self, shape: Shape):
        super().__init__(MutationType.CREATE)

        self.__shape = shape

    def apply(self, store: Store):
        store.add_to_index(self.__shape)
        store.update(self.__shape)

    def unapply(self, store: Store):
        store.remove_from_index(self.__shape)
        store.update(self.__shape)


class InsertChildMutation(Mutation):
    def __init__(self, parent: Shape, child: Shape):
        super().__init__(MutationType.INSERT_CHILD)

        self.__parent = parent
        self.__child = child

    def apply(self, store: Store):
        self.__parent.children.append(self.__child)
        self.__child.parent = self.__parent

        store.update(self.__parent)
        store.update(self.__child)

    def unapply(self, store: Store):
        self.__parent.children.pop()
        self.__child.parent = None

        store.update(self.__parent)
        store.update(self.__child)


class RemoveChildMutation(Mutation):
    def __init__(self, parent: Shape, child: Shape):
        super().__init__(MutationType.REMOVE_CHILD)

        self.__parent = parent
        self.__child = child

    def apply(self, store: Store):
        self.__parent.children.pop()
        self.__child.parent = None

        store.update(self.__parent)
        store.update(self.__child)

    def unapply(self, store: Store):
        self.__parent.children.append(self.__child)
        self.__child.parent = None

        store.update(self.__parent)
        store.update(self.__child)


class AssignMutation(Mutation):
    def __init__(self, shape: Shape, field: str, value: any):
        super().__init__(MutationType.ASSIGN)

        self.__shape = shape
        self.__field = field
        self.__value = value
        self.__old_value = getattr(shape, field)

    def apply(self, store: Store):
        setattr(self.__shape, self.__field, self.__value)
        store.update(self.__shape)

    def unapply(self, store: Store):
        setattr(self.__shape, self.__field, self.__old_value)
        store.update(self.__shape)

    def update_value(self, new_value: any):
        self.__value = new_value


class AssignRefMutation(Mutation):
    def __init__(self, shape: Shape, field: str, value: any):
        super().__init__(MutationType.ASSIGN)

        self.__shape = shape
        self.__field = field
        self.__value = value
        self.__old_value = getattr(shape, field)

    def apply(self, store: Store):
        setattr(self.__shape, self.__field, self.__value)
        store.update(self.__shape)

    def unapply(self, store: Store):
        setattr(self.__shape, self.__field, self.__old_value)
        store.update(self.__shape)

    def update_value(self, new_value: any):
        self.__value = new_value


class Transaction:
    def __init__(self, store: Store):
        self.__store = store
        self.__mutations: list[Mutation] = []

    def size(self):
        return len(self.__mutations)

    def push(self, mutation: Mutation):
        self.__mutations.append(mutation)

    def apply(self):
        for mutation in self.__mutations:
            mutation.apply(self.__store)

    def unapply(self):
        for mutation in self.__mutations:
            mutation.unapply(self.__store)

    def append_shape(self, shape: Shape):
        if not self.__store.get_by_id(shape.id()):
            return False

        mutation = CreateMutation(shape)
        self.push(mutation)

        return True

    def insert_child(self, parent: Shape, shape: Shape):
        if shape in parent.children:
            return False

        mutation = InsertChildMutation(parent, shape)
        mutation.apply(self.__store)
        self.push(mutation)

        return True

    def remove_child(self, parent: Shape, shape: Shape):
        if shape not in parent.children:
            return False

        mutation = RemoveChildMutation(parent, shape)
        mutation.apply(self.__store)
        self.push(mutation)

        return True

    def assign(self, shape: Shape, field: str, value: any):
        if not hasattr(shape, field):
            return False

        old_value = getattr(shape, field)
        if old_value == value:
            return False

        existing_mutation = next(
            (
                mutation
                for mutation in self.__mutations
                if (
                    isinstance(mutation, AssignMutation)
                    and hasattr(mutation, "__shape")
                    and getattr(mutation, "__shape") == shape
                    and hasattr(mutation, "__field")
                    and getattr(mutation, "__field") == field
                )
            ),
            None,
        )

        if existing_mutation:
            existing_mutation.update_value(copy(value))
            existing_mutation.apply(self.__store)
        else:
            assign_mutation = AssignMutation(shape, field, copy(value))
            assign_mutation.apply(self.__store)

            self.__mutations.append(assign_mutation)

        return True

    def assign_ref(self, shape: Shape, field: str, value: any):
        if not hasattr(shape, field):
            return False

        old_value = getattr(shape, field)
        if old_value == value:
            return False

        existing_mutation = next(
            (
                mutation
                for mutation in self.__mutations
                if (
                    isinstance(mutation, AssignRefMutation)
                    and hasattr(mutation, "__shape")
                    and getattr(mutation, "__shape") == shape
                    and hasattr(mutation, "__field")
                    and getattr(mutation, "__field") == field
                )
            ),
            None,
        )

        if existing_mutation:
            existing_mutation.update_value(value)
            existing_mutation.apply(self.__store)
        else:
            assign_mutation = AssignRefMutation(shape, field, value)
            assign_mutation.apply(self.__store)

            self.__mutations.append(assign_mutation)

        return True
