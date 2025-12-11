import unittest

from activity import Activity
from effect import Effect


class TestActivityEffectAssociations(unittest.TestCase):

    def setUp(self):
        self.effect = Effect("Calm", "Reduces stress")
        self.activity = Activity(
            name="Relax",
            description="Calms you down",
            effect=self.effect,
            effect_duration=4
        )

    def test_activity_links_to_effect(self):
        self.assertIs(self.activity.effect, self.effect)
        self.assertIn(self.activity, self.effect.activities)

    def test_change_effect_updates_reverse_side(self):
        new_effect = Effect("Focus", "Boosts concentration")
        self.activity.effect = new_effect

        self.assertIs(self.activity.effect, new_effect)
        self.assertIn(self.activity, new_effect.activities)
        self.assertNotIn(self.activity, self.effect.activities)

    def test_unset_effect(self):
        self.activity.effect = None

        self.assertIsNone(self.activity.effect)
        self.assertEqual(len(self.effect.activities), 0)

    def test_set_invalid_type(self):
        with self.assertRaises(TypeError):
            self.activity.effect = "invalid"

    def test_effect_delete_clears_activity(self):
        self.effect.delete()

        self.assertIsNone(self.activity.effect)
        self.assertNotIn(self.activity, self.effect.activities)

    def test_activity_delete_clears_effect_relation(self):
        self.activity.delete()

        self.assertNotIn(self.activity, self.effect.activities)
