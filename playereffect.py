from datetime import datetime, timedelta
from effect import Effect

class PlayerEffect:
    def __init__(self, player, effect, potion):
        from items.potion import Potion

        if not isinstance(effect, Effect):
            raise TypeError("effect must be an Effect instance.")
        if not isinstance(potion, Potion):
            raise TypeError("potion must be a Potion instance.")

        self.player = player
        self.effect = effect
        self.potion = potion
        self.start_time = datetime.now()
        self.duration = potion.duration

    @property
    def is_expired(self):
        if self.duration == 0:
            return True
        end_time = self.start_time + timedelta(seconds=self.duration)
        return datetime.now() >= end_time

    @property
    def time_remaining(self):
        if self.duration == 0:
            return 0
        end_time = self.start_time + timedelta(seconds=self.duration)
        remaining = (end_time - datetime.now()).total_seconds()
        return max(0, remaining)
