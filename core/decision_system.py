class DecisionSystem:
    def __init__(
        self,
        player_input_system=None,
        interactive: bool = False,
        player_action_callback=None,
    ):
        self.player_input = player_input_system
        self.interactive = interactive
        self.player_action_callback = player_action_callback

    def get_action(self, actor, entities):
        enemies = [e for e in entities if e is not actor and e.hp > 0]
        if not enemies:
            return None

        if getattr(actor, "is_player", False):
            if self.interactive and callable(self.player_action_callback):
                return self.player_action_callback(actor, enemies)
            if self.player_input:
                return self.player_input.get_action(actor, enemies)
            raise ValueError(
                "Player action callback or input system is required for interactive player control"
            )

        return {
            "type": "attack",
            "source": actor,
            "target": enemies[0],
            "base_damage": actor.stats.get("attack", 0)
        }
