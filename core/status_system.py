class StatusSystem:
    @staticmethod
    def end_turn(entity):
        entity.regen_od()
        entity.tick_statuses()
