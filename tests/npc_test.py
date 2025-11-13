import unittest
from entities.npc import NPC

class NPCTest(unittest.TestCase):
    def test_npc_inherits_entity(self):
        n = NPC(drop="gold", name="Villager", current_health=50)
        self.assertEqual(n.drop, "gold")
        self.assertEqual(n.name, "Villager")
        self.assertEqual(n.health, 50)
