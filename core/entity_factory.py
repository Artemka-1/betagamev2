from core.entity_v2 import EntityV2

def create_entity_from_roster(data: dict) -> EntityV2:
    return EntityV2(
        name=data["name"],
        hp=data["hp"],
        dmg=data["base_damage"],
        char_class=data.get("class"),
        faction=data.get("faction")
    )