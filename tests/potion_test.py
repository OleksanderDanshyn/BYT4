import unittest

from items.potion import Potion


class PotionTest(unittest.TestCase):

    def test_valid_potion(self):
        p = Potion("Healing Potion", "Heals HP", True, 50, 1, 10, 5)
        self.assertEqual(p.duration, 10)
        self.assertEqual(p.power, 5)

    def test_invalid_duration_or_power(self):
        with self.assertRaises(TypeError):
            Potion("Potion", "desc", True, 50, 1, "long", 5)
        with self.assertRaises(ValueError):
            Potion("Potion", "desc", True, 50, 1, -5, 5)
        with self.assertRaises(TypeError):
            Potion("Potion", "desc", True, 50, 1, 10, "strong")
        with self.assertRaises(ValueError):
            Potion("Potion", "desc", True, 50, 1, 10, -5)