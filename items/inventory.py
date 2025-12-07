import pickle
import os
from items.item import Item


class Inventory:
    _extent = []

    def __init__(self, owner, max_size=10):
        self.__class__._extent.append(self)

        self.owner = owner
        self.items = {}
        self.max_size = max_size

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items.values())


    def is_empty(self):
        return len(self.items) == 0


    def add_item(self, item):
        if item is None:
            raise ValueError("Cannot add None to inventory.")

        if item.name in self.items:
            raise ValueError(f"Item '{item.name}' is already in inventory.")

        if len(self.items) >= self.max_size:
            raise OverflowError("Inventory is full.")

        self.items[item.name] = item
        return True, f"Item '{item.name}' added successfully."


    def remove_item(self, item_or_name):
        key = item_or_name.name if isinstance(item_or_name, Item) else item_or_name

        if key not in self.items:
            raise ValueError(f"Item '{key}' not found in inventory.")

        del self.items[key]
        return True, f"Item '{key}' removed successfully."

    def get_item(self, name):
        return self.items.get(name, None)


    @classmethod
    def get_extent(cls):
        return cls._extent.copy()

    @classmethod
    def save_extent(cls, filename="inventories.dat"):
        with open(filename, "wb") as file:
            pickle.dump(cls._extent, file)

    @classmethod
    def load_extent(cls, filename="inventories.dat"):
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
