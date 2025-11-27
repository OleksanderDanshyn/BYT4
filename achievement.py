from typing import Iterable

from items.item import Item
from utils import is_nonempty_str


class Achievement:
    _extent: list["Achievement"] = []  # extent

    title: str  # basic
    description: str  # basic
    is_completed: bool = False  # basic (NON-STATIC!)
    difficulty_rating: int  # basic
    _rewards: tuple[Item, ...]  # multi-value
    base_money_scalar: int = 5  # static

    def __init__(self, title: str, description: str, difficulty_rating: int, rewards: Iterable[Item]):
        self.title = title if is_nonempty_str(title) else None
        self.description = description if is_nonempty_str(description) else None
        self.difficulty_rating = difficulty_rating
        self._rewards = tuple(rewards)

        Achievement._extent.append(self)

    @property
    def rewards(self) -> tuple[Item, ...]:
        return self._rewards

    @property
    def money_reward(self) -> int:  # derived
        return Achievement.base_money_scalar * self.difficulty_rating

    @staticmethod
    def get_all():
        return tuple(Achievement._extent)
