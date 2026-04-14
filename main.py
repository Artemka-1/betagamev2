# main.py
from core import battle_log
from core.entity_v2 import EntityV2
from core.classes import KNIGHT, ARCHER, MAGE
from core.pre_fight import pre_fight_timer
from core.turns import TurnManager
from core.rules import MageBonusRule

log = battle_log.BattleLog()

# команды игроков и врагов
players = [
    EntityV2("Игрок1", hp=30, dmg=5, char_class=MAGE, faction="INT"),
    EntityV2("Игрок2", hp=25, dmg=6, char_class=KNIGHT, faction="STR")
]
enemies = [
    EntityV2("Враг1", hp=20, dmg=4, char_class=ARCHER, faction="DEX"),
    EntityV2("Враг2", hp=18, dmg=5, char_class=MAGE, faction="INT")
]

# предбоевой таймер
pre_fight_timer(1)

# настройка правил боя
rules = [MageBonusRule()]
turn_manager = TurnManager(players, enemies, rules=rules)
turn_manager.phase = "PLAYER_TURN"

log.battle_start(turn_manager.turn)

# основной цикл боя
while not turn_manager.is_battle_over():
    log.phase_start(turn_manager.turn, turn_manager.phase)
    
    # Ход игроков
    if turn_manager.phase == "PLAYER_TURN":
        for p in turn_manager.get_alive(turn_manager.players):
            print(f"\n{p.name}'s turn (HP: {p.hp})")
            
            # ввод действия
            valid_actions = ["attack", "skip"]
            action_input = ""
            while action_input not in valid_actions:
                action_input = input("Выберите действие (attack/skip): ").strip().lower()
            
            if action_input == "attack":
                target = turn_manager.get_alive(turn_manager.enemies)[0]
                p.attack(target)
                turn_manager.apply_rules(p, target)
                log.action(turn_manager.turn, f"{p.name} атакует {target.name} (HP врага: {target.hp})")
                if not target.is_alive():
                    log.death(turn_manager.turn, target.name)
            elif action_input == "skip":
                log.action(turn_manager.turn, f"{p.name} пропускает ход")
    
    # Ход врагов
    elif turn_manager.phase == "ENEMY_TURN":
        for e in turn_manager.get_alive(turn_manager.enemies):
            target = turn_manager.get_alive(turn_manager.players)[0]
            e.attack(target)
            turn_manager.apply_rules(e, target)
            log.action(turn_manager.turn, f"{e.name} атакует {target.name} (HP игрока: {target.hp})")
            if not target.is_alive():
                log.death(turn_manager.turn, target.name)
    
    # Фаза RESOLVE (можно использовать для бонусов, эффектов и т.п.)
    elif turn_manager.phase == "RESOLVE":
        pass  # turn уже увеличивается в next_phase()
    
    turn_manager.next_phase()

# бой завершён
log.battle_end(turn_manager.turn)
print("\n=== Бой завершён ===")

# вывод результатов
if turn_manager.get_alive(players) and not turn_manager.get_alive(enemies):
    print("\nВы победили!")
elif turn_manager.get_alive(enemies) and not turn_manager.get_alive(players):
    print("\nВы проиграли!")
else:
    print("\nНичья!")

# вывод лога боя
print(f"\nБой закончился за {turn_manager.turn} ходов.")
print("\n--- Battle Log ---")
print(log)