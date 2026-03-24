def perform_attack(attacker, defender):
    """
    Атакует defender, используя атаку attacker.
    Просто вычитает dmg из hp.
    """
    damage = attacker.dmg
    defender.hp -= damage
    print(f"{attacker.name} наносит {damage} урона {defender.name}. Осталось {defender.hp} HP.")
