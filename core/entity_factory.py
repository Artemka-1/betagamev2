from core.entity_v2 import EntityV2


def create_battle():
    mael = EntityV2(
        entity_id="mael",
        name="Mael",
        max_hp=28500,
        armor=17,
        magic_resistance=21,
        od_max=100,
        faction="Players",
        char_class="Agility",
        stats={
            "attack": 1000,
            "speed": 15
        },
        is_player=True
    )

    vasarax = EntityV2(
        entity_id="vasarax",
        name="VasaraX",
        max_hp=53000,
        armor=32,
        magic_resistance=18,
        od_max=100,
        faction="Enemies",
        char_class="Strength",
        stats={
            "attack": 900,
            "speed": 8
        }
    )

    maluk = EntityV2(
        entity_id="maluk",
        name="Maluk",
        max_hp=31000,
        armor=9,
        magic_resistance=29,
        od_max=100,
        faction="Enemies",
        char_class="Magic",
        stats={
            "attack": 750,
            "speed": 10
        }
    )

    return [mael, vasarax, maluk]