from core.combat_system import CombatSystem

class ActionSystem:
    def execute_ability(self, attacker, target, ability):
        return CombatSystem.calculate_damage(
            attacker,
            target,
            getattr(ability, 'damage', 0),
            damage_type=getattr(ability, 'damage_type', 'physical')
        )

    def execute(self, action):
        if action is None:
            return None

        action_type = action.get('type')
        attacker = action.get('source')
        target = action.get('target')

        if action_type == 'attack':
            base_damage = getattr(attacker, 'dmg', 0)
            return CombatSystem.calculate_damage(
                attacker,
                target,
                base_damage,
                damage_type='physical'
            )

        if action_type == 'ability':
            ability = action.get('ability')
            if ability is None:
                return None
            return self.execute_ability(attacker, target, ability)

        return None
