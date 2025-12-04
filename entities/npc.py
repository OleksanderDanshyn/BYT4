from entities.entity import Entity
from items.item import Item


class NPC(Entity):
    def __init__(self, drop, name, current_health):
        super().__init__(name, current_health)

        if not isinstance(drop, Item):
            raise TypeError(
                "Drop must be an Item object (Weapon, Armor, Food, Potion, or Tool)."
            )

        self.drop = drop
