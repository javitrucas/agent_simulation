import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os
import seaborn as sns

def plot_run_heatmap(run_number, ax=None):
    # Rutas de archivos
    agua_file = f'output/runs/run_{run_number}_agua.csv'
    comida_file = f'output/runs/run_{run_number}_comida.csv'
    historial_file = f'output/runs/run_{run_number}_historial.csv'
    
    # Si no se proporciona ax, crear figura independiente
    if ax is None:
        output_dir = 'output/graphs/runs'
        os.makedirs(output_dir, exist_ok=True)
        fig, ax = plt.subplots(figsize=(10, 8), facecolor='white')
        standalone = True
    else:
        standalone = False
    
    # Cargar CSVs
    agua_df = pd.read_csv(agua_file)
    historial_df = pd.read_csv(historial_file)
    comida_df = pd.read_csv(comida_file)

    # Extraer posiciones de agua (adaptado al nuevo formato x_0,y_0,x_1,y_1,...)
    agua_positions = []
    for _, row in agua_df.iterrows():
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

    # Extraer posiciones de comida (igual que agua)
    comida_positions = []
    for _, row in comida_df.iterrows():
        pos_values = row[2:].values
        for i in range(0, len(pos_values), 2):
            x = pos_values[i]
            y = pos_values[i + 1] if i + 1 < len(pos_values) else None
            if pd.isna(x) or pd.isna(y) or x == '' or y == '':
                continue
            try:
                x_int = int(float(x))
                y_int = int(float(y))
                comida_positions.append((x_int, y_int))
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

    if not all_agent_positions and not agua_positions and not comida_positions:
        if standalone:
            print("No hay datos de posiciones para mostrar el heatmap.")
        return

    all_x = [p[0] for p in all_agent_positions + agua_positions + comida_positions]
    all_y = [p[1] for p in all_agent_positions + agua_positions + comida_positions]
    xmin, xmax = min(all_x), max(all_x)
    ymin, ymax = min(all_y), max(all_y)

    width = xmax - xmin + 1
    height = ymax - ymin + 1
    heatmap = np.zeros((height, width))

    # Contar visitas por celda (solo agentes)
    for (x, y) in all_agent_positions:
        heatmap[y - ymin, x - xmin] += 1

    sns.set_style("whitegrid")

    cax = ax.imshow(heatmap, cmap='YlOrRd', interpolation='nearest', origin='lower')
    
    # Solo añadir colorbar si es standalone
    if standalone:
        cbar = plt.colorbar(cax, ax=ax, label='Número de visitas de agentes')
        cbar.ax.yaxis.label.set_size(12)

    # Dibujar agua (azul)
    for (x, y) in agua_positions:
        rect = plt.Rectangle((x - xmin - 0.5, y - ymin - 0.5), 1, 1,
                             linewidth=1, edgecolor='blue', facecolor='blue', alpha=0.3)
        ax.add_patch(rect)

    # Dibujar comida (verde)
    for (x, y) in comida_positions:
        rect = plt.Rectangle((x - xmin - 0.5, y - ymin - 0.5), 1, 1,
                             linewidth=1, edgecolor='green', facecolor='green', alpha=0.3)
        ax.add_patch(rect)

    ax.set_xticks(np.arange(width))
    ax.set_yticks(np.arange(height))
    ax.set_xticklabels(np.arange(xmin, xmax + 1))
    ax.set_yticklabels(np.arange(ymin, ymax + 1))

    ax.set_xlabel('X', fontsize=10 if not standalone else 12)
    ax.set_ylabel('Y', fontsize=10 if not standalone else 12)
    ax.set_title(f'Mapa de calor - Run {run_number}', fontsize=12 if not standalone else 14, fontweight='bold')
    ax.grid(which='major', color='gray', linestyle='-', linewidth=0.5, alpha=0.2)

    if standalone:
        plt.tight_layout()
        save_path = os.path.join('output/graphs/runs', f'run_{run_number}_heatmap.png')
        plt.savefig(save_path, dpi=150)
        print(f'Gráfico guardado en: {save_path}')
        plt.show()

