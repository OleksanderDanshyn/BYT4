import unittest

from entities.animal import Animal
from items.food import Food
from items.weapon import Weapon


class TestAnimal(unittest.TestCase):

    def test_valid_animal(self):
        carrot = Food(saturation=5, name="carrot", description="tasty", buyable=True, sell_price=10, number_of_uses=1)
        weapon = Weapon("Sword", "A sharp blade", True, 50, 10, "sword")
        e = Animal(drop=weapon, name="Oleg", current_health=10, rideable=True, favourite_food=carrot)
        self.assertEqual(e.rideable, True)
        self.assertEqual(e.name, "Oleg")
