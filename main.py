from core.turn_manager import TurnManager
from core.battle_log import BattleLog
from core.entity_factory import create_battle
from core.action_system import ActionSystem
from core.decision_system import DecisionSystem
from core.status_system import StatusSystem

def main():
    entities = create_battle()

    battle_log = BattleLog()
    action_system = ActionSystem()

    def player_action_callback(actor, enemies):
        print(f"\nХод игрока: {actor.name} (HP: {actor.hp})")
        print("Выберите действие:")

        actions = [{'type': 'attack', 'name': 'Атака'}]
        abilities = getattr(actor, 'abilities', []) or []
        for ability in abilities:
            actions.append({'type': 'ability', 'name': ability.name, 'ability': ability})

        for index, action in enumerate(actions, start=1):
            print(f"{index}. {action['name']}")

        while True:
            choice = input("Введите номер действия: ").strip()
            if not choice.isdigit():
                print("Пожалуйста, введите число.")
                continue
            choice = int(choice)
            if 1 <= choice <= len(actions):
                selected = actions[choice - 1]
                break
            print(f"Выберите число от 1 до {len(actions)}.")

        if len(enemies) == 1:
            target = enemies[0]
        else:
            print("Выберите цель:")
            for index, enemy in enumerate(enemies, start=1):
                print(f"{index}. {enemy.name} (HP: {enemy.hp})")
            while True:
                target_choice = input("Введите номер цели: ").strip()
                if not target_choice.isdigit():
                    print("Пожалуйста, введите число.")
                    continue
                target_choice = int(target_choice)
                if 1 <= target_choice <= len(enemies):
                    target = enemies[target_choice - 1]
                    break
                print(f"Выберите число от 1 до {len(enemies)}.")

        action = {
            'type': selected['type'],
            'source': actor,
            'target': target
        }
        if selected['type'] == 'ability':
            action['ability'] = selected['ability']
        return action

    decision_system = DecisionSystem(interactive=True, player_action_callback=player_action_callback)
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

    while not tm.is_battle_over():
        previous_events = len(battle_log.events)
        tm.process_turn()
        new_events = battle_log.events[previous_events:]
        if new_events:
            print("\n".join(new_events))
        input("Нажмите Enter для следующего хода...")

    battle_log.battle_end()
    print(battle_log)
    print("Battle finished")

if __name__ == "__main__":
    main()
    