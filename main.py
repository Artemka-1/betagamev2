from core.turns import TurnManager
from core.battle_log import BattleLog
from core.entity_factory import create_battle


def main():
    entities = create_battle()
    battle_log = BattleLog()
    
    tm = TurnManager(entities, battle_log)
    
    battle_log.battle_start()
    
    while not tm.is_battle_over():
        tm.process_turn()

    battle_log.battle_end()
    print(battle_log)
    print("Battle finished")


if __name__ == "__main__":
    main()
