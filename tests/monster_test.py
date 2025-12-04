import unittest

from entities.monster import Monster
from items.weapon import Weapon


class MonsterTest(unittest.TestCase):
    def test_valid_monster(self):
        weapon = Weapon("Fangs", "Sharp fangs", True, 100, 20, "sword")
        m = Monster(weapon, is_boss=True, resistance=False, name="Dragon", current_health=300)
        self.assertTrue(m.is_boss)
        self.assertEqual(m.name, "Dragon")

    def test_invalid_is_boss(self):
        weapon = Weapon("Claws", "Sharp claws", True, 50, 15, "sword")
        with self.assertRaises(TypeError):
            Monster(weapon, "yes", True, "Wolf", 200)
