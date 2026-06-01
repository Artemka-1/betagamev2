class EntityV2:
    def __init__(
        self,
        entity_id: str | None = None,
        name: str | None = None,
        max_hp: int = 0,
        armor: int = 0,
        magic_resistance: int = 0,
        od_max: int = 0,
        faction: str | None = None,
        char_class: str | None = None,
        stats: dict | None = None,
        is_player: bool = False,
        **kwargs,
    ):
        self.id = entity_id if entity_id is not None else kwargs.get('id')
        self.name = name if name is not None else kwargs.get('name')
        self.is_player = is_player or kwargs.get('is_player', False)

        self.max_hp = max_hp
        self.hp = max_hp

        self.base_armor = armor
        self.armor = armor
        self.magic_resistance = magic_resistance

        self.od_max = od_max
        self.od = od_max

        self.faction = faction
        self.char_class = char_class

        self.stats = stats or {}
        self.dmg = self.stats.get('attack', kwargs.get('dmg', 10) or 10)
        self.speed = self.stats.get('speed', 0)
        self.abilities = []
        self.statuses = []

    def __str__(self):
        return self.name if self.name else super().__str__()

    def __repr__(self):
        return f"<EntityV2 {self.name} id={self.id}>"

    @property
    def alive(self) -> bool:
        return self.hp > 0

    def is_alive(self) -> bool:
        return self.hp > 0

    def apply_damage(self, damage_result) -> None:
        self.hp = max(0, self.hp - damage_result.final_damage)

    def add_abilities(self, abilities):
        self.abilities.extend(abilities)
        return self

    def request_action(self, target):
        if self.abilities:
            return {'type': 'ability', 'ability': self.abilities[0].name, 'target': target}
        return {'type': 'attack'}

    def attack(self, target):
        if getattr(self, 'combat_system', None):
            result = self.combat_system.calculate_damage(self, target, self.dmg, 'physical')
            target.apply_damage(result)
            return result.final_damage

        damage = self.dmg
        target.hp = max(0, target.hp - damage)
        return damage

    def use_ability(self, ability_name, target):
        for ability in self.abilities:
            if ability.name == ability_name:
                return ability.use(self, target)
        return f"{self.name} tries to use {ability_name} but fails"

    def receive_damage(self, base_damage: int, damage_type: str = 'physical') -> int:
        if damage_type == 'physical':
            mitigated = base_damage * (100 / (100 + self.armor))
        elif damage_type == 'magic':
            mitigated = base_damage * (100 / (100 + self.magic_resistance))
        else:
            mitigated = base_damage
        final_damage = max(0, int(mitigated))
        self.hp = max(0, self.hp - final_damage)
        return final_damage

    def regen_od(self, amount: int = 1) -> None:
        self.od = min(self.od_max, self.od + amount)

    def tick_statuses(self) -> None:
        pass
