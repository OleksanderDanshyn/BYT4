import unittest

from entities.player import Player
from entities.enemy import Enemy


class TestPlayerEnemyAssociation(unittest.TestCase):

    def setUp(self):
        self.player = Player("Hero", current_health=10, money=50)
        self.enemy1 = Enemy(drop=None, name="Goblin", current_health=5, damage=2)
        self.enemy2 = Enemy(drop=None, name="Orc", current_health=12, damage=4)

    def test_player_can_slay_enemy(self):
        self.player.slay_monster(self.enemy1)

        self.assertIn(self.enemy1, self.player.kills)
        self.assertEqual(len(self.player.kills), 1)

    def test_multiple_kills(self):
        self.player.slay_monster(self.enemy1)
        self.player.slay_monster(self.enemy2)

        self.assertIn(self.enemy1, self.player.kills)
        self.assertIn(self.enemy2, self.player.kills)
        self.assertEqual(len(self.player.kills), 2)

    def test_slay_monster_rejects_invalid_type(self):
        with self.assertRaises(TypeError):
            self.player.slay_monster("invalid")

    def test_slay_monster_rejects_duplicate_enemy(self):
        self.player.slay_monster(self.enemy1)
        with self.assertRaises(ValueError):
            self.player.slay_monster(self.enemy1)
