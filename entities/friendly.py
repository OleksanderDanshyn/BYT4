from entities.npc import NPC


class Friendly:
    def __init__(self, npc, tameable, reputation):
        if not isinstance(npc, NPC):
            raise TypeError("Friendly must be associated with an NPC.")

        self.npc = npc
        npc.set_friendly(self)

        if not isinstance(tameable, bool):
            raise TypeError("Tameable must be a boolean.")
        self.tameable = tameable

        self.reputation = reputation
        self._owner = None

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

    def get_owner(self):
        return self._owner

    def is_tamed(self):
        return self._owner is not None