class ActionSystem:
    def execute(self, actor, target):
        """
        Выполняет одно действие актёра.
        Возвращает текст для лога.
        """

        action = actor.request_action(target)

        if not action:
            return f"{actor.name} skips turn"

        if action["type"] == "attack":
            damage = actor.attack(target)
            return f"{actor.name} attacks {target.name} for {damage} damage!"

        if action["type"] == "ability":
            ability_name = action["ability"]
            ability_target = action.get("target", target)
            result = actor.use_ability(ability_name, ability_target)
            return result

        return f"{actor.name} does nothing"