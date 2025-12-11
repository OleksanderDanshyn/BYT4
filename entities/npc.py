from entities.entity import Entity
from items.item import Item


class NPC(Entity):
    def __init__(self, drop, name, current_health):
        super().__init__(name, current_health)

        if not isinstance(drop, Item):
            raise TypeError(
                "Drop must be an Item object (Weapon, Armor, Food, Potion, or Tool)."
            )

        self._drop = None
        self.drop = drop

    @property
    def drop(self):
        return self._drop

    @drop.setter
    def drop(self, item):
        if not isinstance(item, Item):
            raise TypeError(
                "Drop must be an Item object (Weapon, Armor, Food, Potion, or Tool)."
            )

        if self._drop is not None:
            self._drop.remove_holder(self)

        self._drop = item

        self._drop.add_holder(self)