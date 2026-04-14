

#классы персонажей для боя

import random


class EntityV2:
    def __init__(self, name: str, hp: int, dmg: int, char_class=None, faction=None) -> None:
        self.name = name
        self.hp = hp
        self.dmg = dmg
        self.char_class = char_class
        self.faction = faction
        
#проверка жив ли персонаж для определения конца боя
    def is_alive(self) -> bool:
        return self.hp > 0

    def __str__(self) -> str:
        return f"{self.name} ({self.hp} HP, {self.dmg} dmg)"
    
#метод для получения урона и проверки на отрицательное здоровье
    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0
        print(f"{self.name} получает {amount} урона. Осталось {self.hp} HP.")
        
        
    def get_crit_stats(self):
        if self.faction == "DEX":
            return 0.20, 1.7
        elif self.faction == "STR":
            return 0.05, 1.3
        elif self.faction == "INT":
            return 0.10, 1.5
        else:
            return 0.10, 1.5
            
    def attack(self, target):
        print(f"{self.name} атакует {target.name}!")

        base_damage = self.dmg

        crit_chance, crit_mult = self.get_crit_stats()

        is_crit = random.random() < crit_chance

        if is_crit:
            damage = int(base_damage * crit_mult)
            print(f"💥 {self.name} наносит КРИТИЧЕСКИЙ удар!")
        else:
            damage = base_damage

        target.take_damage(damage)
        return damage
        
        
        
        
   