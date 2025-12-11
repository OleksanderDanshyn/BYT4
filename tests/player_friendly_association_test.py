import unittest

from entities.player import Player
from entities.friendly import Friendly
from items.item import Item


class TestItem(Item):
    def __init__(self, name, description="desc", buyable=True, sell_price=10):
        super().__init__(name, description, buyable, sell_price)


class TestPlayerFriendlyAssociations(unittest.TestCase):

    def setUp(self):
        self.drop = TestItem("Bone")
        self.player = Player("Hero", current_health=10, money=100)

        self.pet = Friendly(
            drop=self.drop,
            name="Wolf",
            current_health=15,
            tameable=True,
            reputation=50
        )

        self.other_pet = Friendly(
            drop=self.drop,
            name="Cat",
            current_health=10,
            tameable=True,
            reputation=20
        )

    def test_add_pet_sets_reverse_association(self):
        self.player.add_pet(self.pet)

        self.assertIn(self.pet, self.player.pets)
        self.assertIs(self.pet.get_owner(), self.player)

    def test_remove_pet_clears_reverse_association(self):
        self.player.add_pet(self.pet)
        self.player.remove_pet(self.pet)

        self.assertNotIn(self.pet, self.player.pets)
        self.assertIsNone(self.pet.get_owner())

    def test_add_pet_rejects_duplicate(self):
        self.player.add_pet(self.pet)
        with self.assertRaises(ValueError):
            self.player.add_pet(self.pet)

    def test_add_pet_rejects_untameable(self):
        untameable = Friendly(
            drop=self.drop,
            name="Bear",
            current_health=20,
            tameable=False,
            reputation=40
        )
        with self.assertRaises(ValueError):
            self.player.add_pet(untameable)

    def test_add_pet_rejects_already_tamed_pet(self):
        other_player = Player("Mage", current_health=8, money=50)

        other_player.add_pet(self.pet)

        with self.assertRaises(ValueError):
            self.player.add_pet(self.pet)

    def test_remove_pet_not_in_list(self):
        with self.assertRaises(ValueError):
            self.player.remove_pet(self.pet)