def plot_timeline(run_id=1, ax=None):
    filename = f"output/runs/run_{run_id}_timeline.csv"
    df = pd.read_csv(filename)
    
    # Si no se proporciona ax, crear figura independiente
    if ax is None:
        fig, ax = plt.subplots(figsize=(16, 10))
        fig.patch.set_facecolor('white')
        standalone = True
    else:
        standalone = False
    
    agentes = sorted(df["Agente"].unique())  # Usar solo los agentes que realmente existen y ordenarlos
    
    # Generar colores dinámicamente según el número de agentes
    if len(agentes) <= 10:
        # Para pocos agentes, usar colores predefinidos modernos
        colores_base = [
            '#E53E3E',  # Rojo
            '#3182CE',  # Azul
            '#38A169',  # Verde
            '#DD6B20',  # Naranja
            '#805AD5',  # Morado
            '#319795',  # Teal
            '#D53F8C',  # Rosa
            '#718096',  # Gris
            '#2D3748',  # Gris oscuro
            '#B83280'   # Magenta
        ]
        colores_agentes = colores_base[:len(agentes)]
    else:
        # Para muchos agentes, generar colores automáticamente
        cmap = plt.get_cmap('tab20')
        if len(agentes) > 20:
            cmap = cm.hsv
        colores_agentes = [cmap(i / len(agentes)) for i in range(len(agentes))]
    
    for i, ag in enumerate(agentes):
        datos = df[df["Agente"] == ag].sort_values('Iteración')
        color_agente = colores_agentes[i]
        
        # Crear listas para la línea de vida
        iteraciones_vida = []
        edades_vida = []
        punto_muerte = None
        edad_al_morir = None
        causa_muerte = None
        iter_antes_muerte = None
        
        for _, fila in datos.iterrows():
            iteraciones_vida.append(fila["Iteración"])
            
            if fila["Muerto"]:
                if punto_muerte is None:  # Primera vez que aparece como muerto
                    punto_muerte = fila["Iteración"]
                    causa_muerte = fila.get("Causa de Muerte", "Desconocida")
                    # Buscar la fila anterior para obtener la edad real al morir
                    fila_anterior = datos[datos["Iteración"] < fila["Iteración"]].iloc[-1] if len(datos[datos["Iteración"] < fila["Iteración"]]) > 0 else fila
                    edad_al_morir = fila_anterior["Edad"]
                    iter_antes_muerte = fila_anterior["Iteración"]
                edades_vida.append(-1)
            else:
                edades_vida.append(fila["Edad"])
        
        # Dibujar línea de vida
        ax.plot(iteraciones_vida, edades_vida, 
               color=color_agente, 
               linewidth=2 if not standalone else 3, 
               label=f'Agente {ag}' if standalone else None,
               alpha=0.8)
        
        # Si murió, añadir etiqueta en el punto antes de la muerte (solo en standalone para evitar sobrecargar)
        if punto_muerte is not None and edad_al_morir is not None and standalone:
            # Usar la iteración y edad justo antes de morir
            punto_etiqueta_x = iter_antes_muerte if iter_antes_muerte is not None else punto_muerte
            punto_etiqueta_y = edad_al_morir
            
            # Etiqueta de muerte
            ax.annotate(f'Edad: {int(edad_al_morir)}\n{causa_muerte}', 
                       xy=(punto_etiqueta_x, punto_etiqueta_y),
                       xytext=(0, 30), 
                       textcoords='offset points',
                       fontsize=10,
                       fontweight='500',
                       color='#2D3748',
                       ha='center',
                       bbox=dict(boxstyle="round,pad=0.4", 
                               facecolor='white', 
                               edgecolor=color_agente,
                               linewidth=2,
                               alpha=0.95),
                       arrowprops=dict(arrowstyle='->', 
                                     connectionstyle='arc3,rad=0',
                                     color=color_agente,
                                     lw=1.5))
    
    # Configuración limpia y moderna
    fontsize_title = 14 if not standalone else 22
    fontsize_label = 12 if not standalone else 16
    
    ax.set_xlabel('Iteración', fontsize=fontsize_label, fontweight='600', color='#2D3748')
    ax.set_ylabel('Edad', fontsize=fontsize_label, fontweight='600', color='#2D3748')
    ax.set_title(f'Timeline de Agentes — Run {run_id}', 
                fontsize=fontsize_title, fontweight='300', color='#1A202C', pad=15 if not standalone else 25)
    
    # Cuadrícula minimalista
    ax.grid(True, linestyle='-', alpha=0.1, color='#A0AEC0', linewidth=1)
    ax.set_facecolor('#FAFAFA')
    
    # Línea sutil en y=0
    ax.axhline(y=0, color='#E2E8F0', linewidth=2, alpha=0.8)
    
    # Personalizar ejes
    ax.tick_params(axis='both', which='major', labelsize=10 if not standalone else 12, colors='#4A5568')
    
    # Bordes limpios
    for spine in ax.spines.values():
        spine.set_color('#E2E8F0')
        spine.set_linewidth(1.5)
    
    if standalone:
        # Ajustar layout
        plt.tight_layout()
        plt.show()

