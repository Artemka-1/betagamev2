import core.entity_factory as ef
import core.entity_v2 as ev
import core.combat_system as cs
print('entity_factory file:', ef.__file__)
print('entity_v2 file:', ev.__file__)
print('combat_system file:', cs.__file__)
ents = ef.create_battle()
print('cnt', len(ents))
for e in ents:
    print('entity class file:', e.__class__.__module__, e.__class__.__name__)
    print(e.__dict__)
