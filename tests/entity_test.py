import unittest
from entities.entity import Entity

class EntityTest(unittest.TestCase):
    def test_valid_entity(self):
        e = Entity("Hero", 100)
        self.assertEqual(e.name, "Hero")
        self.assertEqual(e.health, 100)

    def test_invalid_name_type(self):
        with self.assertRaises(TypeError):
            Entity(123, 100)

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            Entity("   ", 100)

    def test_too_long_name(self):
        with self.assertRaises(ValueError):
            Entity("X" * 31, 100)

    def test_negative_health(self):
        with self.assertRaises(ValueError):
            Entity("Hero", -10)

    def test_non_numeric_health(self):
        with self.assertRaises(TypeError):
            Entity("Hero", "a lot")
