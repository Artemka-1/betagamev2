
#log of battle events, such as damage dealt, status effects applied
# core/battle_log.py
class BattleLog:
    def __init__(self):
        self.events = []

    # запись в лог
    def phase_start(self, turn, phase):
        self.add(f"[Turn {turn}] Phase start: {phase}")

    def add(self, text):
        self.events.append(text)

    # методы интерфейса
    def battle_start(self, turn):
        self.add(f"[Turn {turn}] Battle started")

    def turn_start(self, turn, actor_name):
        self.add(f"[Turn {turn}] Turn start: {actor_name}")

    def action(self, turn, text):
        self.add(f"[Turn {turn}] {text}")

    def death(self, turn, entity_name):
        self.add(f"[Turn {turn}] {entity_name} died")

    def battle_end(self, turn):
        self.add(f"[Turn {turn}] Battle ended")

    def __str__(self):
        return "\n".join(self.events)