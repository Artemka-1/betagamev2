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
log.add(f"[Turn {turn_manager.turn}] Battle started")
while turn_manager.phase != "END_BATTLE":
    log.add(f"[Turn {turn_manager.turn}] Turn start: {turn_manager.phase}")
    print(f"\nTurn {turn_manager.turn}, Phase: {turn_manager.phase}")
    print(f"Player HP: {player.hp}, Enemy HP: {enemy.hp}")

#"""turn of the player"""


    if turn_manager.phase == "PLAYER_TURN":
        action = input("Выберите действие (attack/skip): ").strip().lower()

        if action == "attack":
            player.attack(enemy)  # Игрок атакует врага    
            log.add(
                f"[Turn {turn_manager.turn}] {player.name} attacks {enemy.name} "
                f"(Enemy HP: {enemy.hp})"
                )
            if not enemy.is_alive():
                log.add(f"[Turn {turn_manager.turn}] {enemy.name} died")
                
            if not enemy.is_alive():
                turn_manager.phase = "END_BATTLE"
                continue

        elif action == "skip":
            print("Вы пропустили ход.")
# start of the enemys turn
    elif turn_manager.phase == "ENEMY_TURN":
        enemy.attack(player)
        log.add(
            f"[Turn {turn_manager.turn}] {enemy.name} attacks {player.name} "
            f"(Player HP: {player.hp})"
        )
        
        if not player.is_alive():
            log.add(f"[Turn {turn_manager.turn}] {player.name} died")
            
        if not player.is_alive():
            turn_manager.phase = "END_BATTLE"
        else:
            turn_manager.phase = "RESOLVE"

    # Разрешение конца хода
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
log.add(f"[Turn {turn_manager.turn}] Battle ended")
print("\n--- Battle Log ---")
print(log)