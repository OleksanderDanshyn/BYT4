import pickle
import os

class Effect:
    _extent = []

    def __init__(self, name, description):
        self.__class__._extent.append(self)

        if not isinstance(name, str):
            raise TypeError("Effect name must be a string.")
        if not name.strip():
            raise ValueError("Effect name cannot be empty or just spaces.")
        self.name = name

        if not isinstance(description, str):
            raise TypeError("Effect description must be a string.")
        if not description.strip():
            raise ValueError("Effect description cannot be empty or just spaces.")
        self.description = description

        self._potions = []

    @property
    def potions(self):
        return self._potions.copy()

    def add_potion(self, potion):
        if potion not in self._potions:
            self._potions.append(potion)

    def remove_potion(self, potion):
        if potion in self._potions:
            self._potions.remove(potion)

    def delete(self):
        for potion in self._potions.copy():
            potion.effect = None

        if self in self.__class__._extent:
            self.__class__._extent.remove(self)

    @classmethod
    def get_extent(cls):
        return cls._extent.copy()

    @classmethod
    def save_extent(cls, filename="effects.dat"):
        with open(filename, "wb") as file:
            pickle.dump(cls._extent, file)

    @classmethod
    def load_extent(cls, filename="effects.dat"):
        if os.path.exists(filename):
            with open(filename, "rb") as file:
                cls._extent = pickle.load(file)
        else:
            cls._extent = []

    @classmethod
    def clear_extent(cls):
        cls._extent = []
