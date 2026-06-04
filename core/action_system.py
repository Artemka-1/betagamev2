from core.combat_system import CombatSystem

class ActionSystem:
    def __init__(self, combat_system: CombatSystem):
        self.combat_system = combat_system

    def execute(self, action):
        if not action:
            return None

        action_type = action["type"]

        if action_type == "attack":
            return self.combat_system.calculate_damage(
                source=action["source"],
                target=action["target"]
            )

        if action_type == "ability":
            ability = action["ability"]
            return ability.execute(action)

        raise ValueError(f"Unknown action type: {action_type}")
