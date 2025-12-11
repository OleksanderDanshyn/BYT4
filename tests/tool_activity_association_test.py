import unittest

from activity import Activity
from items.tool import Tool
from effect import Effect
from entities.player import Player


class TestToolActivityAssociations(unittest.TestCase):

    def setUp(self):
        self.activity = Activity("Chop Wood", "Chop some logs")
        self.tool = Tool(
            name="Axe",
            description="A sharp axe",
            buyable=True,
            sell_price=15,
            durability=5,
            activity=self.activity
        )
        self.player = Player("Hero", 10, 100)

    def test_tool_links_to_activity(self):
        self.assertIs(self.tool.activity, self.activity)
        self.assertIn(self.tool, self.activity.tools)

    def test_change_activity_updates_reverse_links(self):
        new_activity = Activity("Dig", "Dig dirt")
        self.tool.activity = new_activity

        self.assertIs(self.tool.activity, new_activity)
        self.assertIn(self.tool, new_activity.tools)
        self.assertNotIn(self.tool, self.activity.tools)

    def test_unset_activity(self):
        self.tool.activity = None

        self.assertIsNone(self.tool.activity)
        self.assertEqual(len(self.activity.tools), 0)

    def test_set_invalid_activity_type(self):
        with self.assertRaises(TypeError):
            self.tool.activity = "invalid"

    def test_activity_delete_clears_tool_links(self):
        self.activity.delete()
        self.assertIsNone(self.tool.activity)

    def test_tool_perform_calls_activity(self):
        result = self.tool.perform_activity(self.player, 1)
        self.assertIn("Performed Chop Wood.", result)

    def test_tool_incompatible_activity(self):
        new_activity = Activity("Fish", "Catch fish")
        incompatible_tool = Tool("Shovel", "Dig stuff", True, 10, 5, activity=new_activity)

        with self.assertRaises(ValueError):
            self.activity.perform(self.player, current_turn=1, tool=incompatible_tool)
