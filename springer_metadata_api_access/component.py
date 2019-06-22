from .constraints import Constraint
from typing import Type, TypeVar, List, Generic

def __request(self, url: str) -> dict:
    import urllib.request
    pass

T = TypeVar('T')
def __decorate_dataclass(recordType: Type[T]) -> Type[T]:
    from marshmallow_dataclass import dataclass, add_schema
    pass

class MetadataAPISettigs:
    api_key: str
    page_size: int


class MetadataAPIAccess:
    BOOK_ARTICLES_URL_FORMAT = ""
    JOURNAL_ARTICLES_URL_FORMAT = ""
    ARTICLES_URL_FORMAT = ""
    SINGLE_ARTICLE_URL_FORMAT = ""

    __settings: MetadataAPISettigs

    def __init__(self, settings: MetadataAPISettigs):
        self.__settings = settings

    class PagingInformation:
        pass

    TRecord = TypeVar('TRecord')

    def articles_in_book(self, isbn: str, query: Constraint = None, record_dataclass: Type[TRecord] = dict) -> List[TRecord]:
        pass

    def articles_in_journal(self, issn: str, query: Constraint = None, record_dataclass: Type[TRecord] = dict) -> List[TRecord]:
        pass

    def articles(self, query: Constraint = None, record_dataclass: Type[TRecord] = dict) -> List[TRecord]:
        pass

    def article(self, doi: str, record_dataclass: Type[TRecord] = dict) -> List[TRecord]:
        pass

