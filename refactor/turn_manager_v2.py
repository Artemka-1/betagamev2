from core.action_system import ActionSystem
from core.targeting_system import TargetingSystem
from core.battle_log import BattleLog
from core.status_system import StatusSystem


class TurnManager:
    

    def __init__(self, entities, battle_log):
        self.entities = entities
        self.battle_log = battle_log
        self.action_system = ActionSystem()
        self.turn_index = 0

    def process_turn(self):
        if self.is_battle_over():
            return

        actor = self.get_current_actor()

        if not actor.is_alive():
            self.advance_turn()
            return

        self.battle_log.turn_start(self.turn_index + 1, actor.name)

        target = TargetingSystem.select_target(actor, self.entities)
        damage = self.action_system.execute(actor, target)

        self.battle_log.action(damage)

        self.end_turn(actor)
        self.advance_turn()

    def get_current_actor(self):
        return self.entities[self.turn_index % len(self.entities)]

    def end_turn(self, actor):
        StatusSystem.end_turn(actor)

    def advance_turn(self):
        self.turn_index += 1

    def is_battle_over(self):
        teams_alive = set(e.faction for e in self.entities if e.is_alive())
        return len(teams_alive) <= 1
