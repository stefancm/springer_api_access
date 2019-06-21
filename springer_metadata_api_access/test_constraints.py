from unittest import TestCase
from springer_metadata_api_access.constraints import *


def constraint_text(constraint: Constraint) -> str:
    return constraint._springer_metadata_expression()

class TestConstraints(TestCase):

    def assertConstraintIsEqual(self, constraint: Constraint, expected_springer_query_string: str):
        self.assertEqual(constraint_text(constraint), expected_springer_query_string)

    def test_Constraint_Atomic_Logical_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Constraint()

        with self.assertRaises(TypeError):
            Atomic()

        with self.assertRaises(TypeError):
            Logical()

    def test_equals_constraints(self):
        equals_test_cases = [
            (EqualsField.DOI, '10.1007/978-3-319-07410-8_4', 'doi:10.1007/978-3-319-07410-8_4'),
            (EqualsField.SUBJECT, 'Chemistry', 'subject:Chemistry'),
            (EqualsField.TOPICAL_COLLECTION, '"Scleroderma"', 'topicalcollection:"Scleroderma"'),
            (EqualsField.COUNTRY, '"New Zeeland"', 'country:"New Zeeland"')
        ]

        for  field, value, expected in equals_test_cases:
            with self.subTest(field=field, field_value = value, expected_expression = expected):
                self.assertEqual(expected, constraint_text(EQ(field, value)))

    def test_flags(self):
        flags_test_cases = [
            (Flag.OPEN_ACCESS, 'openaccess:true'),
            (Flag.JOURNAL_ONLINE_FIRST, 'journalonlinefirst:true')
        ]

        for  flag, expected in flags_test_cases:
            with self.subTest(flag=flag, expected_expression = expected):
                self.assertEqual(expected, constraint_text(flag))

    def test_equals_when_value_has_spaces_it_is_enquoted_automatically(self):
        self.assertConstraintIsEqual(EQ(EqualsField.SUBJECT, 'quantic kidology'), 'subject:"quantic kidology"')

    def test_contains_when_value_has_spaces_it_is_enquoted_automatically(self):
        self.assertConstraintIsEqual(CONTAINS(ContainsField.BOOK, 'kidology treaty'), 'book:"kidology treaty"')

    def test_expression_does_not_accept_anything_but_logical_contained(self):
        with self.subTest('contains'), self.assertRaises(AssertionError):
            EXPR(CONTAINS(ContainsField.BOOK, 'somevalue'))
        with self.subTest('equals'), self.assertRaises(AssertionError):
            EXPR(EQ(EqualsField.SUBJECT, 'somevalue'))
        with self.subTest('sort'), self.assertRaises(AssertionError):
            EXPR(SORT(SortField.SEQUENCE))

    def test_field_type_mismatch(self):
        from enum import Enum
        class TestEnum(Enum):
            BOOK = 'book'
            SUBJECT = 'subject'
            SEQUENCE = 'sequence'

        with self.subTest('contains'), self.assertRaises(AssertionError):
            CONTAINS(TestEnum.BOOK, 'somevalue')

        with self.subTest('subject'), self.assertRaises(AssertionError):
            EQ(TestEnum.SUBJECT, 'somevalue')

        with self.subTest('sequence'), self.assertRaises(AssertionError):
            SORT(TestEnum.SEQUENCE)

    def test_complex_expression_1(self):
        expr = AND(CONTAINS(ContainsField.BOOK, 'tinfoil materials science'), EQ(EqualsField.YEAR, 2012))

        self.assertConstraintIsEqual(expr, 'book:"tinfoil materials science" and year:2012')

    def test_complex_expression_2(self):
        expr = AND(EXPR(OR(EXPR(AND(CONTAINS(ContainsField.BOOK, 'tinfoil materials science'), EQ(EqualsField.YEAR, 2012))), EQ(EqualsField.SUBJECT, 'study on tinfoil materials science'))),Flag.OPEN_ACCESS)

        self.assertConstraintIsEqual(expr, '((book:"tinfoil materials science" and year:2012) or subject:"study on tinfoil materials science") and openaccess:true')