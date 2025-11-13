from items.item import Item


class Tool(Item):
    def __init__(self, name, description, buyable, sell_price, ability):
        super().__init__(name, description, buyable, sell_price)
        self.ability = ability


    @property
    def ability(self):
        return self._ability

    @ability.setter
    def ability(self, value):
        if not value.strip():
            raise ValueError("Ability cannot be empty or just spaces.")
        self._ability = value