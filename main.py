import random
import csv
import matplotlib.pyplot as plt
from classes.agent import Agent
from classes.food import Food
from classes.map import Map
from classes.water import Water

def run_simulation(run_id=1, visualize=False, MAX_AGENTES=15, map_x=12, map_y=12, water_min=1, water_max=3,
                    agents_min=2, agents_max=6, agent_energy_min=20, agent_energy_max=30, agent_thrist_min=20, agent_thrist_max=30,
                    food_min=2, food_max=5, new_food_chance=1):
    mapa = Map(map_x, map_y)

    # Añadir agua
    rand_water = random.randint(water_min, water_max)
    water = [Water(map=mapa) for _ in range(rand_water)]
    mapa.add_water(water)

    # Crear agentes
    rand_ag = random.randint(agents_min, agents_max)
    agentes = [Agent(energy=random.randint(agent_energy_min, agent_energy_max), map=mapa, thirst=random.randint(agent_thrist_min, agent_thrist_max)) for _ in range(rand_ag)]

    # Crear comida
    rand_comida = random.randint(food_min, food_max)
    comidas = [Food(map=mapa) for _ in range(rand_comida)]
    mapa.add_food(comidas)

    mapa.add_agent(agentes)

    # Para tracking temporal
    timeline = []
    iteracion = 1

    MAX_ITER=500

    while any(not ag.is_dead() for ag in agentes) and iteracion<MAX_ITER:
        # agentes = [ag for ag in agentes if not ag.is_dead()]
        # if random.randint(0, 100) <= new_food_chance:
        #    nuevas_comidas = [Food(map=mapa) for _ in range(random.randint(food_min, food_max))]
        #    mapa.add_food(nuevas_comidas)

        paso = []
        for idx, ag in enumerate(agentes[:]):
            estado = {
                "Agente": idx,
                "Iteración": iteracion,
                "Posición": ag.pos,
                "Energía": ag.energy,
                "Sed": ag.thirst,
                "Edad": ag.age,
                "Tiene Hambre": ag.is_hungry(),
                "Tiene Sed": ag.is_thirsty(),
                "Ha Comido": False,
                "Ha Bebido": False,
                "Muerto": False,
                "Causa de Muerte": "",
                "Generación": ag.generation, 
                "Hijos": ag.n_children,     
                "Genes": ag.gen 
            }

            if ag.is_dead() == False:
                ag.smart_move(mapa)
                ag.update(mapa)
                for nuevo_agente in mapa.agents:
                    if nuevo_agente not in agentes and len(agentes) < MAX_AGENTES:
                        agentes.append(nuevo_agente)

                estado["Ha Comido"] = ag.just_ate
                estado["Ha Bebido"] = ag.just_drank

                if ag.is_dead():
                    estado["Muerto"] = True
                    estado["Causa de Muerte"] = ag.couse_death()
            else:
                estado["Muerto"] = True
                estado["Causa de Muerte"] = ag.couse_death()

            paso.append(estado)

        timeline.append(paso)

        if visualize:
            mapa.visualizar_mapa()

         # Actualizar regeneración de la comida
        for comida in comidas:
            comida.update()

        iteracion += 1

    if iteracion >= MAX_ITER:
        print(f"⚠️ Simulación {run_id} detenida por límite de iteraciones.")

    # Mostrar datos de los agentes
    print("\nDatos de los agentes:")
    for idx, ag in enumerate(agentes):
        print(f"\nAgente {idx}:")
        print(f"Edad: {ag.age}")
        print(f"Sexo: {ag.sex}")
        print(f"Esperanza de vida: {ag.life_span}")
        print(f"Veces que ha comido: {ag.times_eaten}")
        print(f"Veces que ha bebido: {ag.times_drunk}")
        print(f"Causa de muerte: {ag.couse_death()}")
        print(f"Generación: {ag.generation}")
        print(f"Genes: {ag.gen}")

    # Recopilar datos finales
    resumen = {
        "run_id": run_id,
        "num_agentes": len(agentes),
        "num_hombres": sum(1 for ag in agentes if ag.sex == "hombre"),
        "num_mujeres": sum(1 for ag in agentes if ag.sex == "mujer"),
        "muertes_sed": sum(1 for ag in agentes if ag.couse_death() == "Sed"),
        "muertes_energia": sum(1 for ag in agentes if ag.couse_death() == "Energía"),
        "muertes_edad": sum(1 for ag in agentes if ag.couse_death() == "Edad"),
        "muertes_desconocida": sum(1 for ag in agentes if ag.couse_death() == "Desconocido"),
        "edad_media": round(sum(ag.age for ag in agentes) / len(agentes), 2),
        "comidas_totales": sum(ag.times_eaten for ag in agentes),
        "bebidas_totales": sum(ag.times_drunk for ag in agentes),
        "num_hijos_totales": sum(1 for ag in agentes if ag.generation != 0),
        "generation": max((ag.generation for ag in agentes), default=0),
        "num_normales": sum(1 for ag in agentes if ag.gen == "normal"),
        "num_tontos": sum(1 for ag in agentes if "tonto" in ag.gen),
        "num_fertiles": sum(1 for ag in agentes if "fertil" in ag.gen)
    }

    historial_total = [ag.history for ag in agentes]
    agua = [w.positions for w in water]
    comida = [c.positions for c in comidas]

    return resumen, historial_total, agua,comida, timeline

if __name__ == "__main__":
    resumen, historial, agua, comida,timeline = run_simulation(run_id=1, visualize=True, MAX_AGENTES=15, map_x=12, map_y=12, water_min=1, water_max=3,
                    agents_min=2, agents_max=6, agent_energy_min=20, agent_energy_max=30, agent_thrist_min=20, agent_thrist_max=30,
                    food_min=2, food_max=8, new_food_chance=1)
