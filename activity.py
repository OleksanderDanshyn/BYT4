from extentbase import ExtentBase


class Activity(ExtentBase):
    def __init__(self, name, description):
        super().__init__()
        if not isinstance(name, str):
            raise TypeError("Activity name must be a string.")
        if not name.strip():
            raise ValueError("Name cannot be empty or just spaces.")
        self.name = name

        if not isinstance(description, str):
            raise TypeError("Activity description must be a string.")
        if not description.strip():
            raise ValueError("Activity description cannot be empty or just spaces.")
        self.description = description