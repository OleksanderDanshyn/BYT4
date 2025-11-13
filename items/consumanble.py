from items.item import Item


class Consumable(Item):
    def __init__(self, number_of_uses, name, description, buyable, sell_price):
        super().__init__(name, description, buyable, sell_price)

        if not isinstance(number_of_uses, int):
            raise TypeError("number_of_uses must be a number.")
        if number_of_uses <= 0:
            raise ValueError("Number of uses must be greater than zero.")
        self.number_of_uses = number_of_uses