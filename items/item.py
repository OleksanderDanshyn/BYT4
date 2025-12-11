import pickle
import os




class Item:
    _extent = []

    def __init__(self, name, description, buyable, sell_price):
        self.__class__._extent.append(self)

        if type(self) == Item:
            raise TypeError("Item is abstract - instantiate a subclass")

        self.inventory = None
        self._holders = []
        self._traders = []

        self._components = []
        self._combined_into = None

        self.name = name
        self.description = description
        self.buyable = buyable
        self.sell_price = sell_price
        self.buy_price = sell_price * 1.2


    def add_component(self, item):
        if not isinstance(item, Item):
            raise TypeError("Component must be an Item object.")
        if item == self:
            raise ValueError("Item cannot be a component of itself.")
        if item not in self._components:
            self._components.append(item)
            item._combined_into = self


    def remove_component(self, item):
        if item in self._components:
            self._components.remove(item)
            item._combined_into = None


    def get_components(self):
        return self._components.copy()


    def get_combined_into(self):
        return self._combined_into


    def is_component(self):
        return self._combined_into is not None


    @classmethod
    def combine_items(cls, item1, item2, new_name=None):
        from items.armor import Armor
        from items.potion import Potion
        from items.weapon import Weapon
        if type(item1) != type(item2):
            raise TypeError("Can only combine items of the same type.")

        if item1.is_component() or item2.is_component():
            raise ValueError("Cannot combine items that are already used as components.")

        if isinstance(item1, Weapon):
            return cls._combine_weapons(item1, item2, new_name)
        elif isinstance(item1, Armor):
            return cls._combine_armors(item1, item2, new_name)
        elif isinstance(item1, Potion):
            return cls._combine_potions(item1, item2, new_name)
        else:
            raise TypeError(f"Combining not supported for {type(item1).__name__}")


    @classmethod
    def _combine_weapons(cls, weapon1, weapon2, new_name):
        from items.weapon import Weapon

        if weapon1.type != weapon2.type:
            raise ValueError(f"Cannot combine {weapon1.type} with {weapon2.type}")

        combined_damage = weapon1.damage + weapon2.damage
        combined_price = weapon1.sell_price + weapon2.sell_price

        if new_name is None:
            new_name = f"Enhanced {weapon1.type.capitalize()}"

        new_description = f"Forged from two {weapon1.type}s"

        combined = Weapon(
            name=new_name,
            description=new_description,
            buyable=weapon1.buyable and weapon2.buyable,
            sell_price=combined_price,
            damage=combined_damage,
            type=weapon1.type
        )

        combined.add_component(weapon1)
        combined.add_component(weapon2)

        return combined


    @classmethod
    def _combine_armors(cls, armor1, armor2, new_name):
        from items.armor import Armor

        combined_toughness = armor1.toughness + armor2.toughness
        combined_price = armor1.sell_price + armor2.sell_price

        if new_name is None:
            new_name = f"Reinforced Armor"

        new_description = f"Combined protection from two armor pieces"

        combined = Armor(
            toughness=combined_toughness,
            name=new_name,
            description=new_description,
            buyable=armor1.buyable and armor2.buyable,
            sell_price=combined_price
        )

        combined.add_component(armor1)
        combined.add_component(armor2)

        return combined


    @classmethod
    def _combine_potions(cls, potion1, potion2, new_name):
        from items.potion import Potion

        if potion1.effect != potion2.effect:
            raise ValueError("Can only combine potions with the same effect")

        combined_power = potion1.power + potion2.power
        combined_duration = max(potion1.duration, potion2.duration)
        combined_uses = potion1.number_of_uses + potion2.number_of_uses
        combined_price = potion1.sell_price + potion2.sell_price

        if new_name is None:
            new_name = f"Greater {potion1.name}"

        new_description = f"A more potent mixture"

        combined = Potion(
            name=new_name,
            description=new_description,
            buyable=potion1.buyable and potion2.buyable,
            sell_price=combined_price,
            number_of_uses=combined_uses,
            duration=combined_duration,
            power=combined_power,
            effect=potion1.effect
        )

        combined.add_component(potion1)
        combined.add_component(potion2)

        return combined


    def add_holder(self, npc):
        from entities.npc import NPC
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
        from entities.trader import Trader
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
        for component in self._components.copy():
            self.remove_component(component)

        if self._combined_into is not None:
            self._combined_into.remove_component(self)

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