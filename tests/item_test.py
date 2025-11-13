import unittest

from items.armor import Armor
from items.item import Item


class ItemTest(unittest.TestCase):

    def test_item_is_abstract(self):
        with self.assertRaises(TypeError):
            Item("Test", "desc", True, 10)

    def test_valid_item_subclass(self):
        armor = Armor(5, "Iron Armor", "Heavy chestplate", True, 100)
        self.assertEqual(armor.name, "Iron Armor")
        self.assertEqual(armor.sell_price, 100)
        self.assertTrue(armor.buyable)
        self.assertEqual(armor.buy_price, 120)

    def test_name_validation(self):
        with self.assertRaises(TypeError):
            Armor(5, 123, "desc", True, 50)
        with self.assertRaises(ValueError):
            Armor(5, "   ", "desc", True, 50)
        with self.assertRaises(ValueError):
            Armor(5, "a" * 31, "desc", True, 50)

    def test_description_validation(self):
        with self.assertRaises(TypeError):
            Armor(5, "Iron", 123, True, 50)
        with self.assertRaises(ValueError):
            Armor(5, "Iron", "   ", True, 50)
        with self.assertRaises(ValueError):
            Armor(5, "Iron", "a" * 51, True, 50)

    def test_buyable_validation(self):
        with self.assertRaises(TypeError):
            Armor(5, "Iron", "desc", "yes", 50)

    def test_sell_price_validation(self):
        with self.assertRaises(TypeError):
            Armor(5, "Iron", "desc", True, "cheap")
        with self.assertRaises(ValueError):
            Armor(5, "Iron", "desc", True, -10)