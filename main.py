from core.combat_system import CombatSystem
from core.action_system import ActionSystem
from core.decision_system import DecisionSystem
from core.turn_manager import TurnManager
from core.status_system import StatusSystem
from core.battle_log import BattleLog
from core.entity_factory import create_battle


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

    while not tm.is_battle_over():
        tm.process_turn()
        input("Enter...")

    battle_log.battle_end()
    print(battle_log)
    print("Battle finished")


if __name__ == "__main__":
    main()