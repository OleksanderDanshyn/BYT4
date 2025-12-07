from entities.npc import NPC


class Enemy(NPC):
    def __init__(self, drop, name, current_health, damage):
        super().__init__(drop, name, current_health)
        self.damage = damage

        self.killed_by = []  # reverse association

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        if not isinstance(value, int):
            raise TypeError("damage must be a number.")
        self._damage = value

    def add_killer(self, player):
        if player not in self.killed_by:
            self.killed_by.append(player)
