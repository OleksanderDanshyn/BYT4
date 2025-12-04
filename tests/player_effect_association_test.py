import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from effect import Effect
from items.potion import Potion
from entities.player import Player


class TestPlayerEffectAssociation(unittest.TestCase):

    def setUp(self):
        self.effect = Effect("Strength", "Boosts attack")
        self.potion = Potion(
            name="Heal",
            description="Restores health",
            buyable=True,
            sell_price=10,
            number_of_uses=1,
            duration=5,
            power=3,
            effect=self.effect
        )
        self.player = Player("Hero", current_health=5, money=100)

    def test_player_apply_effect_creates_association(self):
        self.player.apply_effect(self.effect, self.potion)

        self.assertIn(self.effect, self.player.active_effects)
        data = self.player.active_effects[self.effect]

        self.assertEqual(data["potion"], self.potion)
        self.assertEqual(data["duration"], self.potion.duration)
        self.assertIsInstance(data["start_time"], datetime)

    def test_player_apply_effect_rejects_invalid_effect(self):
        with self.assertRaises(TypeError):
            self.player.apply_effect("invalid", self.potion)

    def test_player_apply_effect_rejects_invalid_potion(self):
        with self.assertRaises(TypeError):
            self.player.apply_effect(self.effect, "invalid")

    def test_remove_effect(self):
        self.player.apply_effect(self.effect, self.potion)
        self.player.remove_effect(self.effect)

        self.assertNotIn(self.effect, self.player.active_effects)

    def test_remove_effect_if_not_applied(self):
        self.player.remove_effect(self.effect)

    def test_effect_expires_correctly(self):
        self.player.apply_effect(self.effect, self.potion)

        fake_start = datetime.now() - timedelta(seconds=100)
        self.player.active_effects[self.effect]["start_time"] = fake_start

        self.assertTrue(self.player.is_effect_expired(self.effect))

    def test_remove_expired_effects(self):
        self.player.apply_effect(self.effect, self.potion)

        self.player.active_effects[self.effect]["start_time"] = datetime.now() - timedelta(seconds=10)

        self.player.remove_expired_effects()

        self.assertNotIn(self.effect, self.player.active_effects)
