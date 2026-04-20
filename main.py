# main.py
from core import battle_log
from core.entity_v2 import EntityV2
from core.classes import KNIGHT, ARCHER, MAGE
from core.pre_fight import pre_fight_timer
from core.turns import TurnManager
from core.rules import MageBonusRule
from core.roster import Mael, VasaraX
from core.entity_factory import create_entity_from_roster

log = battle_log.BattleLog()

# команды игроков и врагов
players = [
    create_entity_from_roster(Mael)
]

enemies = [
    create_entity_from_roster(VasaraX)
]
# предбоевой таймер
pre_fight_timer(1)

# настройка правил боя
rules = [MageBonusRule()]
turn_manager = TurnManager(players, enemies, rules=rules)
turn_manager.phase = "PLAYER_TURN"
# старт боя с записи в лог
log.battle_start(turn_manager.turn)
def get_first_target(turn_manager, group):
    alive = turn_manager.get_alive(group)
    return alive[0] if alive else None

# основной цикл боя
while not turn_manager.is_battle_over():
    log.phase_start(turn_manager.turn, turn_manager.phase)
    # Ход игроков
    if turn_manager.phase == "PLAYER_TURN":
        for p in turn_manager.get_alive(turn_manager.players):
            target = get_first_target(turn_manager, turn_manager.enemies)
            if not target:
                continue

            print(f"\n{p.name}'s turn (HP: {p.hp}, OD: {p.od}/{p.od_max})")

            action_input = ""
            while action_input not in ["attack", "ability", "skip"]:
                action_input = input("Выберите действие (attack/ability/skip): ").strip().lower()

            if action_input == "attack":
                turn_manager.apply_rules(p, target)
                damage = p.attack(target)
                log.action(
                    turn_manager.turn,
                    f"{p.name} атакует {target.name} ({damage} урона, HP врага: {target.hp})"
                )
                if not target.is_alive():
                    log.death(turn_manager.turn, target.name)

            elif action_input == "ability":
                abilities = p.get_available_abilities()
                if not abilities:
                    print("Нет доступных способностей сейчас.")
                    continue

                print("Доступные способности:")
                for idx, ability in enumerate(abilities, 1):
                    cd = p.get_ability_cooldown(ability.name)
                    print(f"{idx}. {ability.name} (ОД {ability.cost}, перезарядка {cd}) - {ability.description}")

                choice = ""
                while True:
                    choice = input("Выберите номер способности или cancel: ").strip().lower()
                    if choice == "cancel":
                        break
                    if choice.isdigit() and 1 <= int(choice) <= len(abilities):
                        break
                    print("Неверный выбор, введите номер способности или cancel.")

                if choice == "cancel":
                    continue

                ability = abilities[int(choice) - 1]
                action_text = p.use_ability(ability.name, target)
                log.action(
                    turn_manager.turn,
                    f"{action_text} (HP врага: {target.hp})"
                )
                if not target.is_alive():
                    log.death(turn_manager.turn, target.name)

            elif action_input == "skip":
                log.action(turn_manager.turn, f"{p.name} пропускает ход")

        turn_manager.next_phase()

    # Ход врагов
    elif turn_manager.phase == "ENEMY_TURN":
        for e in turn_manager.get_alive(turn_manager.enemies):
            target = get_first_target(turn_manager, turn_manager.players)
            if not target:
                continue

            turn_manager.apply_rules(e, target)
            available = e.get_available_abilities()
            if available:
                action_text = e.use_ability(available[0].name, target)
            else:
                damage = e.attack(target)
                action_text = f"{e.name} атакует {target.name} ({damage} урона, HP игрока: {target.hp})"

            log.action(turn_manager.turn, action_text)
            if not target.is_alive():
                log.death(turn_manager.turn, target.name)

        turn_manager.next_phase()

    elif turn_manager.phase == "RESOLVE":
        for entity in turn_manager.players + turn_manager.enemies:
            entity.tick_cooldowns()
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
