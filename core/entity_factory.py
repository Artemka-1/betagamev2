from core.entity_v2 import EntityV2
from core.abilities import (
    create_blade_dance,
    create_storm_slashes,
    create_barbarian_touch,
    create_royal_roar,
    create_fireball,
    create_ice_storm,
    create_crushing_blow,
    create_earthquake,
    create_arcane_bolt,
    create_time_warp
)


def create_entity_from_roster(data: dict) -> EntityV2:
    return EntityV2(
        name=data["name"],
        hp=data["hp"],
        dmg=data["base_damage"],
        char_class=data.get("class"),
        faction=data.get("faction"),
        armor=data.get("armor", 0),
        magic_resistance=data.get("magic_resistance", 0.0),
        abilities=data.get("abilities", [])
    )


def create_battle():
    """Create and return all entities for a battle"""
    # Player entities
    mael = EntityV2(
        name="Mael",
        hp=28500,
        dmg=1000,
        armor=17,
        magic_resistance=0.21,
        char_class="Agility",
        faction="Players"
    )
    mael.add_abilities([
        create_blade_dance(),
        create_storm_slashes(),
    ])
    
    # Enemy entities
    vasarax = EntityV2(
        name="VasaraX",
        hp=53000,
        dmg=900,
        armor=32,
        magic_resistance=0.18,
        char_class="Strength",
        faction="Enemies"
    )
    vasarax.add_abilities([
        create_barbarian_touch(),
        create_royal_roar(),
    ])
    
    maluk = EntityV2(
        name="Maluk",
        hp=31000,
        dmg=750,
        armor=9,
        magic_resistance=0.29,
        char_class="Magic",
        faction="Enemies"
    )
    
    morok = EntityV2(
        name="Morok",
        hp=30000,
        dmg=950,
        armor=18,
        magic_resistance=0.19,
        char_class="Strength",
        faction="Enemies"
    )
    
    paradox = EntityV2(
        name="Paradox",
        hp=34000,
        dmg=800,
        armor=7,
        magic_resistance=0.31,
        char_class="Magic",
        faction="Enemies"
    )
    
    # Return all entities
    return [mael, vasarax, maluk, morok, paradox]
    