import unittest

from entities.animal import Animal
from items.food import Food
from items.item import Item


class TestItem(Item):
    def __init__(self, name, description="desc", buyable=True, sell_price=10):
        super().__init__(name, description, buyable, sell_price)


class TestAnimalItemAssociations(unittest.TestCase):

    def setUp(self):
        self.drop_item = TestItem("Drop")

        self.food = Food(
            saturation=5,
            name="Apple",
            description="Red apple",
            buyable=True,
            sell_price=2,
            number_of_uses=1
        )

        self.animal = Animal(
            drop=self.drop_item,
            name="Horse",
            current_health=20,
            rideable=True,
            favourite_food=self.food
        )

    def test_animal_drop_reference(self):
        self.assertIs(self.animal.drop, self.drop_item)

    def test_drop_item_has_animal_as_holder(self):
        self.assertIn(self.animal, self.drop_item.get_holders())
        self.assertEqual(len(self.drop_item.get_holders()), 1)

    def test_reassign_drop_updates_reverse_relation(self):
        new_drop = TestItem("NewDrop")
        self.animal.drop = new_drop

        self.assertIs(self.animal.drop, new_drop)
        self.assertNotIn(self.animal, self.drop_item.get_holders())
        self.assertIn(self.animal, new_drop.get_holders())

    def test_drop_not_duplicated(self):
        self.animal.drop = self.drop_item
        self.animal.drop = self.drop_item
        self.assertEqual(self.drop_item.get_holders().count(self.animal), 1)
