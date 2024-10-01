from magical_creature import MagicalCreature
from acceso_a_datos.dao.magical_creatures.magical_creature_dao import MagicalCreatureDAO

# Creamos una base de datos SQLite para criaturas mágicas
dao = MagicalCreatureDAO('config.ini')

# Obtener todas las criaturas mágicas
creatures = dao.get_all()
for creature in creatures:
    print(f"Todas las criaturas mágicas:{creature}" )

# Crear una nueva criatura mágica
dragon = MagicalCreature(id=None, name="Firagon", lives=10, magic_power=150)
dao.create(dragon)

# Obtener una criatura específica por ID
creature = dao.get(1)
print(f"Criatura con ID 1:{creature}")

# Actualizar una criatura (cambiamos su poder mágico)
creature.magic_power = 200
dao.update(creature)

# Eliminar una criatura
dao.delete(1)