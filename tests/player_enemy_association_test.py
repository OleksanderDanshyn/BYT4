import unittest

from entities.player import Player
from entities.enemy import Enemy
from items.item import Item


class TestItem(Item):
    def __init__(self, name, description="desc", buyable=True, sell_price=10):
        super().__init__(name, description, buyable, sell_price)


class TestPlayerEnemyAssociation(unittest.TestCase):

    def setUp(self):
        self.player1 = Player("Hero", current_health=10, money=50)
        self.player2 = Player("Rogue", current_health=9, money=30)
        self.enemy1 = Enemy(drop=TestItem("Dummy", "Dummy"), name="Goblin", current_health=5, damage=2)
        self.enemy2 = Enemy(drop=TestItem("Dummy", "Dummy"), name="Orc", current_health=12, damage=4)

    def test_player_can_slay_enemy(self):
        self.player1.slay_monster(self.enemy1)

        self.assertIn(self.enemy1, self.player1.kills)
        self.assertEqual(len(self.player1.kills), 1)

    def test_multiple_kills(self):
        self.player1.slay_monster(self.enemy1)
        self.player1.slay_monster(self.enemy2)

        self.assertIn(self.enemy1, self.player1.kills)
        self.assertIn(self.enemy2, self.player1.kills)
        self.assertEqual(len(self.player1.kills), 2)

    def test_slay_monster_rejects_invalid_type(self):
        with self.assertRaises(TypeError):
            self.player1.slay_monster("invalid")

    def test_slay_monster_rejects_duplicate_enemy(self):
        self.player1.slay_monster(self.enemy1)
        with self.assertRaises(ValueError):
            self.player1.slay_monster(self.enemy1)

    def test_enemy_records_killer(self):
        self.player1.slay_monster(self.enemy1)
        self.assertIn(self.player1, self.enemy1.killed_by)
        self.assertEqual(len(self.enemy1.killed_by), 1)

    def test_enemy_records_multiple_killers(self):

        self.player1.slay_monster(self.enemy1)
        self.player2.slay_monster(self.enemy1)

        self.assertIn(self.player1, self.enemy1.killed_by)
        self.assertIn(self.player2, self.enemy1.killed_by)
        self.assertEqual(len(self.enemy1.killed_by), 2)

    def test_enemy_does_not_duplicate_killers(self):
        self.player1.slay_monster(self.enemy1)
        self.enemy1.add_killer(self.player1)
        self.assertEqual(self.enemy1.killed_by.count(self.player1), 1)
