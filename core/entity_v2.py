from core import abilities
import random


class EntityV2:
    def __init__(
        self,
        name,
        hp,
        dmg,
        char_class=None,
        faction=None,
        armor=0,
        magic_resistance=0.0,
        od=0,
        od_max=10,
        abilities=None,
        combat_system=None
    ):
        self.name = name
        self.max_hp = hp
        self.hp = hp

        self.dmg = dmg
        self.char_class = char_class
        self.faction = faction

        self.armor = armor
        self.magic_resistance = magic_resistance

        self.od_max = od_max
        self.od = od if od != 0 else od_max

        self.combat_system = combat_system

        # abilities system
        self.abilities = []
        self.cooldowns = {}

        self.add_abilities(abilities or [])

    # -----------------------------
    # ABILITIES
    # -----------------------------

    def add_abilities(self, abilities_list):
        self.abilities.extend(abilities_list)
        for ability in abilities_list:
            self.cooldowns[ability.name] = 0

    def get_available_abilities(self):
        return [
            ability for ability in self.abilities
            if self.can_use_ability(ability.name)
        ]

    def has_ability(self, ability_name):
        return any(a.name == ability_name for a in self.abilities)

    def _resolve_ability(self, ability_identifier):
        if ability_identifier is None:
            return None

        if hasattr(ability_identifier, "name"):
            ability_name = ability_identifier.name
        else:
            ability_name = ability_identifier

        return next((a for a in self.abilities if a.name == ability_name), None)

    def can_use_ability(self, ability_name):
        ability = self._resolve_ability(ability_name)
        if not ability:
            return False

        return (
            self.can_use_skill(ability.cost)
            and self.cooldowns.get(ability.name, 0) == 0
        )

    def use_ability(self, ability_name, target):
        ability = self._resolve_ability(ability_name)

        if ability is None:
            raise ValueError(f"Ability '{ability_name}' not found for {self.name}")

        if self.cooldowns.get(ability.name, 0) > 0:
            raise ValueError(f"Ability '{ability.name}' is on cooldown")

        if not self.spend_od(ability.cost):
            raise ValueError(f"Not enough OD for {ability.name}")

        self.cooldowns[ability.name] = ability.cooldown
        return ability.use(self, target)

    def get_ability_cooldown(self, ability_name):
        return self.cooldowns.get(ability_name, 0)

    def tick_cooldowns(self):
        for key in self.cooldowns:
            self.cooldowns[key] = max(0, self.cooldowns[key] - 1)

    # -----------------------------
    # COMBAT
    # -----------------------------

    def attack(self, target):
        if self.combat_system is None:
            raise ValueError(f"{self.name} has no combat_system assigned")

        damage = self.combat_system.deal_damage(
            self,
            target,
            self.dmg,
            "physical"
        )

        self.gain_od(15)
        target.gain_od(5)

        return damage

    def receive_damage(self, damage, damage_type="physical", attacker=None):
        if attacker and self.try_parry(attacker):
            return 0  # парри сработал, урон отражён

        if damage_type == "magic":
            reduced = damage * (1 - self.magic_resistance)
        elif damage_type == "physical":
            reduced = damage * (1 - self.armor / 100)
        else:
            reduced = damage

        final_damage = max(0, int(reduced))

        # 👉 ОД даём ПОСЛЕ расчёта урона
        if final_damage > 0:
            self.gain_od(10)

        self.hp -= final_damage
        return final_damage

    def is_alive(self):
        return self.hp > 0

    # -----------------------------
    # OD SYSTEM
    # -----------------------------

    def gain_od(self, amount):
        self.od = min(self.od_max, self.od + amount)

    def spend_od(self, amount):
        if self.od >= amount:
            self.od -= amount
            return True
        return False

    def can_use_skill(self, cost):
        return self.od >= cost

    # -----------------------------
    # DEFENSIVE MECHANIC
    # -----------------------------

    def try_parry(self, attacker):
        if self.name != "Mael":
            return False

        if random.random() <= 0.17:
            damage = random.randint(3800, 4400)
            attacker.receive_damage(damage, "physical")
            return True

        return False

    # -----------------------------
    # AI / TURN SYSTEM
    # -----------------------------

    def request_action(self, target):
        if self.faction == "Players":
            return self._request_player_action(target)

        available = self.get_available_abilities()

        if available:
            ability = available[0]
            return {
                "type": "ability",
                "ability": ability.name,
                "target": target
            }

        return {
            "type": "attack",
            "target": target
        }

    def _request_player_action(self, target):
        available = self.get_available_abilities()

        print(f"\n[PLAYER TURN] {self.name}")
        print(f"HP: {self.hp}/{self.max_hp}, OD: {self.od}/{self.od_max}")
        print(f"Target: {target.name} (HP: {target.hp})")

        print("Choose action:")
        for index, ability in enumerate(available, start=1):
            cooldown = self.cooldowns.get(ability.name, 0)
            print(
                f"{index}. {ability.name} (cost {ability.cost}, cooldown {cooldown})"
            )
        print(f"{len(available) + 1}. Attack")

        while True:
            choice = input("Enter action number: ").strip()
            if not choice.isdigit():
                print("Please enter a valid number.")
                continue

            index = int(choice)
            if 1 <= index <= len(available):
                return {
                    "type": "ability",
                    "ability": available[index - 1].name,
                    "target": target
                }
            if index == len(available) + 1:
                return {
                    "type": "attack",
                    "target": target
                }

            print("Choice out of range. Try again.")
