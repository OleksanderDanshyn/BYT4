from entities.npc import NPC


class Monster(NPC):
    def __init__(self, drop, is_boss, resistance, name, current_health):
        super().__init__(drop, name, current_health)
        if not isinstance(is_boss, bool):
            raise TypeError("Boss status must be a boolean (True or False).")
        self.is_boss = is_boss

        self.resistance = resistance

    @property
    def resistance(self):
        return self._resistance

    @resistance.setter
    def resistance(self, value):
        if not isinstance(value, bool):
            raise TypeError("Resistance must be a boolean.")
        self._resistance = value