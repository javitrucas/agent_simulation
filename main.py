import random
import csv
import matplotlib.pyplot as plt
from classes.agent import Agent
from classes.food import Food
from classes.map import Map
from classes.water import Water

def run_simulation(run_id=1, visualize=False):
    mapa = Map(6, 6)

    # Añadir agua
    rand_water = random.randint(1, 3)
    water = [Water(map=mapa) for _ in range(rand_water)]
    mapa.add_water(water)

    # Crear agentes
    rand_ag = random.randint(2, 4)
    agentes = [Agent(energy=random.randint(15, 25), map=mapa) for _ in range(rand_ag)]

    # Crear comida
    rand_comida = random.randint(2, 8)
    comidas = [Food(map=mapa) for _ in range(rand_comida)]
    mapa.add_food(comidas)

    mapa.add_agent(agentes)

    # Para tracking temporal
    timeline = []
    iteracion = 1

    while any(ag.energy > 0 and ag.pos is not None for ag in agentes):
        if random.randint(1, 10) == 1:
            nuevas_comidas = [Food(map=mapa) for _ in range(random.randint(1, 3))]
            mapa.add_food(nuevas_comidas)

        paso = []
        for idx, ag in enumerate(agentes):
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
                "Causa de Muerte": ""
            }

            if ag.is_dead() == False:
                ag.smart_move(mapa)
                ag.update(mapa)

                estado["Ha Comido"] = ag.just_ate
                estado["Ha Bebido"] = ag.just_drank

                if ag.energy <= 0 or ag.pos is None:
                    estado["Muerto"] = True
                    estado["Causa de Muerte"] = ag.couse_death()
            else:
                estado["Muerto"] = True
                estado["Causa de Muerte"] = ag.couse_death()

            paso.append(estado)

        timeline.append(paso)

        if visualize:
            mapa.visualizar_mapa()

        iteracion += 1

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
        "bebidas_totales": sum(ag.times_drunk for ag in agentes)
    }

    historial_total = [ag.history for ag in agentes]
    agua = [w.positions for w in water]

    return resumen, historial_total, agua, timeline

if __name__ == "__main__":
    resumen, historial, agua, timeline = run_simulation(run_id=1, visualize=True)
