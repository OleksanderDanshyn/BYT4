import unittest

from entities.enemy import Enemy
from items.weapon import Weapon


class EnemyTest(unittest.TestCase):
    def test_valid_enemy(self):
        weapon = Weapon("Sword", "A sharp blade", True, 50, 10, "sword")
        e = Enemy(drop=weapon, name="Goblin", current_health=30, damage=5)
        self.assertEqual(e.damage, 5)
        self.assertEqual(e.name, "Goblin")

    def test_invalid_damage_type(self):
        weapon = Weapon("Sword", "A sharp blade", True, 50, 10, "sword")
        with self.assertRaises(TypeError):
            Enemy(weapon, "Goblin", 30, "strong")
