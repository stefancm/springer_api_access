from unittest import TestCase
from dataclasses import dataclass, field
from springer_metadata_api_access.component import MetadataAPIAccess, MetadataAPISettigs
from springer_metadata_api_access.constraints import AND,OR,EQ,SORT,CONTAINS,EqualsField,ContainsField,SortField
from typing import Type, TypeVar, List

import configparser
config = configparser.ConfigParser()

config.read('Test.ini')
api_key: str = config['General']['ApiKey']


@dataclass
class TestArticleDataClass:
    title: str
    abstract: str
    publication_date: str = field(metadata={'load_from': 'publicationDate'})

class TestArticleNonDataClass:
    title: str
    abstract: str
    publication_date: str = field(metadata={'load_from': 'publicationDate'})

class TestMetadataAPIAccess(TestCase):

    def test_articles_in_book(self):
        T = TypeVar('T')
        def base_arrange_act_test_articles(recordType: Type[T]) -> List[T]:
            settings = MetadataAPISettigs()
            settings.api_key = api_key
            settings.page_size = 10

            component = MetadataAPIAccess(settings)

            isbn = '978-3-319-99625-7'

            query = AND(CONTAINS(ContainsField.NAME,'Bădică'),SORT(SortField.SEQUENCE))

            if recordType is not None:
                return component.articles_in_book(isbn, query, recordType)
            else:
                return component.articles_in_book(isbn, query)

        with self.subTest('Record type is dataclass'):
            results = base_arrange_act_test_articles(TestArticleDataClass)
            self.assertEqual(len(results), 2)
            self.assertEqual(results[0].title, 'Collective Profitability of DAG-Based Selling-Buying Intermediation Processes')
            self.assertEqual(results[0].abstract, 'AbstractWe revisit our formal model of intermediation business processes and propose its generalization from trees to DAGs. With the new model, a company can use multiple sellers to better reach the market of potential buyers interested in purchasing its products. The sellers are engaged in transactions via a set of intermediaries that help connecting with end customers, rather than acting directly in the market. This process can be represented by a complex DAG-structured business transaction. In this work we present a formal model based on DAGs of such transactions and we generalize our results regarding collectively profitable intermediation transactions.')
            self.assertEqual(results[1].title, 'Knowledge-Based Metrics for Document Classification: Online Reviews Experiments')
            self.assertEqual(results[1].abstract, 'AbstractIn this paper we propose a new method that addresses the documents classification problem with respect to their topic. The presented method takes into consideration only textual measures. We exemplify the method by considering three sets of documents of gradually different topics: (i) the first two sets contain reviews that comment the published entity features characteristics representing electronic devices – laptops and mobile phones; (ii) the third set contains reviews about touristic locations. All the review texts are written in Romanian and were extracted by crawling popular Romanian sites. The paper presents and discusses the obtained evaluation scores after the application of textual measures.')

        with self.subTest('Record type is non dataclass'):
            results = base_arrange_act_test_articles(TestArticleNonDataClass)
            self.assertEqual(len(results), 2)
            self.assertEqual(results[0].title, 'Collective Profitability of DAG-Based Selling-Buying Intermediation Processes')
            self.assertEqual(results[0].abstract, 'AbstractWe revisit our formal model of intermediation business processes and propose its generalization from trees to DAGs. With the new model, a company can use multiple sellers to better reach the market of potential buyers interested in purchasing its products. The sellers are engaged in transactions via a set of intermediaries that help connecting with end customers, rather than acting directly in the market. This process can be represented by a complex DAG-structured business transaction. In this work we present a formal model based on DAGs of such transactions and we generalize our results regarding collectively profitable intermediation transactions.')
            self.assertEqual(results[1].title, 'Knowledge-Based Metrics for Document Classification: Online Reviews Experiments')
            self.assertEqual(results[1].abstract, 'AbstractIn this paper we propose a new method that addresses the documents classification problem with respect to their topic. The presented method takes into consideration only textual measures. We exemplify the method by considering three sets of documents of gradually different topics: (i) the first two sets contain reviews that comment the published entity features characteristics representing electronic devices – laptops and mobile phones; (ii) the third set contains reviews about touristic locations. All the review texts are written in Romanian and were extracted by crawling popular Romanian sites. The paper presents and discusses the obtained evaluation scores after the application of textual measures.')


        with self.subTest('Record type is not provided'):
            results = base_arrange_act_test_articles(None)
            self.assertEqual(len(results), 2)
            self.assertEqual(results[0]['title'], 'Collective Profitability of DAG-Based Selling-Buying Intermediation Processes')
            self.assertEqual(results[0]['abstract'], 'AbstractWe revisit our formal model of intermediation business processes and propose its generalization from trees to DAGs. With the new model, a company can use multiple sellers to better reach the market of potential buyers interested in purchasing its products. The sellers are engaged in transactions via a set of intermediaries that help connecting with end customers, rather than acting directly in the market. This process can be represented by a complex DAG-structured business transaction. In this work we present a formal model based on DAGs of such transactions and we generalize our results regarding collectively profitable intermediation transactions.')
            self.assertEqual(results[0]['publicationName'], 'Intelligent Distributed Computing XII')
            self.assertEqual(results[1]['title'], 'Knowledge-Based Metrics for Document Classification: Online Reviews Experiments')
            self.assertEqual(results[1]['abstract'], 'AbstractIn this paper we propose a new method that addresses the documents classification problem with respect to their topic. The presented method takes into consideration only textual measures. We exemplify the method by considering three sets of documents of gradually different topics: (i) the first two sets contain reviews that comment the published entity features characteristics representing electronic devices – laptops and mobile phones; (ii) the third set contains reviews about touristic locations. All the review texts are written in Romanian and were extracted by crawling popular Romanian sites. The paper presents and discusses the obtained evaluation scores after the application of textual measures.')
            self.assertEqual(results[1]['publicationName'], 'Intelligent Distributed Computing XII')

    def test_articles_in_journal(self):
        T = TypeVar('T')
        def base_arrange_act_test_articles(recordType: Type[T]) -> List[T]:
            settings = MetadataAPISettigs()
            settings.api_key = api_key
            settings.page_size = 10

            component = MetadataAPIAccess(settings)

            issn = '1434-601X'

            query = AND(AND(CONTAINS(ContainsField.NAME,'Bădică'),SORT(SortField.SEQUENCE)),EQ(EqualsField.PUBLICATION,'Zeitschrift für Physik A Atoms and Nuclei'))

            if recordType is not None:
                return component.articles_in_journal(issn, query, recordType)
            else:
                return component.articles_in_journal(issn, query)

        with self.subTest('Record type is dataclass'):
            results = base_arrange_act_test_articles(TestArticleDataClass)
            self.assertEqual(len(results), 3)
            self.assertEqual(results[0].title, 'Magnetic moment measurement of 108 keV level in151Gd')
            self.assertEqual(results[0].abstract, 'AbstractThe magnetic momentμ=−(1.23±0.17)μN of the first excited state in151Gd was determined by integral perturbed angular correlation (IPAC) in external magnetic field.')
            self.assertEqual(results[2].title, 'Magnetic moment measurements in64Zn and66Zn')
            self.assertEqual(results[2].abstract, 'AbstractThe ratios of the ∥g∥-factors of the 7−, 4.635 MeV level in64Zn and 6−, 4.074 MeV and 7−, 4.250 MeV levels in66Zn has been found to be (1±0.18)∶(0.64±0.14)∶(0.60±0.12) by means of the recoil-into-gas (helium) integral perturbed angular correlation technique. The studied states were populated by the reactions51V(16O,p2n)64Zn atE0=51 MeV and55Mn(14N,2pn)66Zn atEN=54 MeV.')

        with self.subTest('Record type is non dataclass'):
            results = base_arrange_act_test_articles(TestArticleNonDataClass)
            self.assertEqual(len(results), 3)
            self.assertEqual(results[0].title, 'Magnetic moment measurement of 108 keV level in151Gd')
            self.assertEqual(results[0].abstract, 'AbstractThe magnetic momentμ=−(1.23±0.17)μN of the first excited state in151Gd was determined by integral perturbed angular correlation (IPAC) in external magnetic field.')
            self.assertEqual(results[2].title, 'Magnetic moment measurements in64Zn and66Zn')
            self.assertEqual(results[2].abstract, 'AbstractThe ratios of the ∥g∥-factors of the 7−, 4.635 MeV level in64Zn and 6−, 4.074 MeV and 7−, 4.250 MeV levels in66Zn has been found to be (1±0.18)∶(0.64±0.14)∶(0.60±0.12) by means of the recoil-into-gas (helium) integral perturbed angular correlation technique. The studied states were populated by the reactions51V(16O,p2n)64Zn atE0=51 MeV and55Mn(14N,2pn)66Zn atEN=54 MeV.')


        with self.subTest('Record type is not provided'):
            results = base_arrange_act_test_articles(None)
            self.assertEqual(len(results), 3)
            self.assertEqual(results[0]['title'], 'Magnetic moment measurement of 108 keV level in151Gd')
            self.assertEqual(results[0]['abstract'], 'AbstractThe magnetic momentμ=−(1.23±0.17)μN of the first excited state in151Gd was determined by integral perturbed angular correlation (IPAC) in external magnetic field.')
            self.assertEqual(results[0]['publicationName'], 'Zeitschrift für Physik A Atoms and Nuclei')
            self.assertEqual(results[2]['title'], 'Magnetic moment measurements in64Zn and66Zn')
            self.assertEqual(results[2]['abstract'], 'AbstractThe ratios of the ∥g∥-factors of the 7−, 4.635 MeV level in64Zn and 6−, 4.074 MeV and 7−, 4.250 MeV levels in66Zn has been found to be (1±0.18)∶(0.64±0.14)∶(0.60±0.12) by means of the recoil-into-gas (helium) integral perturbed angular correlation technique. The studied states were populated by the reactions51V(16O,p2n)64Zn atE0=51 MeV and55Mn(14N,2pn)66Zn atEN=54 MeV.')
            self.assertEqual(results[2]['publicationName'], 'Zeitschrift für Physik A Atoms and Nuclei')

    def test_articles(self):
        T = TypeVar('T')
        def base_arrange_act_test_articles(recordType: Type[T]) -> List[T]:
            settings = MetadataAPISettigs()
            settings.api_key = api_key
            settings.page_size = 10

            component = MetadataAPIAccess(settings)

            query = AND(AND(CONTAINS(ContainsField.NAME,'Bădică'),SORT(SortField.SEQUENCE)),EQ(EqualsField.PUBLICATION,'Zeitschrift für Physik A Atoms and Nuclei'))

            if recordType is not None:
                return component.articles(query, recordType)
            else:
                return component.articles(query)

        with self.subTest('Record type is dataclass'):
            results = base_arrange_act_test_articles(TestArticleDataClass)
            self.assertEqual(len(results), 3)
            self.assertEqual(results[0].title, 'Magnetic moment measurement of 108 keV level in151Gd')
            self.assertEqual(results[0].abstract, 'AbstractThe magnetic momentμ=−(1.23±0.17)μN of the first excited state in151Gd was determined by integral perturbed angular correlation (IPAC) in external magnetic field.')
            self.assertEqual(results[2].title, 'Magnetic moment measurements in64Zn and66Zn')
            self.assertEqual(results[2].abstract, 'AbstractThe ratios of the ∥g∥-factors of the 7−, 4.635 MeV level in64Zn and 6−, 4.074 MeV and 7−, 4.250 MeV levels in66Zn has been found to be (1±0.18)∶(0.64±0.14)∶(0.60±0.12) by means of the recoil-into-gas (helium) integral perturbed angular correlation technique. The studied states were populated by the reactions51V(16O,p2n)64Zn atE0=51 MeV and55Mn(14N,2pn)66Zn atEN=54 MeV.')

        with self.subTest('Record type is non dataclass'):
            results = base_arrange_act_test_articles(TestArticleNonDataClass)
            self.assertEqual(len(results), 3)
            self.assertEqual(results[0].title, 'Magnetic moment measurement of 108 keV level in151Gd')
            self.assertEqual(results[0].abstract, 'AbstractThe magnetic momentμ=−(1.23±0.17)μN of the first excited state in151Gd was determined by integral perturbed angular correlation (IPAC) in external magnetic field.')
            self.assertEqual(results[2].title, 'Magnetic moment measurements in64Zn and66Zn')
            self.assertEqual(results[2].abstract, 'AbstractThe ratios of the ∥g∥-factors of the 7−, 4.635 MeV level in64Zn and 6−, 4.074 MeV and 7−, 4.250 MeV levels in66Zn has been found to be (1±0.18)∶(0.64±0.14)∶(0.60±0.12) by means of the recoil-into-gas (helium) integral perturbed angular correlation technique. The studied states were populated by the reactions51V(16O,p2n)64Zn atE0=51 MeV and55Mn(14N,2pn)66Zn atEN=54 MeV.')


        with self.subTest('Record type is not provided'):
            results = base_arrange_act_test_articles(None)
            self.assertEqual(len(results), 3)
            self.assertEqual(results[0]['title'], 'Magnetic moment measurement of 108 keV level in151Gd')
            self.assertEqual(results[0]['abstract'], 'AbstractThe magnetic momentμ=−(1.23±0.17)μN of the first excited state in151Gd was determined by integral perturbed angular correlation (IPAC) in external magnetic field.')
            self.assertEqual(results[0]['publicationName'], 'Zeitschrift für Physik A Atoms and Nuclei')
            self.assertEqual(results[2]['title'], 'Magnetic moment measurements in64Zn and66Zn')
            self.assertEqual(results[2]['abstract'], 'AbstractThe ratios of the ∥g∥-factors of the 7−, 4.635 MeV level in64Zn and 6−, 4.074 MeV and 7−, 4.250 MeV levels in66Zn has been found to be (1±0.18)∶(0.64±0.14)∶(0.60±0.12) by means of the recoil-into-gas (helium) integral perturbed angular correlation technique. The studied states were populated by the reactions51V(16O,p2n)64Zn atE0=51 MeV and55Mn(14N,2pn)66Zn atEN=54 MeV.')
            self.assertEqual(results[2]['publicationName'], 'Zeitschrift für Physik A Atoms and Nuclei')

    def test_article(self):
        T = TypeVar('T')
        def base_arrange_act_test_article(recordType: Type[T]) -> T:
            settings = MetadataAPISettigs()
            settings.api_key = api_key
            settings.page_size = 10

            component = MetadataAPIAccess(settings)

            doi = '10.1007/978-3-540-74930-1_26'

            if recordType is not None:
                return component.article(doi, recordType)
            else:
                return component.article(doi)

        with self.subTest('Record type is dataclass'):
            result = base_arrange_act_test_article(TestArticleDataClass)
            self.assertEqual(result.title, 'Semantic Web and Rule Reasoning inside of E-Learning Systems')
            self.assertEqual(result.abstract, 'SummaryThis paper describes how the Semantic Web and the JenaRules can work together in order to empower e-Learning platform Moodle with rich reports and flexible courses management. We discuss aspects of using Semantic Web technologies in e-learning in general and the JenaRules in particular. The main focus is towards using rules for reasoning on top of existing Moodle content.')
            self.assertEqual(result.publication_date, '2008-01-01')

        with self.subTest('Record type is non dataclass'):
            result = base_arrange_act_test_article(TestArticleNonDataClass)
            self.assertEqual(result.title, 'Semantic Web and Rule Reasoning inside of E-Learning Systems')
            self.assertEqual(result.abstract, 'SummaryThis paper describes how the Semantic Web and the JenaRules can work together in order to empower e-Learning platform Moodle with rich reports and flexible courses management. We discuss aspects of using Semantic Web technologies in e-learning in general and the JenaRules in particular. The main focus is towards using rules for reasoning on top of existing Moodle content.')
            self.assertEqual(result.publication_date, '2008-01-01')

        with self.subTest('Record type is not provided'):
            result = base_arrange_act_test_article(None)
            self.assertEqual(result['title'], 'Semantic Web and Rule Reasoning inside of E-Learning Systems')
            self.assertEqual(result['abstract'], 'SummaryThis paper describes how the Semantic Web and the JenaRules can work together in order to empower e-Learning platform Moodle with rich reports and flexible courses management. We discuss aspects of using Semantic Web technologies in e-learning in general and the JenaRules in particular. The main focus is towards using rules for reasoning on top of existing Moodle content.')
            self.assertEqual(result['publicationDate'], '2008-01-01')
            self.assertEqual(result['publicationName'], 'Advances in Intelligent and Distributed Computing')
