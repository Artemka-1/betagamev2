class BattleLog:
    def __init__(self):
        self.events = []

    def phase_start(self, turn, phase):
        self.add(f"Ход {turn}: начинается фаза {phase}", type="TURN")

    def add(self, text, type="INFO"):
        self.events.append(f"[{type}] {text}")

    def battle_start(self):
        self.add("Бой начался", type="BATTLE")

    def turn_start(self, turn_number, actor):
        actor_type = "Игрок" if getattr(actor, "is_player", False) else "Противник"
        self.add(f"Ход {turn_number}: {actor_type} {actor.name} начинает ход", type="TURN")

    def action(self, text):
        self.add(text, type="ACTION")

    def log_damage(self, result):
        if result.final_damage <= 0:
            self.add(f"{result.source.name} атаковал {result.target.name}, но не нанес урона", type="DAMAGE")
            return

        damage_type_text = {
            "physical": "физического",
            "magic": "магического"
        }.get(result.damage_type, "прямого")

        self.add(
            f"{result.source.name} атаковал {result.target.name} и нанес {result.final_damage} {damage_type_text} урона",
            type="DAMAGE"
        )

    def death(self, entity_name):
        self.add(f"{entity_name} погиб", type="DEATH")

    def battle_end(self):
        self.add("Бой завершён", type="BATTLE")

    def __str__(self):
        return "\n".join(self.events)
