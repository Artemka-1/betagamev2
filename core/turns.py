# core/turns.py
class TurnManager:
    def __init__(self, entities, battle_log, rules=None):
        """
        Initialize turn manager.
        entities: list of all entities (players and enemies)
        battle_log: BattleLog instance for recording events
        """
        self.entities = entities  # все сущности
        self.battle_log = battle_log
        self.rules = rules or []

        self.turn = 1
        self.current_entity_index = 0
        self.phase = "BATTLE"

    def get_alive(self, entities=None):
        """Get all alive entities"""
        if entities is None:
            entities = self.entities
        return [e for e in entities if e.is_alive()]

    def all_dead(self, entities=None):
        """Check if all entities are dead"""
        if entities is None:
            entities = self.entities
        return len(self.get_alive(entities)) == 0

    def next_entity(self):
        """Move to next alive entity"""
        alive = self.get_alive()
        if not alive:
            return None
        
        self.current_entity_index = (self.current_entity_index + 1) % len(alive)
        return alive[self.current_entity_index]

    def get_current_entity(self):
        """Get current acting entity"""
        alive = self.get_alive()
        if not alive:
            return None
        return alive[self.current_entity_index % len(alive)]

    def apply_rules(self, actor, target):
        for rule in self.rules:
            rule.apply(actor, target)

    def is_battle_over(self):
        """Check if battle is over"""
        alive = self.get_alive()
        return len(alive) <= 1

    def process_turn(self):
        """Execute one turn of combat"""
        actor = self.get_current_entity()
        if actor is None:
            return
        
        alive = self.get_alive()
        
        # Get list of potential targets (entities other than actor)
        targets = [e for e in alive if e != actor]
        if not targets:
            return
        
        target = targets[0]  # Simple AI: attack first available target
        
        # Log turn start
        self.battle_log.turn_start(self.turn, actor.name)
        
        # Execute attack
        if actor.abilities:
            # If has abilities, try to use one
            available = actor.get_available_abilities()
            if available:
                ability = available[0]
                try:
                    result = actor.use_ability(ability.name, target)
                    self.battle_log.action(result)
                except Exception as e:
                    # Fallback to basic attack
                    damage = actor.attack(target)
                    self.battle_log.action(f"{actor.name} attacks {target.name} for {damage} damage!")
            else:
                # Abilities on cooldown, do basic attack
                damage = actor.attack(target)
                self.battle_log.action(f"{actor.name} attacks {target.name} for {damage} damage!")
        else:
            # No abilities, basic attack
            damage = actor.attack(target)
            self.battle_log.action(f"{actor.name} attacks {target.name} for {damage} damage!")
        
        # Apply cooldown reduction
        actor.tick_cooldowns()
        
        # Check if target died
        if not target.is_alive():
            self.battle_log.death(target.name)
        
        # Move to next entity
        self.next_entity()
