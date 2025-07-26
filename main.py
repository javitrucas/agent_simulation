from classes.agent import Agent
from classes.food import Food 
from classes.map import Map
from classes.water import Water
import matplotlib.pyplot as plt
import random

# Crear mapa
mapa=Map(10, 10)

# Crear agente
rand_ag=random.randint(1, 5)
agente=[]
for _ in range(rand_ag):
    ag=Agent(energy=random.randint(7, 12), map=mapa)
    agente.append(ag)

# Crear comida
rand_comida=random.randint(2, 8)
comida=[]
for _ in range(rand_comida):
    food=Food(map=mapa)
    comida.append(food)

# Crear agua
rand_water=random.randint(1, 3)
water=[]
for _ in range(rand_water):
    wat=Water(map=mapa)
    water.append(wat)

# Añadir elementos al mapa
mapa.add_water(water)
mapa.add_agent(agente)
mapa.add_food(comida)
mapa.visualizar_mapa()

# Mover agente
i = 1
while any(ag.energy > 0 and ag.pos is not None for ag in agente):
    print(f"\nIteración {i}")
    for idx, ag in enumerate(agente):
        if ag.energy > 0 and ag.pos is not None:
            print(f"Posición del agente {idx}: {ag.pos}")
            print(f"Energía del agente {idx}: {ag.energy}")
            print(f"Sed del agente {idx}: {ag.thirst}")
            ag.smart_move(mapa)
            ag.update(mapa)
    mapa.visualizar_mapa()
    i += 1

# Mostrar datos de los agentes
print("\nDatos de los agentes:")
for idx, ag in enumerate(agente):
    print(f"\nAgente {idx}:")
    print(f"Edad del agente {idx}: {ag.age}")
    print(f"Sexo del agente {idx}: {ag.sex}")
    print(f"Esperanza de vida del agente {idx}: {ag.life_span}")

# Mostrar historial de posiciones de cada agente
for idx, ag in enumerate(agente):
    if ag.pos is not None:
        print(f"Historial de posiciones del agente {idx+1}: {ag.history}")

# Crear heatmap vacío
heatmap = [[0 for _ in range(mapa.width)] for _ in range(mapa.height)]

# Acumular posiciones de todos los agentes en el heatmap
for ag in agente:
    for pos in ag.history:
        if pos is not None:
            x, y = pos
            heatmap[y][x] += 1

# Mostrar el heatmap
plt.imshow(heatmap, cmap='hot', interpolation='nearest', extent=[0, mapa.width, 0, mapa.height])
plt.colorbar()
plt.gca().invert_yaxis()
# plt.show(block=True)
