from core.entity_v2 import EntityV2
from core.classes import KNIGHT, ARCHER, MAGE
from core.pre_fight import pre_fight_timer
from core.turns import TurnManager
from core.rules import MageBonusRule

# Создание персонажей
player = EntityV2("Игрок", hp=30, dmg=5, char_class=MAGE)
enemy = EntityV2("Враг", hp=20, dmg=4, char_class=ARCHER)

# подготовка
pre_fight_timer(1)

# создаём TurnManager
rules = [MageBonusRule()]
turn_manager = TurnManager(player, enemy, rules=rules)

# после создания TurnManager сразу переключаем фазу
turn_manager.phase = "PLAYER_TURN"

# цикл боя
while turn_manager.phase != "END_BATTLE":
    print(f"\nTurn {turn_manager.turn}, Phase: {turn_manager.phase}")
    print(f"Player HP: {player.hp}, Enemy HP: {enemy.hp}")

    if turn_manager.phase == "PLAYER_TURN":
        action = input("Выберите действие (attack/skip): ").strip().lower()
        if action == "attack":
            enemy.hp -= player.dmg
            print(f"Вы нанесли {player.dmg} урона врагу!")
        elif action == "skip":
            print("Вы пропустили ход.")
        turn_manager.phase = "ENEMY_TURN"

    elif turn_manager.phase == "ENEMY_TURN":
        player.hp -= enemy.dmg
        print(f"Враг нанёс {enemy.dmg} урона вам!")
        turn_manager.phase = "RESOLVE"

    elif turn_manager.phase == "RESOLVE":
        turn_manager.turn += 1
        if player.is_alive() and enemy.is_alive():
            turn_manager.phase = "PLAYER_TURN"
        else:
            turn_manager.phase = "END_BATTLE"

# результат
if player.is_alive() and not enemy.is_alive():
    print("\nВы победили!")
elif enemy.is_alive() and not player.is_alive():
    print("\nВы проиграли!")
else:
    print("\nНичья!")

print(f"\nБой закончился за {turn_manager.turn} ходов.")