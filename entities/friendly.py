from entities.npc import NPC


class Friendly(NPC):
    def __init__(self, drop, name, current_health, tameable, reputation):
        super().__init__(drop, name, current_health)
        if not isinstance(tameable, bool):
            raise TypeError("Tameable must be a boolean (True or False).")
        self.tameable = tameable

        self.reputation = reputation


    @property
    def reputation(self):
        return self._reputation

    @reputation.setter
    def reputation(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Reputation must be a number (int or float).")
        if not (0 <= value <= 100):
            raise ValueError("Reputation must be between 0 and 100.")
        self._reputation = value