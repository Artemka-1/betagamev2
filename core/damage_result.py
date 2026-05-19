# core/damage_result.py
class DamageResult:
    def __init__(
        self,
        raw_damage: int,
        final_damage: int,
        is_crit: bool = False,
        reduced_by_armor: int = 0,
        log: list[str] | None = None
    ):
        self.raw_damage = raw_damage
        self.final_damage = final_damage
        self.is_crit = is_crit
        self.reduced_by_armor = reduced_by_armor
        self.log = log or []