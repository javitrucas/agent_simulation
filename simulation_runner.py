import os
import csv
from main import run_simulation

NUM_RUNS = 10
OUTPUT_DIR = "output"
OUTPUT_DIR_RUNS = OUTPUT_DIR + "/runs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

resumenes = []

for run_id in range(1, NUM_RUNS + 1):
    print(f"Ejecutando simulación {run_id}...")
    resumen, histories, agua, timeline = run_simulation(run_id=run_id, visualize=False)
    resumenes.append(resumen)

    # Guardar historial y agua
    with open(f"{OUTPUT_DIR_RUNS}/run_{run_id}_disposicion.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Tipo", "ID"] + [f"Paso_{i}" for i in range(len(histories[0]))])
        for idx, agente_hist in enumerate(histories):
            writer.writerow(["Agente", idx] + [str(p) for p in agente_hist])
        writer.writerow([])
        writer.writerow(["Tipo", "Bloque"] + [f"Celda_{i}" for i in range(len(agua[0]))])
        for idx, bloque in enumerate(agua):
            writer.writerow(["Agua", idx] + [str(p) for p in bloque])

    # Guardar timeline de eventos por iteración
    with open(f"{OUTPUT_DIR_RUNS}/run_{run_id}_timeline.csv", "w", newline="") as f:
        fieldnames = ["Iteración", "Agente", "Posición", "Energía", "Sed", "Edad",
                      "Tiene Hambre", "Tiene Sed", "Ha Comido", "Ha Bebido",
                      "Muerto", "Causa de Muerte"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for paso in timeline:
            for estado in paso:
                writer.writerow(estado)

# Guardar resumen general
with open(f"{OUTPUT_DIR}/resumen_runs.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=resumenes[0].keys())
    writer.writeheader()
    writer.writerows(resumenes)

print(f"✅ Simulaciones completadas. Resultados guardados en: {OUTPUT_DIR}")
