# core/turns.py

class TurnManager:
    def __init__(self, entities, battle_log):
        """
        Управляет порядком ходов и одним полным ходом боя.
        """
        self.entities = entities
        self.battle_log = battle_log

        self.turn = 1
        self.queue = self._build_turn_queue()
        self.current_index = 0

    # ---------- Setup ----------

    def _build_turn_queue(self):
        """Начальная очередь ходов"""
        return [e for e in self.entities if e.is_alive()]

    # ---------- State ----------

    def is_battle_over(self):
        """Бой окончен, если осталась 1 или 0 живых сущностей"""
        return len([e for e in self.queue if e.is_alive()]) <= 1

    # ---------- Turn Flow ----------

    def process_turn(self):
        """Один полный ход одного актёра"""
        if self.is_battle_over():
            return

        actor = self._get_current_actor()
        if actor is None or not actor.is_alive():
            self._advance_turn()
            return

        target = self._select_target(actor)
        if target is None:
            self._advance_turn()
            return

        # лог начала хода
        self.battle_log.turn_start(self.turn, actor.name)

        # действие
        self._execute_action(actor, target)

        # тики кулдаунов
        actor.tick_cooldowns()

        # смерть цели
        if not target.is_alive():
            self.battle_log.death(target.name)

        self._advance_turn()

    # ---------- Internals ----------

    def _get_current_actor(self):
        if not self.queue:
            return None
        return self.queue[self.current_index]

    def _select_target(self, actor):
        alive_targets = [
            e for e in self.queue
            if e.is_alive() and e != actor
        ]
        return alive_targets[0] if alive_targets else None

    def _execute_action(self, actor, target):
        # попытка использовать способность
        if actor.abilities:
            available = actor.get_available_abilities()
            if available:
                ability = available[0]
                try:
                    result = actor.use_ability(ability.name, target)
                    self.battle_log.action(result)
                    return
                except Exception:
                    pass  # fallback на обычную атаку

        # обычная атака
        damage = actor.attack(target)
        self.battle_log.action(
            f"{actor.name} attacks {target.name} for {damage} damage!"
        )

    def _advance_turn(self):
        """Переход к следующему ходу"""
        self.current_index += 1

        if self.current_index >= len(self.queue):
            self.current_index = 0
            self.turn += 1

        # чистим мёртвых
        self.queue = [e for e in self.queue if e.is_alive()]