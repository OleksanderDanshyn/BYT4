import unittest
from entities.player import Player
from entities.enemy import Enemy
from effect import Effect
from items.weapon import Weapon
from items.armor import Armor

class DummyEffect(Effect):
    def __init__(self):
        super().__init__("Blessing", "Increases strength temporarily")

class DummyWeapon(Weapon):
    def __init__(self):
        super().__init__("Sword", "Sharp blade", True, 50, 10, "sword")

class DummyArmor(Armor):
    def __init__(self):
        super().__init__(5, "Armor", "Strong", True, 100)

class DummyEnemy(Enemy):
    def __init__(self):
        super().__init__("drop", "Orc", 50, 5)

class PlayerTest(unittest.TestCase):
    def test_valid_player(self):
        p = Player("Knight", 100, 500)
        self.assertEqual(p.name, "Knight")
        self.assertEqual(p.money, 500)

    def test_invalid_money_type(self):
        with self.assertRaises(TypeError):
            Player("Knight", 100, "a lot")

    def test_apply_effect(self):
        p = Player("Mage", 100, 100)
        effect = DummyEffect()
        p.apply_effect(effect)
        self.assertIn(effect, p.effects)

    def test_equip_weapon(self):
        p = Player("Archer", 100, 50)
        w = DummyWeapon()
        p.equip_weapon(w)
        self.assertEqual(p.equipped_weapon, w)

    def test_equip_armor(self):
        p = Player("Warrior", 100, 50)
        a = DummyArmor()
        p.equip_armor(a)
        self.assertEqual(p.equipped_armor, a)

    def test_slay_monster(self):
        p = Player("Knight", 100, 50)
        e = DummyEnemy()
        p.slay_monster(e)
        self.assertIn(e, p.kills)
