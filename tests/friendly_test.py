import unittest
from entities.friendly import Friendly

class FriendlyTest(unittest.TestCase):
    def test_valid_friendly(self):
        f = Friendly("apple", "Ally", 40, True, 75)
        self.assertEqual(f.tameable, True)
        self.assertEqual(f.reputation, 75)

    def test_invalid_tameable_type(self):
        with self.assertRaises(TypeError):
            Friendly("item", "Ally", 40, "yes", 75)

    def test_invalid_reputation_type(self):
        with self.assertRaises(TypeError):
            Friendly("item", "Ally", 40, True, "high")

    def test_reputation_out_of_bounds(self):
        with self.assertRaises(ValueError):
            Friendly("item", "Ally", 40, True, 150)
