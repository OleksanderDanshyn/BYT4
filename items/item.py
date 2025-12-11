import pickle
import os
from entities.npc import NPC
from entities.trader import Trader


class Item:
    _extent = []

    def __init__(self, name, description, buyable, sell_price):
        self.__class__._extent.append(self)

        if type(self) == Item:
            raise TypeError("Item is abstract - instantiate a subclass")

        self.inventory = None
        self._holders = []
        self._traders = []

        self.name = name
        self.description = description
        self.buyable = buyable
        self.sell_price = sell_price
        self.buy_price = sell_price * 1.2

    def add_holder(self, npc):
        if not isinstance(npc, NPC):
            raise TypeError("Holder must be an NPC object.")
        if npc not in self._holders:
            self._holders.append(npc)


    def remove_holder(self, npc):
        if npc in self._holders:
            self._holders.remove(npc)


    def get_holders(self):
        return self._holders.copy()


    def add_trader(self, trader):
        if not isinstance(trader, Trader):
            raise TypeError("Must be a Trader object.")
        if trader not in self._traders:
            self._traders.append(trader)


    def remove_trader(self, trader):
        if trader in self._traders:
            self._traders.remove(trader)


    def get_traders(self):
        return self._traders.copy()


    def get_owner_player(self):
        if self.inventory is not None:
            return self.inventory.owner
        return None


    def get_all_owners(self):
        return {
            'player': self.get_owner_player(),
            'inventory': self.inventory,
            'drop_holders': self._holders.copy(),
            'traders': self._traders.copy()
        }


    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if not value.strip():
            raise ValueError("Name cannot be empty or just spaces.")
        if len(value) > 30:
            raise ValueError("Name cannot exceed 30 characters.")
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError("Description must be a string.")
        if not value.strip():
            raise ValueError("Description cannot be empty or just spaces.")
        if len(value) > 50:
            raise ValueError("Description cannot exceed 50 characters.")
        self._description = value

    @property
    def buyable(self):
        return self._buyable

    @buyable.setter
    def buyable(self, value):
        if not isinstance(value, bool):
            raise TypeError("Buyable must be a boolean.")
        self._buyable = value

    @property
    def sell_price(self):
        return self._sell_price

    @sell_price.setter
    def sell_price(self, value):
        if not isinstance(value, int):
            raise TypeError("Sell price must be a number.")
        if value < 0:
            raise ValueError("Sell price cannot be negative.")
        self._sell_price = value

    @classmethod
    def get_extent(cls):
        return cls._extent.copy()

    @classmethod
    def save_extent(cls, filename="items.dat"):
        with open(filename, "wb") as file:
            pickle.dump(cls._extent, file)

    @classmethod
    def load_extent(cls, filename="items.dat"):
        if os.path.exists(filename):
            with open(filename, "rb") as file:
                cls._extent = pickle.load(file)
        else:
            cls._extent = []

    @classmethod
    def clear_extent(cls):
        cls._extent = []

    def delete(self):
        for holder in self._holders.copy():
            if holder.drop == self:
                holder.drop = None
            self.remove_holder(holder)

        for trader in self._traders.copy():
            trader.remove_item_from_stock(self)

        if self.inventory is not None:
            try:
                self.inventory.remove_item(self)
            except ValueError:
                pass

        if self in self.__class__._extent:
            self.__class__._extent.remove(self)