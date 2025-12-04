import unittest

from entities.npc import NPC
from items.food import Food


class NPCTest(unittest.TestCase):
    def test_npc_inherits_entity(self):
        food = Food(5, "Bread", "Fresh bread", True, 10, 1)
        n = NPC(drop=food, name="Villager", current_health=50)
        self.assertEqual(n.drop, food)
        self.assertEqual(n.name, "Villager")
        self.assertEqual(n.health, 50)
