import unittest

from entities.trader import Trader
from items.armor import Armor


class TraderTest(unittest.TestCase):
    def test_valid_trader(self):
        armor = Armor(5, "Leather Armor", "Basic protection", True, 50)
        t = Trader(armor, "armor", True, "Borin", 100)
        self.assertEqual(t.type, "armor")
        self.assertTrue(t.sale)

    def test_invalid_type_not_string(self):
        armor = Armor(5, "Leather Armor", "Basic protection", True, 50)
        with self.assertRaises(TypeError):
            Trader(armor, 123, True, "Borin", 100)

    def test_invalid_type_value(self):
        armor = Armor(5, "Leather Armor", "Basic protection", True, 50)
        with self.assertRaises(ValueError):
            Trader(armor, "furniture", True, "Borin", 100)

    def test_invalid_sale_type(self):
        armor = Armor(5, "Leather Armor", "Basic protection", True, 50)
        with self.assertRaises(TypeError):
            Trader(armor, "armor", "yes", "Borin", 100)
