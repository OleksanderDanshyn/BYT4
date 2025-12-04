from datetime import datetime, timedelta
from effect import Effect
from entities.enemy import Enemy
from entities.entity import Entity
from items.armor import Armor
from items.inventory import Inventory
from items.weapon import Weapon


class Player(Entity):
    _extent = []
    max_health = 10

    def __init__(self, name, current_health, money):
        super().__init__(name, current_health)
        if not isinstance(money, int):
            raise TypeError("Money must be an integer.")
        self.hunger = 10
        self.pets = []
        self.equipped_armor = None
        self.equipped_weapon = None
        self.money = money

        self.inventory = Inventory(self)

        self.kills = []

        self.active_effects = {}

        Player._extent.append(self)

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, value):
        if not isinstance(value, int):
            raise TypeError("Money must be an integer.")
        self._money = value

    def equip_weapon(self, weapon):
        if weapon is None:
            raise ValueError("Weapon cannot be None.")

        if not isinstance(weapon, Weapon):
            raise TypeError("Must equip a Weapon instance.")

        if weapon.name not in self.inventory.items:
            raise ValueError("Cannot equip a weapon not in inventory.")

        self.equipped_weapon = weapon


    def equip_armor(self, armor):
        if armor is None:
            raise ValueError("Armor cannot be None.")

        if not isinstance(armor, Armor):
            raise TypeError("Must equip an Armor instance.")

        if armor.name not in self.inventory.items:
            raise ValueError("Cannot equip an armor not in inventory.")

        self.equipped_armor = armor


    def apply_effect(self, effect, potion):
        if not isinstance(effect, Effect):
            raise TypeError("effect must be an Effect instance.")
        from items.potion import Potion
        if not isinstance(potion, Potion):
            raise TypeError("potion must be a Potion instance.")

        self.active_effects[effect] = {
            'potion': potion,
            'start_time': datetime.now(),
            'duration': potion.duration
        }


    def remove_effect(self, effect):
        if effect in self.active_effects:
            del self.active_effects[effect]


    def is_effect_expired(self, effect):
        if effect not in self.active_effects:
            return True

        effect_data = self.active_effects[effect]
        duration = effect_data['duration']

        if duration == 0:
            return True

        start_time = effect_data['start_time']
        end_time = start_time + timedelta(seconds=duration)
        return datetime.now() >= end_time


    def get_effect_time_remaining(self, effect):
        if effect not in self.active_effects:
            return 0

        effect_data = self.active_effects[effect]
        duration = effect_data['duration']

        if duration == 0:
            return 0

        start_time = effect_data['start_time']
        end_time = start_time + timedelta(seconds=duration)

        if datetime.now() >= end_time:
            return 0

        remaining = (end_time - datetime.now()).total_seconds()
        return max(0, remaining)


    def remove_expired_effects(self):
        expired_effects = [effect for effect in self.active_effects.keys()
                           if self.is_effect_expired(effect)]
        for effect in expired_effects:
            self.remove_effect(effect)


    def get_active_effect_names(self):
        self.remove_expired_effects()
        result = []
        for effect, data in self.active_effects.items():
            if data['duration'] == 0:
                result.append(f"{effect.name} (instant)")
            else:
                time_left = self.get_effect_time_remaining(effect)
                result.append(f"{effect.name} ({int(time_left)}s remaining)")
        return result


    def get_effect_potion(self, effect):
        if effect in self.active_effects:
            return self.active_effects[effect]['potion']
        return None

    def slay_monster(self, enemy):
        if not isinstance(enemy, Enemy):
            raise TypeError("Can only slay Enemy instances.")

        if enemy in self.kills:
            raise ValueError("Enemy already recorded as slain.")

        self.kills.append(enemy)

    def add_pet(self, pet):

        if pet in self.pets:
            raise ValueError("Pet already in pet list.")

        if not isinstance(pet, Friendly):
            raise TypeError("Pet must be an Friendly instance.")

        self.pets.append(pet)