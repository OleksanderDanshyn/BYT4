import unittest

from items.item import Item


class TestItem(Item):
    def __init__(self, name, description="desc", buyable=True, sell_price=10):
        super().__init__(name, description, buyable, sell_price)


class TestItemItemAssociations(unittest.TestCase):

    def setUp(self):
        self.base = TestItem("Base")
        self.comp1 = TestItem("Comp1")
        self.comp2 = TestItem("Comp2")

    def test_add_component_sets_reverse_relation(self):
        self.base.add_component(self.comp1)
        self.assertIn(self.comp1, self.base.get_components())
        self.assertIs(self.comp1.get_combined_into(), self.base)

    def test_remove_component_clears_reverse_relation(self):
        self.base.add_component(self.comp1)
        self.base.remove_component(self.comp1)
        self.assertNotIn(self.comp1, self.base.get_components())
        self.assertIsNone(self.comp1.get_combined_into())

    def test_multiple_components(self):
        self.base.add_component(self.comp1)
        self.base.add_component(self.comp2)
        self.assertIn(self.comp1, self.base.get_components())
        self.assertIn(self.comp2, self.base.get_components())
        self.assertEqual(len(self.base.get_components()), 2)

    def test_component_not_duplicated(self):
        self.base.add_component(self.comp1)
        self.base.add_component(self.comp1)
        self.assertEqual(self.base.get_components().count(self.comp1), 1)

    def test_cannot_add_self_as_component(self):
        with self.assertRaises(ValueError):
            self.base.add_component(self.base)
