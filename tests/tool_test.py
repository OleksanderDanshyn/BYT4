import unittest

from items.tool import Tool


class ToolTest(unittest.TestCase):

    def test_valid_tool(self):
        t = Tool("Pickaxe", "Mine rocks", True, 25, "Mining")
        self.assertEqual(t.ability, "Mining")

    def test_invalid_tool_ability(self):
        with self.assertRaises(ValueError):
            Tool("Pickaxe", "desc", True, 25, "   ")