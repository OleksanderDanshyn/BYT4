from entities.npc import NPC
from items.food import Food


class Animal(NPC):
    def __init__(self, drop, name, current_health, rideable, favourite_food):
        super().__init__(drop, name, current_health)

        if not isinstance(rideable, bool):
            raise TypeError("Rideable status must be a boolean (True or False).")
        self.rideable = rideable

        if not isinstance(favourite_food, Food):
            raise TypeError("Favourite food must be a Food object.")

        self.favourite_food = favourite_food
