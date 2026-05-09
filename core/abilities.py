from typing import Callable

AbilityAction = Callable[[object, object, object], str]


class Ability:
    def __init__(
        self,
        name: str,
        cost: int,
        cooldown: int,
        description: str,
        action: AbilityAction,
        damage_type: str = "physical"
    ):
        self.name = name
        self.cost = cost
        self.cooldown = cooldown
        self.description = description
        self.action = action
        self.damage_type = damage_type

    def use(self, user, target) -> str:
        """Execute the ability action"""
        return self.action(user, target, self)


# ============================================
# AGILITY
# ============================================

def blade_dance(user, target, ability):
    """4 quick strikes"""
    hits = 4
    total = 0

    for _ in range(hits):
        dmg = int(user.dmg * 0.9)
        damage = target.receive_damage(dmg, damage_type=ability.damage_type)
        total += damage

    return f"{user.name} использует {ability.name} и наносит {total} урона {target.name}!"


def storm_slashes(user, target, ability):
    """12 quick strikes"""
    hits = 12
    total = 0

    for _ in range(hits):
        dmg = int(user.dmg * 0.8)
        damage = target.receive_damage(dmg, damage_type=ability.damage_type)
        total += damage

    return f"{user.name} использует {ability.name} и наносит {total} урона {target.name}!"


# ============================================
# STRENGTH
# ============================================

def barbarian_touch(user, target, ability):
    """Powerful strike"""
    dmg = int(user.dmg * 1.5)
    damage = target.receive_damage(dmg, damage_type=ability.damage_type)
    return f"{user.name} использует {ability.name} и наносит {damage} урона {target.name}!"


def royal_roar(user, target, ability):
    """Stunning strike"""
    dmg = int(user.dmg * 1.7)
    damage = target.receive_damage(dmg, damage_type=ability.damage_type)
    return f"{user.name} использует {ability.name} и наносит {damage} урона {target.name}!"


# ============================================
# MAGIC - Maluk
# ============================================

def fireball(user, target, ability):
    """Explosive fireball"""
    hits = 3
    total = 0
    
    for _ in range(hits):
        dmg = int(user.dmg * 1.2)
        damage = target.receive_damage(dmg, damage_type=ability.damage_type)
        total += damage
    
    return f"{user.name} использует {ability.name} и наносит {total} урона {target.name}!"


def ice_storm(user, target, ability):
    """Freezing ice storm"""
    hits = 8
    total = 0
    
    for _ in range(hits):
        dmg = int(user.dmg * 1.0)
        damage = target.receive_damage(dmg, damage_type=ability.damage_type)
        total += damage
    
    return f"{user.name} использует {ability.name} и наносит {total} урона {target.name}!"


# ============================================
# STRENGTH - Morok
# ============================================

def crushing_blow(user, target, ability):
    """Massive crushing attack"""
    dmg = int(user.dmg * 1.8)
    damage = target.receive_damage(dmg, damage_type=ability.damage_type)
    return f"{user.name} использует {ability.name} и наносит {damage} урона {target.name}!"


def earthquake(user, target, ability):
    """Devastating earthquake"""
    dmg = int(user.dmg * 1.4)
    damage = target.receive_damage(dmg, damage_type=ability.damage_type)
    return f"{user.name} использует {ability.name} и наносит {damage} урона {target.name}!"


# ============================================
# MAGIC - Paradox
# ============================================

def arcane_bolt(user, target, ability):
    """Quick arcane projectile"""
    hits = 2
    total = 0
    
    for _ in range(hits):
        dmg = int(user.dmg * 1.3)
        damage = target.receive_damage(dmg, damage_type=ability.damage_type)
        total += damage
    
    return f"{user.name} использует {ability.name} и наносит {total} урона {target.name}!"


def time_warp(user, target, ability):
    """Temporal distortion"""
    dmg = int(user.dmg * 1.6)
    damage = target.receive_damage(dmg, damage_type=ability.damage_type)
    return f"{user.name} использует {ability.name} и наносит {damage} урона {target.name}!"




# ============================================
# FACTORIES
# ============================================

def create_blade_dance():
    return Ability(
        name="Blade Dance",
        cost=15,
        cooldown=2,
        description="4 быстрых удара",
        action=blade_dance,
        damage_type="physical"
    )


def create_storm_slashes():
    return Ability(
        name="Storm Slashes",
        cost=25,
        cooldown=3,
        description="12 быстрых ударов",
        action=storm_slashes,
        damage_type="physical"
    )


def create_barbarian_touch():
    return Ability(
        name="Barbarian Touch",
        cost=30,
        cooldown=3,
        description="Мощный удар",
        action=barbarian_touch,
        damage_type="magic"
    )


def create_royal_roar():
    return Ability(
        name="Royal Roar",
        cost=35,
        cooldown=4,
        description="Оглушающий удар",
        action=royal_roar,
        damage_type="magic"
    )


def create_fireball():
    return Ability(
        name="Fireball",
        cost=28,
        cooldown=2,
        description="Взрывное огненное кольцо",
        action=fireball,
        damage_type="magic"
    )


def create_ice_storm():
    return Ability(
        name="Ice Storm",
        cost=32,
        cooldown=3,
        description="Ледяной шторм",
        action=ice_storm,
        damage_type="magic"
    )


def create_crushing_blow():
    return Ability(
        name="Crushing Blow",
        cost=32,
        cooldown=3,
        description="Сокрушающий удар",
        action=crushing_blow,
        damage_type="physical"
    )


def create_earthquake():
    return Ability(
        name="Earthquake",
        cost=38,
        cooldown=4,
        description="Землетрясение",
        action=earthquake,
        damage_type="physical"
    )


def create_arcane_bolt():
    return Ability(
        name="Arcane Bolt",
        cost=20,
        cooldown=2,
        description="Быстрый магический снаряд",
        action=arcane_bolt,
        damage_type="magic"
    )


def create_time_warp():
    return Ability(
        name="Time Warp",
        cost=40,
        cooldown=5,
        description="Искажение времени",
        action=time_warp,
        damage_type="magic"
    )