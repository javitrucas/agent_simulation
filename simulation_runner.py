import os
import csv
from main import run_simulation

NUM_RUNS = 10
OUTPUT_DIR = "output"
OUTPUT_DIR_RUNS = OUTPUT_DIR + "/runs"
os.makedirs(OUTPUT_DIR_RUNS, exist_ok=True)  # Asegúrate de crear la carpeta runs

resumenes = []

for run_id in range(1, NUM_RUNS + 1):
    print(f"Ejecutando simulación {run_id}...")
    resumen, histories, agua, timeline = run_simulation(run_id=run_id, visualize=False)
    resumenes.append(resumen)

    # Encontrar longitud máxima entre todos los historiales de agentes
    max_len = max(len(hist) for hist in histories)

    # Guardar historial (cada posición en dos columnas: x_i y y_i)
    with open(f"{OUTPUT_DIR_RUNS}/run_{run_id}_historial.csv", "w", newline="") as f:
        writer = csv.writer(f)
        # Cabecera: Tipo, ID, x_0, y_0, x_1, y_1, ...
        header = ["Tipo", "ID"]
        for i in range(max_len):
            header += [f"x_{i}", f"y_{i}"]
        writer.writerow(header)

        for idx, agente_hist in enumerate(histories):
            row = ["Agente", idx]
            # Rellenar con ('', '') para posiciones faltantes
            padded_hist = agente_hist + [('', '')] * (max_len - len(agente_hist))
            for pos in padded_hist:
                row += [pos[0], pos[1]]
            writer.writerow(row)

    # Guardar agua (guardando cada posición en columnas separadas x_i, y_i)
    with open(f"{OUTPUT_DIR_RUNS}/run_{run_id}_agua.csv", "w", newline="") as f:
        writer = csv.writer(f)
        # Cabecera: Tipo, Bloque, x_0, y_0, x_1, y_1, ...
        max_positions = max(len(bloque) for bloque in agua)
        header = ["Tipo", "Bloque"]
        for i in range(max_positions):
            header += [f"x_{i}", f"y_{i}"]
        writer.writerow(header)

        for idx, bloque in enumerate(agua):
            row = ["Agua", idx]
            # Completar con ('', '') si faltan posiciones para igualar longitud
            padded_block = bloque + [('', '')] * (max_positions - len(bloque))
            for pos in padded_block:
                row += [pos[0], pos[1]]
            writer.writerow(row)

    # Guardar timeline de eventos por iteración (igual que antes)
    with open(f"{OUTPUT_DIR_RUNS}/run_{run_id}_timeline.csv", "w", newline="") as f:
        fieldnames = ["Iteración", "Agente", "Posición", "Energía", "Sed", "Edad",
                      "Tiene Hambre", "Tiene Sed", "Ha Comido", "Ha Bebido",
                      "Muerto", "Causa de Muerte"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for paso in timeline:
            for estado in paso:
                writer.writerow(estado)

# Guardar resumen general (igual que antes)
with open(f"{OUTPUT_DIR}/resumen_runs.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=resumenes[0].keys())
    writer.writeheader()
    writer.writerows(resumenes)

print(f"✅ Simulaciones completadas. Resultados guardados en: {OUTPUT_DIR}")
