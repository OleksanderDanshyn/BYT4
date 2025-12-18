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
        self._friendly = None
        self._enemy = None

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

    def set_friendly(self, friendly):
        if self._enemy is not None:
            raise ValueError("NPC cannot be both Friendly and Enemy.")
        self._friendly = friendly

    def set_enemy(self, enemy):
        if self._friendly is not None:
            raise ValueError("NPC cannot be both Friendly and Enemy.")
        self._enemy = enemy

    def is_friendly(self):
        return self._friendly is not None

    def is_enemy(self):
        return self._enemy is not None
