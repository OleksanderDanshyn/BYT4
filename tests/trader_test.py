import unittest
from entities.trader import Trader

class TraderTest(unittest.TestCase):
    def test_valid_trader(self):
        t = Trader("loot", "armor", True, "Borin", 100)
        self.assertEqual(t.type, "armor")
        self.assertTrue(t.sale)

    def test_invalid_type_not_string(self):
        with self.assertRaises(TypeError):
            Trader("loot", 123, True, "Borin", 100)

    def test_invalid_type_value(self):
        with self.assertRaises(ValueError):
            Trader("loot", "furniture", True, "Borin", 100)

    def test_invalid_sale_type(self):
        with self.assertRaises(TypeError):
            Trader("loot", "armor", "yes", "Borin", 100)
