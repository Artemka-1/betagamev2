from core import battle_log
from core.entity_v2 import EntityV2
from core.classes import KNIGHT, ARCHER, MAGE
from core.pre_fight import pre_fight_timer
from core.turns import TurnManager
from core.rules import MageBonusRule
from core.battle_log import BattleLog

log = BattleLog()

"""
now here are 2 classes but in fither will be more
here are clsses of player and enemys team
"""

# Создание персонажей
player = EntityV2("Игрок", hp=30, dmg=5, char_class=MAGE)
enemy = EntityV2("Враг", hp=20, dmg=4, char_class=ARCHER)

# подготовка
pre_fight_timer(1)


#create rules and use them turn manager 

# создаём TurnManager
rules = [MageBonusRule()]
turn_manager = TurnManager(player, enemy, rules=rules)
#""" start the fight loop, which will continue until one of the entities is defeated or the battle ends """

# после создания TurnManager сразу переключаем фазу
turn_manager.phase = "PLAYER_TURN"

# цикл боя
log.battle_start(turn_manager.turn)

while turn_manager.phase != "END_BATTLE":
    log.turn_start(turn_manager.turn, turn_manager.phase)

    if turn_manager.phase == "PLAYER_TURN":
        action_input = input("Выберите действие (attack/skip): ").strip().lower()

        if action_input == "attack":
            player.attack(enemy)
            log.action(
                turn_manager.turn,
                f"{player.name} attacks {enemy.name} (Enemy HP: {enemy.hp})"
            )

            if not enemy.is_alive():
                log.death(turn_manager.turn, enemy.name)
                turn_manager.phase = "END_BATTLE"
                continue
            else:
                turn_manager.phase = "ENEMY_TURN"

        elif action_input == "skip":
            log.action(
                turn_manager.turn,
                f"{player.name} skips the turn"
            )
            turn_manager.phase = "ENEMY_TURN"

    elif turn_manager.phase == "ENEMY_TURN":
        enemy.attack(player)
        log.action(turn_manager.turn, f"{enemy.name} attacks {player.name} (Player HP: {player.hp})")
        if not player.is_alive():
            log.death(turn_manager.turn, player.name)
            turn_manager.phase = "END_BATTLE"
        else:
            turn_manager.phase = "RESOLVE"

    elif turn_manager.phase == "RESOLVE":
        turn_manager.turn += 1
        if player.is_alive() and enemy.is_alive():
            turn_manager.phase = "PLAYER_TURN"
        else:
            turn_manager.phase = "END_BATTLE"


# the battle results after turns and create th end phase of the battle
            
            
if player.is_alive() and not enemy.is_alive():
    print("\nВы победили!")
elif enemy.is_alive() and not player.is_alive():
    print("\nВы проиграли!")
else:
    print("\nНичья!")

print(f"\nБой закончился за {turn_manager.turn} ходов.")
print("\n--- Battle Log ---")
print(log)
log.battle_end(turn_manager.turn)