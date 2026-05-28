



class EntityV2:
    def __init__(
        self,
        name: str,
        hp: int,
        dmg: int,
        armor: int = 0,
        magic_resistance: float = 0.0,
        od_max: int = 10,
        faction: str | None = None,
        char_class: str | None = None,
        abilities: list | None = None,
        combat_system=None,
    ):
        self.name = name

        self.max_hp = hp
        self.hp = hp
        self.dmg = dmg

        self.armor = armor
        self.magic_resistance = magic_resistance

        self.od_max = od_max
        self.od = od_max

        self.faction = faction
        self.char_class = char_class

        self.statuses: list = []
        self.abilities = abilities or []
        self.combat_system = combat_system

    # -----------------------------
    # STATE ONLY
    # -----------------------------

    def is_alive(self) -> bool:
        return self.hp > 0

    def apply_damage(self, damage_result) -> None:
        """Entity РЅРµ СЃС‡РёС‚Р°РµС‚ СѓСЂРѕРЅ, Р° С‚РѕР»СЊРєРѕ РїСЂРёРјРµРЅСЏРµС‚ РіРѕС‚РѕРІС‹Р№ СЂРµР·СѓР»СЊС‚Р°С‚"""
        self.hp = max(0, self.hp - damage_result.final_damage)

    def add_abilities(self, abilities):
        self.abilities.extend(abilities)
        return self
    def request_action(self, target):
        if self.abilities:
            return {"type": "ability", "ability": self.abilities[0].name, "target": target}
        return {"type": "attack"}

    def attack(self, target):
        if self.combat_system:
            result = self.combat_system.calculate_damage(self, target, self.dmg, "physical")
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

    def receive_damage(self, base_damage: int, damage_type: str = "physical") -> int:
        if damage_type == "physical":
            mitigated = base_damage * (100 / (100 + self.armor))
        elif damage_type == "magic":
            mitigated = base_damage * (100 / (100 + self.magic_resistance))
        else:
            mitigated = base_damage
        final_damage = max(0, int(mitigated))
        self.hp = max(0, self.hp - final_damage)
        return final_damage

    def regen_od(self, amount: int = 1) -> None:
        self.od = min(self.od_max, self.od + amount)

    def tick_statuses(self) -> None:
        # Placeholder for status effect processing
        pass


