from damage_result import DamageResult


class CombatSystem:
    @staticmethod
    def basic_attack(attacker, target):
        log = []

        # 1. base damage
        base = attacker.attack
        log.append(f"Base damage: {base}")

        # 2. modifiers (пока один — strength / power)
        modified = base + attacker.power
        log.append(f"Modified damage: {modified}")

        # 3. crit
        is_crit = False
        if CombatSystem.roll_crit(attacker):
            modified = int(modified * attacker.crit_multiplier)
            is_crit = True
            log.append("Critical hit!")

        # 4. armor mitigation
        reduced = CombatSystem.apply_armor(modified, target.armor)
        final_damage = max(0, modified - reduced)
        if reduced > 0:
            log.append(f"Armor reduced damage by {reduced}")

        return DamageResult(
            raw_damage=modified,
            final_damage=final_damage,
            is_crit=is_crit,
            reduced_by_armor=reduced,
            log=log
        )