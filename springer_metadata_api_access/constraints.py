from abc import ABCMeta, abstractmethod
from enum import Enum

class Constraint(metaclass=ABCMeta):
    @property
    @abstractmethod
    def springer_metadata_expression(self) -> str:
        pass


class Atomic(Constraint, metaclass=ABCMeta):
    pass

class Logical(Constraint, metaclass=ABCMeta):
    constraint1: Constraint
    constraint2: Constraint

class Expression(Constraint):
    contained: Logical

    def springer_metadata_expression(self):
        pass

class EqualsField(Enum):
    pass

class Equals(Atomic):
    field: EqualsField
    value: str

    def springer_metadata_expression(self):
        pass

class ContainsField(Enum):
    pass

class Contains(Atomic):
    field: ContainsField
    value: str

    def springer_metadata_expression(self):
        pass

class SortField(Enum):
    pass

class Sort(Atomic):
    field: SortField

    def springer_metadata_expression(self):
        pass

class And(Logical):
    def springer_metadata_expression(self):
        pass

class Or(Logical):
    def springer_metadata_expression(self):
        pass