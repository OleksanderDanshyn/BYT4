from effect import Effect
from entities.enemy import Enemy
from entities.entity import Entity
from entities.friendly import Friendly
from items.armor import Armor
from items.inventory import Inventory
from items.weapon import Weapon
from playereffect import PlayerEffect


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

        pe = PlayerEffect(self, effect, potion)
        self.active_effects.append(pe)

    def remove_effect(self, effect):
        self.active_effects = [
            pe for pe in self.active_effects
            if pe.effect != effect
        ]

    def remove_expired_effects(self):
        self.active_effects = [
            pe for pe in self.active_effects
            if not pe.is_expired
        ]

    def get_effect_time_remaining(self, effect):
        for pe in self.active_effects:
            if pe.effect == effect:
                return pe.time_remaining
        return 0

    def get_active_effect_names(self):
        self.remove_expired_effects()
        result = []
        for pe in self.active_effects:
            if pe.duration == 0:
                result.append(f"{pe.effect.name} (instant)")
            else:
                result.append(f"{pe.effect.name} ({int(pe.time_remaining)}s remaining)")
        return result

    def get_effect_potion(self, effect):
        for pe in self.active_effects:
            if pe.effect == effect:
                return pe.potion
        return None

    def slay_monster(self, enemy):
        if not isinstance(enemy, Enemy):
            raise TypeError("Can only slay Enemy instances.")

        if enemy in self.kills:
            raise ValueError("Enemy already recorded as slain.")

        self.kills.append(enemy)
        enemy.add_killer(self)


    def add_pet(self, pet):
        if not isinstance(pet, Friendly):
            raise TypeError("Pet must be a Friendly instance.")

        if pet in self.pets:
            raise ValueError("Pet already in pet list.")

        if not pet.tameable:
            raise ValueError(f"{pet.name} cannot be tamed.")

        if pet._owner is not None:
            raise ValueError(f"{pet.name} is already tamed.")

        self.pets.append(pet)
        pet._owner = self

    def remove_pet(self, pet):
        if pet not in self.pets:
            raise ValueError("Pet not in pet list.")

        self.pets.remove(pet)
        pet._owner = None