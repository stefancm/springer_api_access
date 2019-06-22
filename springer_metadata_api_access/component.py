from springer_metadata_api_access.constraints import Constraint
from typing import Type, TypeVar, List, Generic

def _request(url: str) -> dict:
    import urllib.request
    import json

    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        r = response.read()
        return json.loads(r)

T = TypeVar('T')
def _decorate_dataclass(recordType: Type[T]) -> Type[T]:
    import dataclasses
    from marshmallow_dataclass import dataclass, add_schema

    if dataclasses.is_dataclass(recordType):
        return add_schema(recordType)
    else:
        return dataclass(recordType)

class MetadataAPISettigs:
    api_key: str
    page_size: int


class MetadataAPIAccess:
    BOOK_ARTICLES_URL_FORMAT = "http://api.springernature.com/metadata/json/isbn/%s"
    JOURNAL_ARTICLES_URL_FORMAT = "http://api.springernature.com/metadata/json/issn/%s"
    ARTICLES_URL_FORMAT = "http://api.springernature.com/metadata/json"
    SINGLE_ARTICLE_URL_FORMAT = "http://api.springernature.com/metadata/json/doi/%s"

    __settings: MetadataAPISettigs

    def __init__(self, settings: MetadataAPISettigs):
        self.__settings = settings

    class PagingInformation:
        pass

    def __add_parameters(self, url, query: Constraint = None):
        result = url + '?'

        result = result + f'api_key={self.__settings.api_key}'

        if query is not None:
            import urllib.request
            assert isinstance(query, Constraint), 'Query should be a constraint.'
            escaped_expression = urllib.request.quote(query._springer_metadata_expression())
            result = result + '&' + f'q={escaped_expression}'

        return result

    TRecord = TypeVar('TRecord')
    def __base_articles(self, url_string: str, query: Constraint, record_dataclass: Type[TRecord]) -> List[TRecord]:
        url_string = self.__add_parameters(url_string, query)
        result_dict = _request(url_string)

        if not result_dict['records']:
            return None
        else:
            if record_dataclass is not dict:
                record_marshmallow_dataclass = _decorate_dataclass(record_dataclass)
                result, _ = record_marshmallow_dataclass.Schema().load(result_dict['records'], many=True)
                return result
            else:
                return result_dict['records']

    def articles_in_book(self, isbn: str, query: Constraint = None, record_dataclass: Type[TRecord] = dict) -> List[TRecord]:
        return self.__base_articles(self.BOOK_ARTICLES_URL_FORMAT % isbn, query, record_dataclass)

    def articles_in_journal(self, issn: str, query: Constraint = None, record_dataclass: Type[TRecord] = dict) -> List[TRecord]:
        return self.__base_articles(self.JOURNAL_ARTICLES_URL_FORMAT % issn, query, record_dataclass)

    def articles(self, query: Constraint = None, record_dataclass: Type[TRecord] = dict) -> List[TRecord]:
        return self.__base_articles(self.ARTICLES_URL_FORMAT, query, record_dataclass)

    def article(self, doi: str, record_dataclass: Type[TRecord] = dict) -> TRecord:
        url_string = self.SINGLE_ARTICLE_URL_FORMAT % doi
        url_string = self.__add_parameters(url_string)
        result_dict = _request(url_string)

        if not result_dict['records']:
            return None
        else:
            if record_dataclass is not dict:
                record_marshmallow_dataclass = _decorate_dataclass(record_dataclass)
                result, _ = record_marshmallow_dataclass.Schema().load(result_dict['records'][0])
                return result
            else:
                return result_dict['records'][0]

