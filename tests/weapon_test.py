import unittest

from items.weapon import Weapon


class WeaponTest(unittest.TestCase):

    def test_valid_weapon(self):
        w = Weapon("Axe", "Heavy weapon", True, 80, 12, "axe")
        self.assertEqual(w.damage, 12)
        self.assertEqual(w.type, "axe")

    def test_invalid_damage(self):
        with self.assertRaises(TypeError):
            Weapon("Sword", "desc", True, 80, "strong", "sword")

    def test_invalid_type(self):
        with self.assertRaises(TypeError):
            Weapon("Sword", "desc", True, 80, 10, 123)
        with self.assertRaises(ValueError):
            Weapon("Sword", "desc", True, 80, 10, "gun")
        with self.assertRaises(ValueError):
            Weapon("Sword", "desc", True, 80, 10, "   ")