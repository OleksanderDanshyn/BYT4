from items.item import Item


class Weapon(Item):
    def __init__(self, name, description, buyable, sell_price, damage, type):
        super().__init__(name, description, buyable, sell_price)
        self.damage = damage
        self.type = type

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        if not isinstance(value, int):
            raise TypeError("Damage must be a number.")
        self._damage = value


    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        if not isinstance(value, str):
            raise TypeError("Type must be a string.")
        if value not in ["hammer", "bow", "sword", "axe"]:
            raise ValueError("Type must be one of 'hammer', 'bow', 'sword', 'axe'")
        if not value.strip():
            raise ValueError("Type cannot be empty or just spaces.")
        self._type = value