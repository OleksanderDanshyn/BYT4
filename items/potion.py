from items.consumanble import Consumable


class Potion(Consumable):
    def __init__(self, name, description, buyable, sell_price, number_of_uses, duration, power):
        super().__init__(number_of_uses, name, description, buyable, sell_price)
        if not isinstance(duration, int):
            raise TypeError("Duration must be a number.")
        if duration < 0:
            raise ValueError("Duration cannot be negative.")
        self.duration = duration


        if not isinstance(power, int):
            raise TypeError("Power must be a number.")
        if power < 0:
            raise ValueError("Power cannot be negative.")
        self.power = power


