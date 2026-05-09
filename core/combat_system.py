class CombatSystem:
    @staticmethod
    def deal_damage(attacker, target, base_damage, damage_type="physical", source="attack"):
        """
        Deal damage from attacker to target.
        Returns the actual damage dealt after resistances/armor.
        """
        actual_damage = target.receive_damage(base_damage, damage_type=damage_type)
        return actual_damage
    
    @staticmethod
    def basic_attack(attacker, target):
        """
        Perform a basic attack from attacker to target.
        Returns damage dealt.
        """
        damage = attacker.attack(target)
        return damage