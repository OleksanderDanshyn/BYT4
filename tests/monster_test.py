import unittest
from entities.monster import Monster

class MonsterTest(unittest.TestCase):
    def test_valid_monster(self):
        m = Monster("fangs", is_boss=True, resistance="fire", name="Dragon", current_health=300)
        self.assertTrue(m.is_boss)
        self.assertEqual(m.name, "Dragon")

    def test_invalid_is_boss(self):
        with self.assertRaises(TypeError):
            Monster("claws", "yes", "ice", "Wolf", 200)
