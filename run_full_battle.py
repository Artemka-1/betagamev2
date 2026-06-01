from core.entity_factory import create_battle
from core.battle_log import BattleLog


def run():
    entities = create_battle()
    log = BattleLog()
    log.battle_start()

    turn_counter = 1
    while True:
        alive_entities = [e for e in entities if e.is_alive()]
        factions = set(e.faction for e in alive_entities)
        if len(factions) <= 1:
            break

        for actor in list(alive_entities):
            if not actor.is_alive():
                continue

            enemies = [e for e in entities if e.faction != actor.faction and e.is_alive()]
            if not enemies:
                continue

            target = enemies[0]
            log.turn_start(turn_counter, actor.name)

            if actor.abilities:
                ability = actor.abilities[0]
                action_text = ability.use(actor, target)
            else:
                damage = actor.attack(target)
                action_text = f"{actor.name} attacks {target.name} for {damage} damage"

            log.action(action_text)

            if not target.is_alive():
                log.death(target.name)

            turn_counter += 1

    log.battle_end()
    print(log)


if __name__ == '__main__':
    run()
