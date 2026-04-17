import random

class EntityV2:
    def __init__(self, name: str, hp: int, dmg: int, char_class=None, faction=None):
        self.name = name
        self.hp = hp
        self.dmg = dmg
        self.char_class = char_class
        self.faction = faction

        # 🔥 ДОБАВЛЯЕМ ОД
        self.max_od = 10
        self.od = 10
        
        
    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

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
        cost = 3  # стоимость атаки

        if self.od < cost:
            print(f"{self.name} не хватает ОД! ({self.od})")
            return 0

        self.od -= cost

        base_damage = self.dmg
        crit_chance, crit_mult = self.get_crit_stats()
        
        # Разброс урона ±20%
        damage_variance = int(base_damage * 0.2)
        base_damage = base_damage + random.randint(-damage_variance, damage_variance)

        if random.random() < crit_chance:
            damage = int(base_damage * crit_mult)
            print(f"💥 КРИТ {self.name}!")
        else:
            damage = base_damage

        target.take_damage(damage)

        print(f"{self.name} наносит {damage} урона. ОД осталось: {self.od}")

        return damage