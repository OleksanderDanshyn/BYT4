from effect import Effect
from entities.enemy import Enemy
from entities.entity import Entity
from entities.friendly import Friendly
from event import Event
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

        self.active_effects = []

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


    def apply_effect(self, effect, potion, current_turn):
        if not isinstance(effect, Effect):
            raise TypeError("effect must be an Effect instance.")
        from items.potion import Potion
        if not isinstance(potion, Potion):
            raise TypeError("potion must be a Potion instance.")

        player_effect = PlayerEffect(
            player=self,
            effect=effect,
            source=potion,
            source_type='potion',
            duration_turns=potion.duration,
            start_turn=current_turn
        )
        self.active_effects.append(player_effect)

    def apply_effect_from_activity(self, effect, activity, current_turn, duration_turns=3):
        if not isinstance(effect, Effect):
            raise TypeError("effect must be an Effect instance.")
        from activity import Activity
        if not isinstance(activity, Activity):
            raise TypeError("activity must be an Activity instance.")

        player_effect = PlayerEffect(
            player=self,
            effect=effect,
            source=activity,
            source_type='activity',
            duration_turns=duration_turns,
            start_turn=current_turn
        )
        self.active_effects.append(player_effect)

    def remove_effect(self, player_effect):
        if player_effect in self.active_effects:
            self.active_effects.remove(player_effect)


    def remove_expired_effects(self, current_turn):
        expired = [pe for pe in self.active_effects if pe.is_expired(current_turn)]
        for player_effect in expired:
            self.remove_effect(player_effect)


    def get_active_effect_names(self, current_turn):
        self.remove_expired_effects(current_turn)
        result = []
        for player_effect in self.active_effects:
            if player_effect.duration_turns == 0:
                result.append(f"{player_effect.effect.name} (instant)")
            else:
                turns_left = player_effect.turns_remaining(current_turn)
                result.append(f"{player_effect.effect.name} ({turns_left} turns remaining)")
        return result


    def has_effect(self, effect, current_turn):
        self.remove_expired_effects(current_turn)
        return any(pe.effect == effect for pe in self.active_effects)


    def get_effect_by_type(self, effect, current_turn):
        self.remove_expired_effects(current_turn)
        for pe in self.active_effects:
            if pe.effect == effect:
                return pe
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

    def experience_event(self, event):

        if not isinstance(event, Event):
            raise TypeError("Event must be an Event instance.")

        if event.check_event_success() is True:
            self.inventory.add_item(event.item_reward)
            self.money.__add__(event.money_reward)

    def die(self):
        for pet in self.pets:
            pet._owner = None
        self.pets.clear()

        self.active_effects.clear()

        if self.inventory is not None:
            self.inventory.delete()
            self.inventory = None

        if self in Player._extent:
            Player._extent.remove(self)