def plot_alive_count(run_id=1, ax=None):
    filename = f"output/runs/run_{run_id}_timeline.csv"
    df = pd.read_csv(filename)

    # Agrupar por iteración y contar los agentes que no están muertos
    vivos_por_iteracion = df[df["Muerto"] == False].groupby("Iteración")["Agente"].nunique()

    # Si no se proporciona ax, crear figura independiente
    if ax is None:
        plt.figure(figsize=(12, 6))
        ax = plt.gca()
        standalone = True
    else:
        standalone = False

    ax.plot(vivos_por_iteracion.index, vivos_por_iteracion.values, color='#2B6CB0', linewidth=2.5)
    
    fontsize_title = 14 if not standalone else 20
    fontsize_label = 12 if not standalone else 14
    
    ax.set_title(f'Agentes Vivos — Run {run_id}', fontsize=fontsize_title, pad=10 if not standalone else 15)
    ax.set_xlabel("Iteración", fontsize=fontsize_label)
    ax.set_ylabel("Agentes vivos", fontsize=fontsize_label)
    ax.grid(True, linestyle="--", alpha=0.3)
    
    if standalone:
        plt.tight_layout()
        plt.show()


def plot_run_summary(run_id, axes=None):
    resumen_path = "output/resumen_runs.csv"
    
    if not os.path.exists(resumen_path):
        print(f"No se encontró el archivo {resumen_path}")
        return

    df = pd.read_csv(resumen_path)
    
    if "run_id" not in df.columns:
        print("La columna 'run_id' no está presente en el archivo resumen_runs.csv")
        return
    
    df_run = df[df["run_id"] == run_id]
    
    if df_run.empty:
        print(f"No se encontró información para run_id={run_id}")
        return

    row = df_run.iloc[0]

    # Si no se proporcionan axes, crear figura independiente con 4 subgráficas
    if axes is None:
        fig, axes = plt.subplots(1, 4, figsize=(18, 6))
        standalone = True
    else:
        standalone = False

    # Gráfica 1: Distribución por Sexo
    axes[0].pie([row["num_hombres"], row["num_mujeres"]],
                labels=["Hombres", "Mujeres"],
                autopct='%1.1f%%',
                startangle=90,
                colors=["lightblue", "lightpink"])
    axes[0].set_title("Distribución por Sexo", fontsize=12 if not standalone else 14)

    # Gráfica 2: Causas de Muerte
    muertes = {
        "Sed": row["muertes_sed"],
        "Energía": row["muertes_energia"],
        "Edad": row["muertes_edad"],
        "Desconocida": row["muertes_desconocida"]
    }

    axes[1].pie(muertes.values(),
                labels=muertes.keys(),
                autopct='%1.1f%%',
                startangle=90,
                colors=["#91c7b1", "#f4a582", "#d1c4e9", "#cccccc"])
    axes[1].set_title("Causas de Muerte", fontsize=12 if not standalone else 14)

    # Gráfica 3: Estadísticas Finales
    etiquetas = ["Edad Media", "Comidas", "Bebidas", "Hijos", "Generaciones"]
    valores = [
        row["edad_media"],
        row["comidas_totales"],
        row["bebidas_totales"],
        row["num_hijos_totales"],
        row["generation"]
    ]
    colores = ["#6baed6", "#74c476", "#fd8d3c", "#d62728", "#e377c2", "#6e12c5", "#7f7f7f", "#bcbd22"]

    axes[2].bar(etiquetas, valores, color=colores, alpha=0.9)
    axes[2].set_title("Estadísticas Finales", fontsize=12 if not standalone else 14)
    axes[2].set_ylabel("Cantidad", fontsize=10 if not standalone else 12)
    if not standalone:
        axes[2].tick_params(axis='x', rotation=45, labelsize=8)

