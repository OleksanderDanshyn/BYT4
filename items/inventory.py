from extentbase import ExtentBase


class Inventory(ExtentBase):
    def __init__(self, max_size=10):
        super().__init__()
        self.items = []
        self.max_size = max_size

    def __len__(self):
        return len(self.items)

    def __iter__(self):
        return iter(self.items)

    def is_empty(self):
        return len(self.items) == 0

    def add_item(self, item):
        if len(self.items) >= self.max_size:
            return False, "Inventory is full!"
        self.items.append(item)
        return True, f"Added {item.name} to inventory."

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        return False