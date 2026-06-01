class StatusSystem:
    def __init__(self):
        self.statuses = {}

    def _entity_key(self, entity):
        if hasattr(entity, 'id'):
            return entity.id
        if hasattr(entity, 'name'):
            return entity.name
        return id(entity)

    def add_status(self, entity, status):
        self.statuses.setdefault(self._entity_key(entity), []).append(status)

    def trigger(self, event_name, entity, payload=None):
        for status in self.statuses.get(self._entity_key(entity), []):
            hook = getattr(status, event_name, None)
            if hook:
                hook(payload or entity)

    def cleanup(self, entity):
        self.statuses[self._entity_key(entity)] = [
            s for s in self.statuses.get(self._entity_key(entity), [])
            if not s.is_expired()
        ]
