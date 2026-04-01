

#классы персонажей для боя

class EntityV2:
    def __init__(self, name: str, hp: int, dmg: int, char_class=None) -> None:
        self.name = name
        self.hp = hp
        self.dmg = dmg
        self.char_class = char_class
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
            
    def attack(self, target):
        print(f"{self.name} атакует {target.name}!")
        target.take_damage(self.dmg)
        return self.dmg