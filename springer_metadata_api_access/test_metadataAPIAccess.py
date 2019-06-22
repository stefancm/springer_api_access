from unittest import TestCase
from dataclasses import dataclass, field
from springer_metadata_api_access.component import MetadataAPIAccess, MetadataAPISettigs
from typing import Type, TypeVar, List

import configparser
config = configparser.ConfigParser()

config.read('Test.ini')
api_key: str = config['General']['ApiKey']



class TestMetadataAPIAccess(TestCase):

    def test_articles_in_book(self):
        self.fail()

    def test_articles_in_journal(self):
        self.fail()

    def test_articles(self):
        self.fail()

    T = TypeVar('T')
    def base_arrange_act_test_article(self, recordType: Type[T]) -> T:
        settings = MetadataAPISettigs()
        settings.api_key = api_key
        settings.page_size = 10

        component = MetadataAPIAccess(settings)


        doi = '10.1007/978-3-540-74930-1_26'

        if recordType is not None:
            return component.article(doi, recordType)
        else:
            return component.article(doi)

    def test_article(self):

        with self.subTest('Record type is dataclass'):
            @dataclass
            class TestArticleDataClass:
                title: str
                abstract: str
                publication_date: str = field(metadata={'load_from':'publicationDate'})
            result = self.base_arrange_act_test_article(TestArticleDataClass)
            self.assertEqual(result.title, 'Semantic Web and Rule Reasoning inside of E-Learning Systems')
            self.assertEqual(result.abstract, 'SummaryThis paper describes how the Semantic Web and the JenaRules can work together in order to empower e-Learning platform Moodle with rich reports and flexible courses management. We discuss aspects of using Semantic Web technologies in e-learning in general and the JenaRules in particular. The main focus is towards using rules for reasoning on top of existing Moodle content.')
            self.assertEqual(result.publication_date, '2008-01-01')

        with self.subTest('Record type is non dataclass'):
            class TestArticleNonDataClass:
                title: str
                abstract: str
                publication_date: str = field(metadata={'load_from': 'publicationDate'})
            result = self.base_arrange_act_test_article(TestArticleNonDataClass)
            self.assertEqual(result.title, 'Semantic Web and Rule Reasoning inside of E-Learning Systems')
            self.assertEqual(result.abstract, 'SummaryThis paper describes how the Semantic Web and the JenaRules can work together in order to empower e-Learning platform Moodle with rich reports and flexible courses management. We discuss aspects of using Semantic Web technologies in e-learning in general and the JenaRules in particular. The main focus is towards using rules for reasoning on top of existing Moodle content.')
            self.assertEqual(result.publication_date, '2008-01-01')

        with self.subTest('Record type is not provided'):
            result = self.base_arrange_act_test_article(None)
            self.assertEqual(result['title'], 'Semantic Web and Rule Reasoning inside of E-Learning Systems')
            self.assertEqual(result['abstract'], 'SummaryThis paper describes how the Semantic Web and the JenaRules can work together in order to empower e-Learning platform Moodle with rich reports and flexible courses management. We discuss aspects of using Semantic Web technologies in e-learning in general and the JenaRules in particular. The main focus is towards using rules for reasoning on top of existing Moodle content.')
            self.assertEqual(result['publicationDate'], '2008-01-01')
            self.assertEqual(result['publicationName'], 'Advances in Intelligent and Distributed Computing')
