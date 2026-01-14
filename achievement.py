from datetime import datetime
from typing import Iterable
from copy import deepcopy

from items.item import Item
from utils import is_nonempty_str


class Achievement():
    title: str  # basic
    description: str  # basic
    _completed_at: datetime | None = None  # optional, complex
    difficulty_rating: int  # basic
    _rewards: list[Item]  # multi-value
    base_money_scalar: int = 5  # static

    def __init__(self, title: str, description: str, difficulty_rating: int, rewards: Iterable[Item]):
        self.title = title if is_nonempty_str(title) else None
        self.description = description if is_nonempty_str(description) else None
        self.difficulty_rating = difficulty_rating
        self._rewards = list(rewards)
        self._completed_at = None

        # Add self to extent
        Achievement._extent.append(self)

    @property
    def rewards(self) -> list[Item]:
        return self._rewards.copy()

    @property
    def money_reward(self) -> int:  # derived
        return Achievement.base_money_scalar * self.difficulty_rating

    @property
    def completed_at(self) -> datetime | None:
        return self._completed_at

    @staticmethod
    def get_all() -> list["Achievement"]:
        """This implementation should stay separate from {Achievement.get_extent}, as it serves a different purpose.
        This is a public function, wherease {Achievement.get_extent} is only for use with serialisation and may have a slightly different implementation.
        """
        return deepcopy(Achievement._extent)

    @staticmethod
    def get_completed() -> list["Achievement"]:
        return list(filter(lambda a: a.completed_at is not None, Achievement._extent))

    def complete(self):
        if self._completed_at is None:
            self._completed_at = datetime.now()

    # Extent
    @classmethod
    def get_extent(cls):
        return deepcopy(cls._extent)
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
        for instance in cls._extent:
            del instance
        # The extent should be cleared by now.
        assert not cls._extent
    
    def __del__(self):
        if self in self.__class__._extent:
            # Remove self from the extent list
            self.__class__._extent.remove(self)
        # Delete ourselves
        super.__del__(self)
