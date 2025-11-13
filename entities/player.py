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
        self.inventory = Inventory()

        self.effects = []
        self.kills = []

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
        if isinstance(weapon, Weapon):
            self.equipped_weapon = weapon


    def equip_armor(self, armor):
        if isinstance(armor, Armor):
            self.equipped_armor = armor


    def apply_effect(self, effect):
        if isinstance(effect, Effect):
            self.effects.append(effect)


    def slay_monster(self, enemy):
        if isinstance(enemy, Enemy):
            self.kills.append(enemy)


