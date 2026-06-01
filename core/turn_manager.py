class TurnManager:
    def __init__(self, entities, action_system, battle_log, decision_system, status_system):
        self.entities = entities
        self.action_system = action_system
        self.battle_log = battle_log
        self.decision_system = decision_system
        self.status_system = status_system
        self.turn_index = 0

    # -------------------------
    # MAIN LOOP STEP
    # -------------------------
    def process_turn(self):
        if self.is_battle_over():
            self.battle_log.add("Battle ended", type="SYSTEM")
            return

        actor = self.get_current_actor()

        if not self._is_alive(actor):
            self.advance_turn()
            return

        # TURN START
        self.battle_log.turn_start(self.turn_index + 1, actor)
        self.status_system.trigger("on_turn_start", actor)

        # DECISION
        action = self.decision_system.get_action(actor, self.entities)

        if action is None:
            self.battle_log.add(f"{actor.name} skips turn", type="SKIP")
            self.status_system.trigger("on_turn_end", actor)
            self.advance_turn()
            return

        # EXECUTION
        result = self.action_system.execute(action)

        if result:
            result.apply()

            # DAMAGE HOOK
            self.status_system.trigger("on_damage", result.target, result)
            self.battle_log.log_damage(result)

            # DEATH HOOK
            if self._is_dead(result.target):
                self.status_system.trigger("on_death", result.target)
                self.battle_log.add(f"{result.target.name} died", type="DEATH")

        # CHECK END AFTER ACTION
        if self.is_battle_over():
            self.battle_log.add("Battle ended", type="SYSTEM")
            return

        # TURN END
        self.status_system.trigger("on_turn_end", actor)
        self.advance_turn()

    # -------------------------
    # TURN CONTROL
    # -------------------------
    def get_current_actor(self):
        alive_entities = [e for e in self.entities if self._is_alive(e)]
        if not alive_entities:
            return None
        return alive_entities[self.turn_index % len(alive_entities)]

    def advance_turn(self):
        self.turn_index += 1

    # -------------------------
    # BATTLE STATE
    # -------------------------
    def is_battle_over(self):
        alive_factions = set()

        for entity in self.entities:
            if self._is_alive(entity):
                alive_factions.add(getattr(entity, "faction", None))

        return len(alive_factions) <= 1

    # -------------------------
    # LIVING CHECKS
    # -------------------------
    def _is_alive(self, entity):
        return getattr(entity, "hp", 0) > 0

    def _is_dead(self, entity):
        return getattr(entity, "hp", 0) <= 0