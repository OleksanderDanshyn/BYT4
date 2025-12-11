import unittest

from entities.player import Player
from effect import Effect
from items.potion import Potion
from activity import Activity
from playereffect import PlayerEffect


class TestPlayerEffectAssociations(unittest.TestCase):

    def setUp(self):
        self.player = Player("Hero", current_health=10, money=100)
        self.effect = Effect("Strength", "Increase power")

        self.potion = Potion(
            name="Strength Potion",
            description="Buff",
            buyable=True,
            sell_price=10,
            number_of_uses=1,
            duration=3,
            power=0,
            effect=self.effect
        )

        self.activity = Activity(
            name="Meditate",
            description="Focus",
            effect=self.effect,
            effect_duration=5
        )

    def test_apply_effect_from_potion(self):
        self.player.apply_effect(self.effect, self.potion, current_turn=1)

        self.assertEqual(len(self.player.active_effects), 1)
        pe = self.player.active_effects[0]

        self.assertIs(pe.effect, self.effect)
        self.assertIs(pe.source, self.potion)
        self.assertEqual(pe.source_type, "potion")
        self.assertEqual(pe.start_turn, 1)

    def test_apply_effect_from_activity(self):
        self.player.apply_effect_from_activity(self.effect, self.activity, current_turn=2)

        self.assertEqual(len(self.player.active_effects), 1)
        pe = self.player.active_effects[0]

        self.assertIs(pe.effect, self.effect)
        self.assertIs(pe.source, self.activity)
        self.assertEqual(pe.source_type, "activity")
        self.assertEqual(pe.start_turn, 2)

    def test_apply_effect_invalid_types(self):
        with self.assertRaises(TypeError):
            self.player.apply_effect("bad", self.potion, 1)

        with self.assertRaises(TypeError):
            self.player.apply_effect(self.effect, "bad", 1)

    def test_effect_expires_after_duration(self):
        self.player.apply_effect(self.effect, self.potion, current_turn=1)

        self.player.remove_expired_effects(current_turn=4)

        self.assertEqual(len(self.player.active_effects), 0)

    def test_has_effect(self):
        self.player.apply_effect(self.effect, self.potion, current_turn=1)
        self.assertTrue(self.player.has_effect(self.effect, 2))
        self.assertFalse(self.player.has_effect(self.effect, 10))

    def test_get_effect_by_type(self):
        self.player.apply_effect(self.effect, self.potion, current_turn=1)
        pe = self.player.get_effect_by_type(self.effect, 2)
        self.assertIsInstance(pe, PlayerEffect)

    def test_get_active_effect_names(self):
        self.player.apply_effect(self.effect, self.potion, current_turn=1)
        names = self.player.get_active_effect_names(current_turn=2)

        self.assertEqual(len(names), 1)
        self.assertIn("Strength (2 turns remaining)", names[0])
