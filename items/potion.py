from items.consumanble import Consumable
from effect import Effect

class Potion(Consumable):
    def __init__(self, name, description, buyable, sell_price, number_of_uses, duration, power, effect=None):
        super().__init__(number_of_uses, name, description, buyable, sell_price)
        if not isinstance(duration, int):
            raise TypeError("Duration must be a number.")
        if duration < 0:
            raise ValueError("Duration cannot be negative.")
        self.duration = duration

        if not isinstance(power, int):
            raise TypeError("Power must be a number.")
        if power < 0:
            raise ValueError("Power cannot be negative.")
        self.power = power

        if effect is not None and not isinstance(effect, Effect):
            raise TypeError("effect must be an Effect instance or None.")
        self.effect = effect

    @property
    def effect(self):
        return self._effect

    @effect.setter
    def effect(self, new_effect):
        from effect import Effect

        if self.effect is not None:
            self.effect.remove_potion(self)

        if new_effect is not None:
            if not isinstance(new_effect, Effect):
                raise TypeError("effect must be an Effect instance or None.")
            new_effect.add_potion(self)

        self._effect = new_effect


    def use_on_player(self, player):
        from entities.player import Player
        if not isinstance(player, Player):
            raise TypeError("player must be a Player instance.")

        player.health = min(
            player.health + self.power,
            player.max_health
        )

        if self.effect is not None:
            player.apply_effect(self.effect, self)

        self.number_of_uses -= 1

        return f"Used {self.name}! Restored {self.power} HP."