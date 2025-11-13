from extentbase import ExtentBase


class Entity(ExtentBase):
    def __init__(self, name, current_health):
        super().__init__()
        self.name = name
        self.health = current_health

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if not value.strip():
            raise ValueError("Name cannot be empty or just spaces.")
        if len(value) > 30:
            raise ValueError("Name cannot exceed 30 characters.")
        self._name = value


    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if not isinstance(value, int):
            raise TypeError("Health must be a number.")
        if value < 0:
            raise ValueError("Health cannot be negative.")
        self._health = value