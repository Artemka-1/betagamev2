from typing import Callable

AbilityAction = Callable[[object, object, object], str]

class Ability:
    """
    Класс для представления способности персонажа.
    
    Атрибуты:
        name: Название способности
        cost: Затраты ОД (очки действия)
        cooldown: Перезарядка в ходах
        description: Описание способности
        action: Функция, которая выполняет действие
        damage_type: Тип урона - "physical" (физический) или "magic" (магический)
    """
    def __init__(self, name: str, cost: int, cooldown: int, description: str, action: AbilityAction, damage_type: str = "physical"):
        self.name = name
        self.cost = cost
        self.cooldown = cooldown
        self.description = description
        self.action = action
        self.damage_type = damage_type  # "physical" или "magic"

    def use(self, user, target) -> str:
        return self.action(user, target, self)


# ============================================
# СПОСОБНОСТИ ЛУЧНИКОВ (AGILITY)
# ============================================

def blade_dance(user, target, ability):
    """
    ТАНЕЦ КЛИНКА (Blade Dance)
    Принцип: 4 быстрых удара по цели
    Тип урона: ФИЗИЧЕСКИЙ
    Урон за удар: 90% от атаки
    """
    hits = 4
    total = 0
    for _ in range(hits):
        damage = target.receive_damage(int(user.dmg * 0.9), damage_type=ability.damage_type)
        total += damage
    return f"{user.name} использует Танец клинка и наносит {total} физического урона {target.name}!"


def storm_slashes(user, target, ability):
    """
    БУРЯ СЕЧЕНИЯ (Storm Slashes)
    Принцип: 12 мощных ударов по цели
    Тип урона: ФИЗИЧЕСКИЙ
    Урон за удар: 80% от атаки
    """
    hits = 12
    total = 0
    for _ in range(hits):
        damage = target.receive_damage(int(user.dmg * 0.8), damage_type=ability.damage_type)
        total += damage
    return f"{user.name} применяет Бурю сечения и наносит {total} физического урона {target.name}!"


# ============================================
# СПОСОБНОСТИ РЫЦАРЕЙ (STRENGTH)
# ============================================

def barbarian_touch(user, target, ability):
    """
    КАСАНИЕ ВАРВАРА (Barbarian Touch)
    Принцип: Мощный магический удар, наносящий оглушение
    Тип урона: МАГИЧЕСКИЙ
    Урон: 150% от атаки (регистрируется как магический)
    """
    damage = target.receive_damage(int(user.dmg * 1.5), damage_type=ability.damage_type)
    return f"{user.name} наносит Касание варвара и наносит {damage} магического урона {target.name}!"


def royal_roar(user, target, ability):
    """
    РЫК (Royal Roar)
    Принцип: Мощный магический рык, оглушающий врага
    Тип урона: МАГИЧЕСКИЙ
    Урон: 170% от атаки (регистрируется как магический)
    """
    damage = target.receive_damage(int(user.dmg * 1.7), damage_type=ability.damage_type)
    return f"{user.name} выпускает Рык и наносит {damage} магического урона {target.name}!"

