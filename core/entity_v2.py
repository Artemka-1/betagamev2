class EntityV2:
    def __init__(self, name: str, hp: int, dmg: int, char_class=None) -> None:
        self.name = name
        self.hp = hp
        self.dmg = dmg
        self.char_class = char_class

    def is_alive(self) -> bool:
        return self.hp > 0

    def __str__(self) -> str:
        return f"{self.name} ({self.hp} HP, {self.dmg} dmg)"