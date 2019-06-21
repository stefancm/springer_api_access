from unittest import TestCase
from springer_metadata_api_access.constraints import *


class TestConstraints(TestCase):
    def test_Constraint_Atomic_Logical_cannot_be_instantiated(self):
        with self.assertRaises(TypeError):
            Constraint()

        with self.assertRaises(TypeError):
            Atomic()

        with self.assertRaises(TypeError):
            Logical()