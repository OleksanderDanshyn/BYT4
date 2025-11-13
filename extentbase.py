import pickle
import os


class ExtentBase:
    _extent = []

    def __init__(self):
        self.__class__._extent.append(self)


    @classmethod
    def get_extent(cls):
        return cls._extent.copy()


    @classmethod
    def save_extent(cls, filename=None):
        if filename is None:
            filename = f"{cls.__name__.lower()}s.dat"
        with open(filename, "wb") as file:
            pickle.dump(cls._extent, file)


    @classmethod
    def load_extent(cls, filename=None):
        if filename is None:
            filename = f"{cls.__name__.lower()}s.dat"
        if os.path.exists(filename):
            with open(filename, "rb") as file:
                cls._extent = pickle.load(file)
        else:
            cls._extent = []


    @classmethod
    def clear_extent(cls):
        cls._extent = []


    def delete(self):
        if self in self.__class__._extent:
            self.__class__._extent.remove(self)

