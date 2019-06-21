from abc import ABCMeta, abstractmethod
from enum import Enum

class Constraint(metaclass=ABCMeta):
    @property
    @abstractmethod
    def _springer_metadata_expression(self) -> str:
        pass

class Atomic(Constraint, metaclass=ABCMeta):
    pass

class Logical(Constraint, metaclass=ABCMeta):
    _constraint1: Constraint
    _constraint2: Constraint

    def __init__(self, constraint1: Constraint, constraint2: Constraint):
        self._constraint1 = constraint1
        self._constraint2 = constraint2

class Expression(Constraint):
    __contained: Logical

    def __init__(self, logical_constraint: Logical):
        self.__contained = logical_constraint

    def _springer_metadata_expression(self):
        pass

class EqualsField(Enum):
    pass

class Equals(Atomic):
    __field: EqualsField
    __value: str

    def __init__(self, field: EqualsField, value: str):
        self.__field = field
        self.__value = value

    def _springer_metadata_expression(self):
        pass

class ContainsField(Enum):
    pass

class Contains(Atomic):
    __field: ContainsField
    __value: str

    def __init__(self, field: ContainsField, value: str):
        self.__field = field
        self.__value = value

    def _springer_metadata_expression(self):
        pass

class SortField(Enum):
    pass

class Sort(Atomic):
    __field: SortField

    def __init__(self, field: SortField):
        self.__field = field

    def _springer_metadata_expression(self):
        pass

class And(Logical):
    def _springer_metadata_expression(self):
        pass

class Or(Logical):
    def _springer_metadata_expression(self):
        pass

def EXPR(contained: Logical) -> Constraint:
    return Expression(contained)

def AND(constraint1: Constraint, constraint2: Constraint) -> Logical:
    return And(constraint1, constraint2)

def OR(constraint1: Constraint, constraint2: Constraint) -> Logical:
    return Or(constraint1, constraint2)

def EQ(field: EqualsField, value: str) -> Constraint:
    return Equals(field, value)

def CONTAINS(field: ContainsField, value: str) -> Constraint:
    return Contains(field, value)

def IN(value: str, field: ContainsField) -> Constraint:
    return Contains(field, value)

def SORT(field: SortField) -> Constraint:
    return Sort(field)