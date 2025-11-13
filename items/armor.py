from items.item import Item


class Armor(Item):
    def __init__(self, toughness, name, description, buyable, sell_price):
        super().__init__(name, description, buyable, sell_price)
        if not isinstance(toughness, int):
            raise TypeError("toughness must be a number.")
        if toughness <= 0:
            raise ValueError("Toughness must be greater than zero.")
        self.toughness = toughness