import unittest

from items.consumanble import Consumable


class ConsumableTest(unittest.TestCase):

    def test_valid_consumable(self):
        c = Consumable(3, "Apple", "Restores hunger", True, 5)
        self.assertEqual(c.number_of_uses, 3)

    def test_invalid_consumable(self):
        with self.assertRaises(TypeError):
            Consumable("three", "Apple", "desc", True, 5)
        with self.assertRaises(ValueError):
            Consumable(0, "Apple", "desc", True, 5)
