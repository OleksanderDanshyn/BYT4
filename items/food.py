from items.consumanble import Consumable


class Food(Consumable):
    def __init__(self, saturation, name, description, buyable, sell_price, number_of_uses):
        super().__init__(number_of_uses, name, description, buyable, sell_price)
        if not isinstance(saturation, int):
            raise TypeError("Saturation must be a number.")
        if saturation < 0:
            raise ValueError("Saturation cannot be negative.")
        self.saturation = saturation