class EntityV2:
    def __init__(self, name, hp, dmg, char_class=None, faction=None,
                 armor=0, magic_resistance=0.0, od=0, od_max=100, abilities=None):

        self.name = name
        self.max_hp = hp
        self.hp = hp

        self.dmg = dmg
        self.char_class = char_class
        self.faction = faction

        self.armor = armor
        self.magic_resistance = magic_resistance
        self.od = 100 if od == 0 else od
        self.od_max = od_max
        self._set_abilities(abilities or [])

    def _set_abilities(self, abilities):
        """Set abilities and initialize cooldowns"""
        self.abilities = abilities
        self.cooldowns = {ability.name: 0 for ability in self.abilities}

    def add_abilities(self, abilities):
        """Add abilities after initialization"""
        self.abilities.extend(abilities)
        for ability in abilities:
            self.cooldowns[ability.name] = 0

    def is_alive(self):
        return self.hp > 0

    def attack(self, target):
        raw_damage = self.dmg
        final_damage = target.receive_damage(raw_damage, damage_type="physical")
        self.gain_od(15)
        target.gain_od(5)
        return final_damage

    def receive_damage(self, damage, damage_type: str = "physical"):
        if damage_type == "magic":
            reduced = damage * (1 - self.magic_resistance)
        elif damage_type == "physical":
            reduced = damage * (1 - self.armor / 100)
        else:
            reduced = damage

        reduced = max(0, int(reduced))
        self.hp -= reduced
        return reduced
    
    def get_available_abilities(self):
        return [ability for ability in self.abilities
                if self.can_use_skill(ability.cost) and self.cooldowns.get(ability.name, 0) == 0]

    def has_ability(self, ability_name):
        return any(ability.name == ability_name for ability in self.abilities)

    def can_use_ability(self, ability_name):
        ability = next((ability for ability in self.abilities if ability.name == ability_name), None)
        if ability is None:
            return False
        return self.can_use_skill(ability.cost) and self.cooldowns.get(ability.name, 0) == 0

    def use_ability(self, ability_name, target):
        ability = next((ability for ability in self.abilities if ability.name == ability_name), None)
        if ability is None:
            raise ValueError(f"Ability '{ability_name}' not found for {self.name}")
        if self.cooldowns.get(ability.name, 0) > 0:
            raise ValueError(f"Ability '{ability.name}' is on cooldown")
        if not self.spend_od(ability.cost):
            raise ValueError(f"Недостаточно ОД для использования {ability.name}")

        self.cooldowns[ability.name] = ability.cooldown
        return ability.use(self, target)

    def get_ability_cooldown(self, ability_name):
        return self.cooldowns.get(ability_name, 0)

    def tick_cooldowns(self):
        for key in self.cooldowns:
            self.cooldowns[key] = max(0, self.cooldowns[key] - 1)

    def gain_od(self, amount):
        self.od = min(self.od_max, self.od + amount)

    def spend_od(self, amount):
        if self.od >= amount:
            self.od -= amount
            return True
        return False

    def can_use_skill(self, cost):
        return self.od >= cost