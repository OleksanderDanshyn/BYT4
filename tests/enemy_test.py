import unittest
from entities.enemy import Enemy

class EnemyTest(unittest.TestCase):
    def test_valid_enemy(self):
        e = Enemy(drop="loot", name="Goblin", current_health=30, damage=5)
        self.assertEqual(e.damage, 5)
        self.assertEqual(e.name, "Goblin")

    def test_invalid_damage_type(self):
        with self.assertRaises(TypeError):
            Enemy("gold", "Goblin", 30, "strong")
