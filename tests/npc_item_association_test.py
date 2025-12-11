import unittest

from entities.npc import NPC
from items.item import Item


class TestItem(Item):
    def __init__(self, name, description="desc", buyable=True, sell_price=10):
        super().__init__(name, description, buyable, sell_price)


class TestNPCItemAssociations(unittest.TestCase):

    def setUp(self):
        self.item1 = TestItem("Drop1")
        self.item2 = TestItem("Drop2")
        self.npc = NPC(drop=self.item1, name="Goblin", current_health=10)

    def test_npc_has_drop_reference(self):
        self.assertIs(self.npc.drop, self.item1)

    def test_item_holds_npc_reference(self):
        self.assertIn(self.npc, self.item1.get_holders())
        self.assertEqual(len(self.item1.get_holders()), 1)

    def test_reassign_drop_updates_reverse_association(self):
        self.npc.drop = self.item2

        self.assertIs(self.npc.drop, self.item2)
        self.assertNotIn(self.npc, self.item1.get_holders())
        self.assertIn(self.npc, self.item2.get_holders())

    def test_drop_not_duplicated(self):
        self.npc.drop = self.item1
        self.npc.drop = self.item1
        self.assertEqual(self.item1.get_holders().count(self.npc), 1)
