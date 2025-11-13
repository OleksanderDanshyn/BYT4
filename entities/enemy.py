from entities.npc import NPC


class Enemy(NPC):
    def __init__(self, drop, name, current_health, damage):
        super().__init__(drop, name, current_health)
        self.damage = damage

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        if not isinstance(value, int):
            raise TypeError("damage must be a number.")
        self._damage = value