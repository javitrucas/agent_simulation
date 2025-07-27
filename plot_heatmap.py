import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def plot_run_heatmap(run_number):
    # Rutas de archivos
    agua_file = f'output/runs/run_{run_number}_agua.csv'
    historial_file = f'output/runs/run_{run_number}_historial.csv'
    output_dir = 'output/graphs/runs'
    os.makedirs(output_dir, exist_ok=True)
    
    # Cargar CSVs
    agua_df = pd.read_csv(agua_file)
    historial_df = pd.read_csv(historial_file)

    # Extraer posiciones de agua (adaptado al nuevo formato x_0,y_0,x_1,y_1,...)
    agua_positions = []
    for _, row in agua_df.iterrows():
        # Las posiciones empiezan en la columna 2, en pares (x_i, y_i)
        pos_values = row[2:].values
        for i in range(0, len(pos_values), 2):
            x = pos_values[i]
            y = pos_values[i + 1] if i + 1 < len(pos_values) else None
            if pd.isna(x) or pd.isna(y) or x == '' or y == '':
                continue
            try:
                x_int = int(float(x))
                y_int = int(float(y))
                agua_positions.append((x_int, y_int))
            except (ValueError, TypeError):
                continue

    # Extraer posiciones de agentes (igual que antes)
    all_agent_positions = []
    for _, row in historial_df.iterrows():
        positions = row[2:].values
        for i in range(0, len(positions), 2):
            x = positions[i]
            y = positions[i + 1] if i + 1 < len(positions) else None
            if pd.isna(x) or pd.isna(y):
                continue
            try:
                x_int = int(float(x))
                y_int = int(float(y))
                all_agent_positions.append((x_int, y_int))
            except (ValueError, TypeError):
                continue

    if not all_agent_positions and not agua_positions:
        print("No hay datos de posiciones para mostrar el heatmap.")
        return

    # Resto del código igual...

    all_x = [p[0] for p in all_agent_positions + agua_positions]
    all_y = [p[1] for p in all_agent_positions + agua_positions]
    xmin, xmax = min(all_x), max(all_x)
    ymin, ymax = min(all_y), max(all_y)

    width = xmax - xmin + 1
    height = ymax - ymin + 1
    heatmap = np.zeros((height, width))

    # Contar visitas por celda (solo agentes)
    for (x, y) in all_agent_positions:
        heatmap[y - ymin, x - xmin] += 1

    sns.set_style("whitegrid")

    fig, ax = plt.subplots(figsize=(10, 8), facecolor='white')
    cax = ax.imshow(heatmap, cmap='YlOrRd', interpolation='nearest', origin='lower')
    cbar = fig.colorbar(cax, ax=ax, label='Número de visitas de agentes')
    cbar.ax.yaxis.label.set_size(12)

    # Dibujar agua
    for (x, y) in agua_positions:
        rect = plt.Rectangle((x - xmin - 0.5, y - ymin - 0.5), 1, 1,
                             linewidth=1, edgecolor='blue', facecolor='blue', alpha=0.3)
        ax.add_patch(rect)

    ax.set_xticks(np.arange(width))
    ax.set_yticks(np.arange(height))
    ax.set_xticklabels(np.arange(xmin, xmax + 1))
    ax.set_yticklabels(np.arange(ymin, ymax + 1))

    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_title(f'Mapa de calor - Run {run_number}', fontsize=14, fontweight='bold')
    ax.grid(which='major', color='gray', linestyle='-', linewidth=0.5, alpha=0.2)

    plt.tight_layout()

    save_path = os.path.join(output_dir, f'run_{run_number}_heatmap.png')
    plt.savefig(save_path, dpi=150)
    print(f'Gráfico guardado en: {save_path}')

    plt.show()


if __name__ == "__main__":
    for run_id in range(1, 11):
        plot_run_heatmap(run_id)
