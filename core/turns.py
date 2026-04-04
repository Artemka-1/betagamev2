# core/turns.py
class TurnManager:
    def __init__(self, players, enemies, rules=None):
        self.players = players  # список игроков
        self.enemies = enemies  # список врагов
        self.rules = rules or []

        self.turn = 1
        self.phase = "PLAYER_TURN"

    def get_alive(self, entities):
        return [e for e in entities if e.is_alive()]

    def all_dead(self, entities):
        return len(self.get_alive(entities)) == 0

    def next_phase(self):
        if self.phase == "PLAYER_TURN":
            self.phase = "ENEMY_TURN"
        elif self.phase == "ENEMY_TURN":
            self.phase = "RESOLVE"
        elif self.phase == "RESOLVE":
            self.turn += 1
            if self.get_alive(self.players) and self.get_alive(self.enemies):
                self.phase = "PLAYER_TURN"
            else:
                self.phase = "END_BATTLE"

    def apply_rules(self, actor, target):
        for rule in self.rules:
            rule.apply(actor, target)

    
    def is_battle_over(self):
        if not self.get_alive(self.players):
            self.phase = "END_BATTLE"
            return True
        if not self.get_alive(self.enemies):
            self.phase = "END_BATTLE"
            return True
        return False

    