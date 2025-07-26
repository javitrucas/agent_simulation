from classes.agent import Agent
from classes.food import Food 
from classes.map import Map
import matplotlib.pyplot as plt

# Crear mapa
mapa=Map(10, 10)

# Crear agente
ag=Agent(map=mapa)
ag2=Agent(energy=8, map=mapa)
agente=[ag, ag2]

# Crear comida
c=Food(pos=(2, 3))
c2=Food(pos=(7, 3), energy=10)
comida=[c, c2]

# Añadir agente al mapa
mapa.add_agent(agente)
mapa.add_food(comida)
#mapa.visualizar_mapa()

# Mover agente aleatoriamente y sacar información
i=1
for _ in range(20):  # Realizar movimientos aleatorios
    print(f"Iteración {i}")
    for idx, ag in enumerate(agente):
        if ag.energy > 0 and ag.pos is not None:
            print(f"Posición del agente {idx}: {ag.pos}")
            print(f"Energía del agente {idx}: {ag.energy}")
            print(f"Tiene hambre el agente {idx}: {ag.is_hungry()}")
            ag.smart_move(mapa)
            ag.update(mapa)
        
    mapa.visualizar_mapa()
    i += 1

for idx, ag in enumerate(agente):
    print(f"Edad del agente {idx}: {ag.age}")

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
plt.show(block=True)
