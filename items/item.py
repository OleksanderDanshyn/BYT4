from extentbase import ExtentBase

class Item(ExtentBase):
    def __init__(self, name, description, buyable, sell_price):
        super().__init__()

        if type(self) == Item:
            raise TypeError("Item is abstract - instantiate a specific subclass (Weapon, Armor, etc.)")

        self.name = name
        self.description = description
        self.buyable = buyable
        self.sell_price = sell_price
        self.buy_price = sell_price * 1.2


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
            raise TypeError("Buyable must be a boolean (True or False).")
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