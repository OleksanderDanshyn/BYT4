from extentbase import ExtentBase


class Effect(ExtentBase):
    def __init__(self, name, description):
        super().__init__()
        if not isinstance(name, str):
            raise TypeError("Effect name must be a string.")
        if not name.strip():
            raise ValueError("Effect name cannot be empty or just spaces.")
        self.name = name

        if not isinstance(description, str):
            raise TypeError("Effect description must be a string.")
        if not description.strip():
            raise ValueError("Effect description cannot be empty or just spaces.")
        self.description = description