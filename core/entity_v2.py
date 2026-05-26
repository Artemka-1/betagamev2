



class EntityV2:
    def __init__(
        self,
        name: str,
        max_hp: int,
        armor: int = 0,
        magic_resistance: float = 0.0,
        od_max: int = 10,
        faction: str | None = None,
        char_class: str | None = None,
    ):
        self.name = name

        self.max_hp = max_hp
        self.hp = max_hp

        self.armor = armor
        self.magic_resistance = magic_resistance

        self.od_max = od_max
        self.od = od_max

        self.faction = faction
        self.char_class = char_class

        self.statuses: list = []

    # -----------------------------
    # STATE ONLY
    # -----------------------------

    def is_alive(self) -> bool:
        return self.hp > 0

    def apply_damage(self, damage_result) -> None:
        """Entity не считает урон, а только применяет готовый результат"""
        self.hp = max(0, self.hp - damage_result.final_damage)