from core.combat_system import CombatSystem
from core.action_system import ActionSystem
from core.decision_system import DecisionSystem
from core.turn_manager import TurnManager
from core.status_system import StatusSystem
from core.battle_log import BattleLog
from core.entity_factory import create_battle


def player_action_callback(actor, enemies):
    if not enemies:
        return None

    print(f"Выберите цель для {actor.name}:")
    for idx, enemy in enumerate(enemies, start=1):
        print(f"{idx}) {enemy.name} (HP {enemy.hp}/{enemy.max_hp})")

    while True:
        choice = input(f"Номер цели (1-{len(enemies)}): ").strip()
        if not choice.isdigit():
            print("Введите число.")
            continue
        target_index = int(choice) - 1
        if 0 <= target_index < len(enemies):
            break
        print("Неверный номер цели.")

    target = enemies[target_index]
    return {
        "type": "attack",
        "source": actor,
        "target": target
    }


def main():
    entities = create_battle()

    battle_log = BattleLog()

    action_system = ActionSystem(CombatSystem())

    decision_system = DecisionSystem(
        interactive=True,
        player_action_callback=player_action_callback
    )

    status_system = StatusSystem()

    tm = TurnManager(
        entities=entities,
        action_system=action_system,
        battle_log=battle_log,
        decision_system=decision_system,
        status_system=status_system
    )

    battle_log.battle_start()
    print(battle_log.events[-1])

    last_event_index = len(battle_log.events)
    while not tm.is_battle_over():
        tm.process_turn()

        for event in battle_log.events[last_event_index:]:
            print(event)
        last_event_index = len(battle_log.events)

        if not tm.is_battle_over():
            input("Нажмите Enter для продолжения...")

    battle_log.battle_end()
    print(battle_log)
    print("Battle finished")


if __name__ == "__main__":
    main()
