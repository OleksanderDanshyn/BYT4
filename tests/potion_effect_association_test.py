import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

from effect import Effect
from items.potion import Potion


class TestPotionEffectAssociations(unittest.TestCase):

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

    def test_potion_has_effect_reference(self):
        self.assertIs(self.potion.effect, self.effect)
