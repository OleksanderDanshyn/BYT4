import unittest

from entities.friendly import Friendly
from items.food import Food


class FriendlyTest(unittest.TestCase):
    def test_valid_friendly(self):
        apple = Food(5, "Apple", "A red apple", True, 10, 1)
        f = Friendly(apple, "Ally", 40, True, 75)
        self.assertEqual(f.tameable, True)
        self.assertEqual(f.reputation, 75)

    def test_invalid_tameable_type(self):
        apple = Food(5, "Apple", "A red apple", True, 10, 1)
        with self.assertRaises(TypeError):
            Friendly(apple, "Ally", 40, "yes", 75)

    def test_invalid_reputation_type(self):
        apple = Food(5, "Apple", "A red apple", True, 10, 1)
        with self.assertRaises(TypeError):
            Friendly(apple, "Ally", 40, True, "high")

    def test_reputation_out_of_bounds(self):
        apple = Food(5, "Apple", "A red apple", True, 10, 1)
        with self.assertRaises(ValueError):
            Friendly(apple, "Ally", 40, True, 150)
