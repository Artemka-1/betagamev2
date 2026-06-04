import random
from core.damage_result import DamageResult


class CombatSystem:

    @staticmethod
    def calculate_damage(
        source,
        target,
        damage_range: tuple[int, int] | None = None,
        base_damage: int | None = None,
        damage_type: str = "physical"
    ) -> DamageResult:

        # 1. BASE DAMAGE RESOLVE
        if damage_range is not None:
            damage = random.randint(*damage_range)
        elif base_damage is not None:
            damage = base_damage
        else:
            damage = 0

        # 2. MITIGATION
        if damage_type == "physical":
            reduction = target.armor / (100 + target.armor)
            mitigated = damage * (1 - reduction)

        elif damage_type == "magic":
            reduction = target.magic_resistance / (100 + target.magic_resistance)
            mitigated = damage * (1 - reduction)

        else:  # true damage
            mitigated = damage

        # 3. FINAL DAMAGE
        final_damage = max(0, int(mitigated))

        # 4. RESULT (NO SIDE EFFECTS)
        return DamageResult(
            source=source,
            target=target,
            raw_damage=damage,
            final_damage=final_damage,
            damage_type=damage_type
        )
