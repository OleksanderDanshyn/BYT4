from items.item import Item
from activity import Activity


class Tool(Item):
    def __init__(self, name, description, buyable, sell_price, durability, activity=None):
        super().__init__(name, description, buyable, sell_price)

        if not isinstance(durability, int):
            raise TypeError("Durability must be an integer.")
        if durability < 0:
            raise ValueError("Durability cannot be negative.")
        self.durability = durability

        self._activity = None
        if activity is not None and not isinstance(activity, Activity):
            raise TypeError("activity must be an Activity instance or None.")
        self.activity = activity

    @property
    def activity(self):
        return self._activity

    @activity.setter
    def activity(self, new_activity):
        from activity import Activity

        if self._activity is not None:
            self._activity.remove_tool(self)

        if new_activity is not None:
            if not isinstance(new_activity, Activity):
                raise TypeError("activity must be an Activity instance or None.")
            new_activity.add_tool(self)

        self._activity = new_activity

    def use(self):
        if self.durability <= 0:
            raise ValueError(f"{self.name} is broken and cannot be used.")

        self.durability -= 1

        if self.durability == 0:
            return f"{self.name} broke!"
        else:
            return f"Used {self.name}. Durability: {self.durability}"

    def repair(self, amount):
        if not isinstance(amount, int):
            raise TypeError("Repair amount must be an integer.")
        if amount < 0:
            raise ValueError("Repair amount cannot be negative.")

        self.durability += amount
        return f"{self.name} repaired! Durability: {self.durability}"

    def perform_activity(self, player, current_turn):
        if self.activity is None:
            raise ValueError(f"{self.name} has no associated activity.")

        return self.activity.perform(player, current_turn, tool=self)
