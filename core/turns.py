class TurnManager:
    def __init__(self, player, enemy, rules=None):
        self.player = player
        self.enemy = enemy
        self.rules = rules if rules else []
        self.phase = "PRE_BATTLE"
        self.turn = 1

        # Применяем правила в начале боя
        for rule in self.rules:
            rule.apply(self.player, self.enemy)

    def execute_phase(self):
        if self.phase == "PRE_BATTLE":
            print(f"Фаза подготовки к бою. Ход {self.turn}")
        elif self.phase == "PLAYER_TURN":
            print("Ход игрока")
        elif self.phase == "ENEMY_TURN":
            print("Ход врага")
        elif self.phase == "RESOLVE":
            print("Разрешение действий")
        elif self.phase == "END_BATTLE":
            print("Бой завершён")
        else:
            print(f"Неизвестная фаза: {self.phase}")
            