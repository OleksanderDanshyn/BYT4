from entities.npc import NPC


class Trader(NPC):
    ALLOWED_TYPES = {"armor", "weapons", "potions", "food", "misc"}

    def __init__(self, drop, trader_type, sale, name, current_health):
        super().__init__(drop, name, current_health)

        if not isinstance(trader_type, str):
            raise TypeError("Trader type must be a string.")
        trader_type = trader_type.lower().strip()

        if trader_type not in Trader.ALLOWED_TYPES:
            raise ValueError(
                f"Invalid trader type '{trader_type}'. "
                f"Must be one of: {', '.join(Trader.ALLOWED_TYPES)}"
            )
        self.type = trader_type

        if not isinstance(sale, bool):
            raise TypeError("Sale must be a boolean (True or False).")
        self.sale = sale

        self._stock = []

    def add_item_to_stock(self, item):
        from items.item import Item
        if not isinstance(item, Item):
            raise TypeError("Can only add Item objects to stock.")
        if item not in self._stock:
            self._stock.append(item)
            item.add_trader(self)

    def remove_item_from_stock(self, item):
        if item in self._stock:
            self._stock.remove(item)
            item.remove_trader(self)

    def get_stock(self):
        return self._stock.copy()

    def has_item(self, item):
        return item in self._stock

    def clear_stock(self):
        for item in self._stock.copy():
            self.remove_item_from_stock(item)