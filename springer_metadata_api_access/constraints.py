from abc import ABCMeta, abstractmethod
from enum import Enum, EnumMeta

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

def _enquote_string( string: str) -> str:
        if ' ' in string and not(string.startswith('"') and string.endswith('"')):
            return f'"{string}"'
        else:
            return string

class Expression(Constraint):
    __contained: Logical

    def __init__(self, logical_constraint: Logical):
        assert isinstance(logical_constraint, Logical)
        self.__contained = logical_constraint

    def _springer_metadata_expression(self):
        return f'({self.__contained._springer_metadata_expression()})'

class And(Logical):
    def _springer_metadata_expression(self):
        return f'{self._constraint1._springer_metadata_expression()} and {self._constraint2._springer_metadata_expression()}'

class Or(Logical):
    def _springer_metadata_expression(self):
        return f'{self._constraint1._springer_metadata_expression()} or {self._constraint2._springer_metadata_expression()}'

class EqualsField(Enum):
    DOI = 'doi'
    SUBJECT = 'subject'
    KEYWORD = 'keyword'
    PUBLICATION = 'pub'
    YEAR = 'year'
    ONLINEDATE = 'onlinedate'
    COUNTRY = 'country'
    ISBN = 'isbn'
    ISSN = 'issn'
    JOURNAL_ID = 'journalid'
    TOPICAL_COLLECTION = 'topicalcollection'
    DATE = 'date'
    ISSUE_TYPE = 'issuetype'
    ISSUE = 'issue'
    VOLUME = 'volume'
    TYPE = 'type'

class ContainsField(Enum):
    EMPTY = 0
    TITLE = 'title'
    ORGANIZATION_NAME = 'orgname'
    JOURNAL = 'journal'
    BOOK = 'book'
    NAME = 'name'

class SortField(Enum):
    DATE = 'date'
    SEQUENCE = 'sequence'

class Equals(Atomic):
    __field: EqualsField
    __value: str

    def __init__(self, field: EqualsField, value: str):
        assert isinstance(field, EqualsField), 'Field should be an EqualsField.'
        self.__field = field
        self.__value = value if value is str else value.__str__()

    def _springer_metadata_expression(self):
        return f'{self.__field.value}:{_enquote_string(self.__value)}'

class Contains(Atomic):
    __field: ContainsField
    __value: str

    def __init__(self, field: ContainsField, value: str):
        assert isinstance(field, ContainsField), 'Field should be a ContainsField.'
        self.__field = field
        self.__value = value if value is str else value.__str__()

    def _springer_metadata_expression(self):
        if(self.__field == ContainsField.EMPTY):
            return f'{self.__value}'

        return f'{self.__field.value}:{_enquote_string(self.__value)}'

class Sort(Atomic):
    __field: SortField

    def __init__(self, field: SortField):
        assert isinstance(field, SortField), 'Field should be a SortField.'
        self.__field = field

    def _springer_metadata_expression(self):
        return f'sort:{self.__field.value}'

class __AbstractEnumMeta(EnumMeta, ABCMeta):
    pass

class Flag(Atomic, Enum, metaclass=__AbstractEnumMeta):
    JOURNAL_ONLINE_FIRST = 'journalonlinefirst:true'
    OPEN_ACCESS = 'openaccess:true'

    def _springer_metadata_expression(self):
        return self.value

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