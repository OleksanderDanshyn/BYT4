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
