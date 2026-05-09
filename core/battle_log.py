#log of battle events
class BattleLog:
    def __init__(self):
        self.events = []

    def phase_start(self, turn, phase):
        self.add(f"[Turn {turn}] Phase start: {phase}")

    def add(self, text, type="INFO"):
        self.events.append(f"[{type}] {text}")

    def battle_start(self):
        self.add("Battle started", type="BATTLE")

    def turn_start(self, turn, actor_name):
        self.add(f"[Turn {turn}] {actor_name} starts turn", type="TURN")

    def action(self, text):
        self.add(text, type="ACTION")

    def death(self, entity_name):
        self.add(f"{entity_name} died", type="DEATH")

    def battle_end(self):
        self.add("Battle ended", type="BATTLE")

    def __str__(self):
        return "\n".join(self.events)
