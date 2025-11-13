import unittest

from items.food import Food


class FoodTest(unittest.TestCase):

    def test_valid_food(self):
        f = Food(5, "Bread", "Tasty food", True, 10, 2)
        self.assertEqual(f.saturation, 5)

    def test_invalid_food(self):
        with self.assertRaises(TypeError):
            Food("five", "Bread", "desc", True, 10, 2)
        with self.assertRaises(ValueError):
            Food(-5, "Bread", "desc", True, 10, 2)