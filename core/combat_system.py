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
        else:
            mitigated = raw_damage

        final_damage = max(0, int(mitigated))

        return DamageResult(
            source=attacker,
            target=defender,
            raw_damage=raw_damage,
            final_damage=final_damage,
            damage_type=damage_type,
            is_crit=False,
            reduced_by_armor=armor_used if damage_type == "physical" else resist_used
        )
