from extentbase import ExtentBase
from items.item import Item


class Inventory(ExtentBase):
    def __init__(self, owner, max_size=10):
        super().__init__()
        self.owner = owner
        self.items = {}
        self.max_size = max_size


    def __len__(self):
        return len(self.items)


    def __iter__(self):
        return iter(self.items.values())  # Iterate over items, not keys


    def is_empty(self):
        return len(self.items) == 0


    def add_item(self, item):
        if item is None:
            raise ValueError("Cannot add None to inventory.")

        if item.name in self.items:
            raise ValueError(f"Item '{item.name}' is already in inventory.")

        if len(self.items) >= self.max_size:
            raise OverflowError("Inventory is full.")

        self.items[item.name] = item
        return True, f"Item '{item.name}' added successfully."


    def remove_item(self, item_or_name):
        if isinstance(item_or_name, Item):
            key = item_or_name.name
        else:
            key = item_or_name

        if key not in self.items:
            raise ValueError(f"Item '{key}' not found in inventory.")

        del self.items[key]
        return True, f"Item '{key}' removed successfully."


    def get_item(self, name):
        return self.items.get(name, None)
