# core/combat_system.py
import random
from core.damage_result import DamageResult

class CombatSystem:
    @staticmethod
    def deal_damage(attacker, target, base_damage, damage_type="physical"):
        if isinstance(base_damage, tuple):
            base_damage = random.randint(*base_damage)

        raw = base_damage

        if damage_type == "physical":
            reduced = base_damage * (1 - target.armor / 100)
        elif damage_type == "magic":
            reduced = base_damage * (1 - target.magic_resistance)
        else:
            reduced = base_damage

        final = max(0, int(reduced))
        reduced_by_armor = raw - final

        return DamageResult(
            raw_damage=raw,
            final_damage=final,
            reduced_by_armor=reduced_by_armor,
            log=[]
        )