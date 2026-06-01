# core/damage_result.py
class DamageResult:
    def __init__(
        self,
        source,
        target,
        raw_damage: int,
        final_damage: int,
        damage_type: str = "physical",
        is_crit: bool = False,
        reduced_by_armor: int = 0,
        log: list[str] | None = None
    ):
        self.source = source
        self.target = target
        self.raw_damage = raw_damage
        self.final_damage = final_damage
        self.damage_type = damage_type
        self.is_crit = is_crit
        self.reduced_by_armor = reduced_by_armor
        self.log = log or []

    def apply(self):
        if self.target is not None:
            self.target.hp = max(0, self.target.hp - self.final_damage)
