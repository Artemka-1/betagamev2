from core.turns import TurnManager
from core.battle_log import BattleLog
from core.entity_factory import create_entity_from_roster
from core.roster import Mael, Morok, VasaraX, QueenValkyrie, Maluk


def create_battle():
    """Create a simple battle setup with players and enemies"""
    players = [
        create_entity_from_roster(Mael),
        create_entity_from_roster(VasaraX),
    ]
    enemies = [
        create_entity_from_roster(Morok),
        create_entity_from_roster(QueenValkyrie),
    ]
    return players, enemies


def main():
    players, enemies = create_battle()
    battle_log = BattleLog()
    
    tm = TurnManager(players, enemies)
    
    battle_log.battle_start(1)
    
    while not tm.is_battle_over():
        tm.next_phase()
        battle_log.phase_start(tm.turn, tm.phase)

    battle_log.battle_end(tm.turn)
    print(battle_log)
    print("Battle finished")


if __name__ == "__main__":
    main()