def plot_combined_run_analysis(run_id):
    # Crear figura grande con subplots
    fig = plt.figure(figsize=(20, 20))
    fig.suptitle(f'Análisis Completo - Run {run_id}', fontsize=24, fontweight='bold', y=0.96)
    
    # Definir el grid de subplots: 4 filas, 4 columnas
    gs = fig.add_gridspec(4, 4,
                          height_ratios=[1.2, 1, 0.8, 1.2],
                          width_ratios=[1, 1, 1, 1],
                          hspace=0.4, wspace=0.3)
    
    # Timeline (ocupa la fila 0 completa)
    ax_timeline = fig.add_subplot(gs[0, :])
    plot_timeline(run_id, ax_timeline)
    
    # Heatmap (fila 1, columnas 0-1)
    ax_heatmap = fig.add_subplot(gs[1, :2])
    plot_run_heatmap(run_id, ax_heatmap)
    
    # Alive count (fila 1, columnas 2-3)
    ax_alive = fig.add_subplot(gs[1, 2:])
    plot_alive_count(run_id, ax_alive)
    
    # Summary plots (fila 2, columnas 0-3 divididas en 4)
    ax_summary1 = fig.add_subplot(gs[2, 0])
    ax_summary2 = fig.add_subplot(gs[2, 1])
    ax_summary3 = fig.add_subplot(gs[2, 2])
    # ax_summary4 = fig.add_subplot(gs[2, 3])
    plot_run_summary(run_id, [ax_summary1, ax_summary2, ax_summary3])
    
    # Gráfica de Genes (fila 3 completa)
    ax_genes = fig.add_subplot(gs[3, :])
    _plot_genes_evolution(run_id, ax_genes)
    
    # Guardar y mostrar
    output_dir = 'output/graphs/runs'
    os.makedirs(output_dir, exist_ok=True)
    save_path = os.path.join(output_dir, f'run_{run_id}_combined_analysis.png')
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f'Análisis combinado guardado en: {save_path}')
    plt.show()


def _plot_genes_evolution(run_id, ax):
    timeline_file = f"output/runs/run_{run_id}_timeline.csv"
    if not os.path.exists(timeline_file):
        ax.text(0.5, 0.5, "No hay datos\nde genes por iteración",
                ha='center', va='center', fontsize=14, color='gray')
        ax.axis('off')
        return

    df_tl = pd.read_csv(timeline_file)

    # Excluir agentes muertos
    if "Causa de Muerte" in df_tl.columns:
        df_tl = df_tl[df_tl["Causa de Muerte"].isna() | (df_tl["Causa de Muerte"] == "")]
    elif "Muerto" in df_tl.columns:
        df_tl = df_tl[df_tl["Muerto"] == False]

    if df_tl.empty:
        ax.text(0.5, 0.5, "No hay agentes vivos\npara graficar",
                ha='center', va='center', fontsize=14, color='gray')
        ax.axis('off')
        return

    # Contar por iteración y por gen
    df_gen = df_tl.groupby(['Iteración', 'Genes']).size().unstack(fill_value=0)

    # Ordenar tus genes
    genes = ['normal', 'tonto', 'fertil']  # extiende según necesites
    for g in genes:
        if g not in df_gen.columns:
            df_gen[g] = 0
    df_gen = df_gen[genes]

    # Dibujar barras apiladas
    bottom = pd.Series(0, index=df_gen.index)
    for gen in genes:
        ax.bar(df_gen.index, df_gen[gen],
               bottom=bottom, label=gen.capitalize(), alpha=0.8)
        bottom += df_gen[gen]

    # Estilo
    ax.set_title("Genes a lo largo del tiempo", fontsize=18, fontweight='600', pad=10)
    ax.set_xlabel("Iteración", fontsize=14)
    ax.set_ylabel("Número de agentes", fontsize=14)
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    ax.legend(fontsize=12, loc='upper left')
    ax.set_facecolor('#FAFAFA')

if __name__ == "__main__":
    for run_id in range(1, 11):
        # Mantener las funciones individuales
        #plot_timeline(run_id)
        #plot_alive_count(run_id)
        #plot_run_summary(run_id)
        #plot_run_heatmap(run_id)
        
        # Nueva función combinada
        plot_combined_run_analysis(run_id)