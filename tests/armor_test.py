import unittest

from items.armor import Armor


class ArmorTest(unittest.TestCase):

    def test_valid_armor(self):
        armor = Armor(10, "Steel Armor", "Tough", True, 200)
        self.assertEqual(armor.toughness, 10)

    def test_invalid_toughness(self):
        with self.assertRaises(TypeError):
            Armor("hard", "Armor", "desc", True, 100)
        with self.assertRaises(ValueError):
            Armor(0, "Armor", "desc", True, 100)