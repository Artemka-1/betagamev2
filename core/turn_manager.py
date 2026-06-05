class TurnManager:
    def __init__(self, entities, action_system, battle_log, decision_system, status_system):
        self.entities = entities
        self.action_system = action_system
        self.battle_log = battle_log
        self.decision_system = decision_system
        self.status_system = status_system

        self.turn_index = 0
        self.turn_number = 1

    # -------------------------
    # CORE HELPERS
    # -------------------------

    def _is_alive(self, entity):
        return entity.hp > 0

    def _alive_entities(self):
        return [e for e in self.entities if e.hp > 0]

    def is_battle_over(self):
        return len(self._alive_entities()) <= 1

    def get_current_actor(self):
        n = len(self.entities)

        for i in range(n):
            idx = (self.turn_index + i) % n
            actor = self.entities[idx]

            if actor.hp > 0:
                self.turn_index = idx
                return actor

        return None

    def advance_turn(self):
        n = len(self.entities)

        for _ in range(n):
            self.turn_index = (self.turn_index + 1) % n
            if self.entities[self.turn_index].hp > 0:
                return

    # -------------------------
    # MAIN LOOP
    # -------------------------

    def process_turn(self):
        if self.is_battle_over():
            self.battle_log.add("Battle ended", type="SYSTEM")
            return

        actor = self.get_current_actor()
        if actor is None:
            return

        # TURN START
        self.battle_log.turn_start(self.turn_number, actor)
        self.status_system.trigger("on_turn_start", actor)

        # DECISION
        action = self.decision_system.get_action(actor, self.entities)

        if action is None:
            self.battle_log.add(f"{actor.name} skips turn", type="SKIP")
            self.status_system.trigger("on_turn_end", actor)
            self.advance_turn()
            self.turn_number += 1
            return

        # EXECUTION
        

        # Ensure attack actions include base_damage (fallback when callbacks omit it)
        if action and action.get("type") == "attack" and "base_damage" not in action:
            try:
                action["base_damage"] = action["source"].stats.get("attack", 0)
            except Exception:
                action["base_damage"] = 0

        

        # Prefer direct combat calculation for attacks to avoid ActionSystem mismatches
        result = None
        if action and action.get("type") == "attack":
            try:
                result = self.action_system.combat_system.calculate_damage(
                    source=action.get("source"),
                    target=action.get("target"),
                    base_damage=action.get("base_damage")
                )
            except Exception:
                result = self.action_system.execute(action)
        else:
            result = self.action_system.execute(action)

        if result:
            target = result.target
            target.hp = max(0, target.hp - result.final_damage)

            self.status_system.trigger("on_damage", target, result)
            self.battle_log.log_damage(result)

            if target.hp <= 0:
                self.status_system.trigger("on_death", target)
                self.battle_log.add(f"{target.name} died", type="DEATH")

        # END CHECK
        if self.is_battle_over():
            self.battle_log.add("Battle ended", type="SYSTEM")
            return

        # TURN END
        self.status_system.trigger("on_turn_end", actor)
        self.advance_turn()
        self.turn_number += 1
       