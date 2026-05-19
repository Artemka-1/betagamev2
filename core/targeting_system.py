class TargetingSystem:
    @staticmethod
    def select_target(actor, entities):
        enemies = [
            e for e in entities
            if e.faction != actor.faction and e.is_alive()
        ]
        return enemies[0] if enemies else None
