from datetime import datetime
from typing import Iterable

from extentbase import ExtentBase
from items.item import Item
from utils import is_nonempty_str


class Achievement(ExtentBase):
    title: str  # basic
    description: str  # basic
    completed_at: datetime | None = None  # optional, complex
    difficulty_rating: int  # basic
    _rewards: list[Item]  # multi-value
    base_money_scalar: int = 5  # static

    def __init__(self, title: str, description: str, difficulty_rating: int, rewards: Iterable[Item]):
        self.title = title if is_nonempty_str(title) else None
        self.description = description if is_nonempty_str(description) else None
        self.difficulty_rating = difficulty_rating
        self._rewards = list(rewards)
        self.completed_at = None

        super().__init__()

    @property
    def rewards(self) -> list[Item]:
        return self._rewards.copy()

    @property
    def money_reward(self) -> int:  # derived
        return Achievement.base_money_scalar * self.difficulty_rating

    @staticmethod
    def get_all() -> list["Achievement"]:
        return Achievement._extent.copy()

    @staticmethod
    def get_completed() -> list["Achievement"]:
        return list(filter(lambda a: a.completed_at is not None, Achievement._extent))

    def complete(self) -> None:
        if self.completed_at is None:
            self.completed_at = datetime.now()

