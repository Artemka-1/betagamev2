from core.damage_result import DamageResult


class CombatSystem:

    @staticmethod
    def calculate_damage(attacker, defender, base_damage: int, damage_type="physical"):
        raw_damage = base_damage
        armor_used = 0
        resist_used = 0

        if damage_type == "physical":
            armor_used = defender.armor
            mitigated = raw_damage * (100 / (100 + armor_used))

        elif damage_type == "magic":
            resist_used = defender.magic_resistance
            mitigated = raw_damage * (100 / (100 + resist_used))

        else:  # true damage
            mitigated = raw_damage

        final_damage = max(0, int(mitigated))

        return DamageResult(
            raw_damage=raw_damage,
            mitigated_damage=int(mitigated),
            final_damage=final_damage,
            armor_used=armor_used,
            resist_used=resist_used,
            crit=False,
            blocked=False
        )