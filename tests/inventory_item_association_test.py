import unittest

from entities.player import Player
from items.inventory import Inventory
from items.item import Item


class TestItem(Item):
    def __init__(self, name, description="desc", buyable=True, sell_price=10):
        super().__init__(name, description, buyable, sell_price)


class TestInventoryItemAssociation(unittest.TestCase):

    def setUp(self):
        self.player = Player("Hero", current_health=10, money=100)
        self.inventory = self.player.inventory

        self.item1 = TestItem("Sword", "Sharp sword", True, 10)
        self.item2 = TestItem("Shield", "Tough shield", True, 15)

    def test_add_item_success(self):
        result, msg = self.inventory.add_item(self.item1)

        self.assertTrue(result)
        self.assertIn("added successfully", msg)
        self.assertIn(self.item1.name, self.inventory.items)
        self.assertIs(self.inventory.items[self.item1.name], self.item1)

    def test_add_item_rejects_none(self):
        with self.assertRaises(ValueError):
            self.inventory.add_item(None)

    def test_add_item_rejects_duplicate(self):
        self.inventory.add_item(self.item1)
        with self.assertRaises(ValueError):
            self.inventory.add_item(self.item1)

    def test_add_item_respects_max_size(self):
        inv = Inventory(owner=self.player, max_size=1)
        inv.add_item(self.item1)

        with self.assertRaises(OverflowError):
            inv.add_item(self.item2)

    def test_remove_item_by_object(self):
        self.inventory.add_item(self.item1)
        result, msg = self.inventory.remove_item(self.item1)

        self.assertTrue(result)
        self.assertIn("removed successfully", msg)
        self.assertNotIn(self.item1.name, self.inventory.items)

    def test_remove_item_by_name(self):
        self.inventory.add_item(self.item1)
        self.inventory.remove_item("Sword")

        self.assertNotIn("Sword", self.inventory.items)

    def test_remove_item_not_found(self):
        with self.assertRaises(ValueError):
            self.inventory.remove_item("missing")

    def test_get_item_returns_correct_object(self):
        self.inventory.add_item(self.item1)
        item = self.inventory.get_item("Sword")
        self.assertIs(item, self.item1)

    def test_get_item_not_found_returns_none(self):
        self.assertIsNone(self.inventory.get_item("missing"))

    def test_inventory_length(self):
        self.assertEqual(len(self.inventory), 0)
        self.inventory.add_item(self.item1)
        self.assertEqual(len(self.inventory), 1)

    def test_inventory_is_empty(self):
        self.assertTrue(self.inventory.is_empty())
        self.inventory.add_item(self.item1)
        self.assertFalse(self.inventory.is_empty())

    def test_add_item_sets_reverse_inventory_reference(self):
        self.inventory.add_item(self.item1)
        self.assertIs(self.item1.inventory, self.inventory)

    def test_remove_item_clears_reverse_inventory_reference(self):
        self.inventory.add_item(self.item1)
        self.inventory.remove_item(self.item1)
        self.assertIsNone(self.item1.inventory)

    def test_inventory_does_not_duplicate_reverse_references_on_readding(self):
        self.inventory.add_item(self.item1)
        self.inventory.remove_item(self.item1)
        self.inventory.add_item(self.item1)

        self.assertIs(self.item1.inventory, self.inventory)
        self.assertEqual(len(self.inventory.items), 1)
