import unittest

from entities.trader import Trader
from items.item import Item


class TestItem(Item):
    def __init__(self, name, description="desc", buyable=True, sell_price=10):
        super().__init__(name, description, buyable, sell_price)


class TestTraderItemAssociations(unittest.TestCase):

    def setUp(self):
        self.item1 = TestItem("Item1")
        self.item2 = TestItem("Item2")

        self.drop_item = TestItem("Drop")

        self.trader = Trader(
            drop=self.drop_item,
            trader_type="weapons",
            sale=True,
            name="Bob",
            current_health=30
        )

    def test_add_item_sets_reverse_association(self):
        self.trader.add_item_to_stock(self.item1)
        self.assertIn(self.item1, self.trader.get_stock())
        self.assertIn(self.trader, self.item1.get_traders())

    def test_remove_item_clears_reverse_association(self):
        self.trader.add_item_to_stock(self.item1)
        self.trader.remove_item_from_stock(self.item1)

        self.assertNotIn(self.item1, self.trader.get_stock())
        self.assertNotIn(self.trader, self.item1.get_traders())

    def test_add_item_not_duplicated(self):
        self.trader.add_item_to_stock(self.item1)
        self.trader.add_item_to_stock(self.item1)
        self.assertEqual(self.trader.get_stock().count(self.item1), 1)
        self.assertEqual(self.item1.get_traders().count(self.trader), 1)

    def test_clear_stock_updates_reverse_associations(self):
        self.trader.add_item_to_stock(self.item1)
        self.trader.add_item_to_stock(self.item2)

        self.trader.clear_stock()

        self.assertEqual(len(self.trader.get_stock()), 0)
        self.assertNotIn(self.trader, self.item1.get_traders())
        self.assertNotIn(self.trader, self.item2.get_traders())
