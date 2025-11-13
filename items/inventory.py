from extentbase import ExtentBase


class Inventory(ExtentBase):
    def __init__(self):
        super().__init__()
        self.max_size = 10