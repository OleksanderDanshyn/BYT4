from entities.npc import NPC


class Enemy:
    def __init__(self, npc, damage):
        if not isinstance(npc, NPC):
            raise TypeError("Enemy must be associated with an NPC.")

        self.npc = npc
        npc.set_enemy(self)

        self.damage = damage
        self.killed_by = []


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
