import os
import pickle
from copy import deepcopy

from items.item import Item

class Event:

    _extent: list["Event"] = []
    types_list = ["safe", "standard", "dangerous"]

    def __init__(self, name, event_type, optional, difficulty, item_reward, Player):
        self.name = name
        self.event_type = event_type
        self.optional = optional
        self.difficulty = difficulty
        self.item_reward = item_reward
        self.money_reward = abs((Player.max_health - Player.current_health))*difficulty

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if not value.strip():
            raise ValueError("Name must not be empty or only whitespace.")
        if len(value) > 30:
            raise ValueError("Name must not be longer than 30 characters.")
        self.name = value

    @property
    def event_type(self):
        return self.event_type

    @event_type.setter
    def event_type(self, value):
        if not isinstance(value, str):
            raise TypeError("Description must be a string.")
        if not value.strip():
            raise ValueError("Description must not be empty or only whitespace.")
        if type not in self.types_list:
            raise ValueError("Type must be one of 'safe', 'standard', 'dangerous'.")
        self.event_type = value

    @property
    def optional(self):
        return self.optional

    @optional.setter
    def optional(self, value):
        if not isinstance(value, bool):
            raise TypeError("Optional must be a boolean.")
        self.optional = value

    @property
    def difficulty(self):
        return self.difficulty

    @difficulty.setter
    def difficulty(self, value):
        if not isinstance(value, int):
            raise TypeError("Difficulty must be an integer.")
        if value <= 0 or value >= 10:
            raise ValueError("Difficulty must be between 0 and 10 (inclusive).")
        self.difficulty = value

    @property
    def item_rewards(self):
        return self.item_rewards

    @item_rewards.setter
    def item_rewards(self, value):
        if not isinstance(value, Item.__class__):
            raise TypeError("item_reward must be an Item.")

        self.item = value

    @classmethod
    def get_extent(cls):
        return deepcopy(cls._extent)
    @classmethod
    def save_extent(cls, filename=None):
        if filename is None:
            filename = f"{cls.__name__.lower()}s.dat"
        with open(filename, "wb") as file:
            pickle.dump(cls._extent, file)
    @classmethod
    def load_extent(cls, filename=None):
        if filename is None:
            filename = f"{cls.__name__.lower()}s.dat"
        if os.path.exists(filename):
            with open(filename, "rb") as file:
                cls._extent = pickle.load(file)
        else:
            cls._extent = []

    @classmethod
    def clear_extent(cls):
        cls._extent = []
    def delete(self):
        if self in self.__class__._extent:
            self.__class__._extent.remove(self)
