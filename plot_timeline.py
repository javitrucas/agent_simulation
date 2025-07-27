import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import os

def plot_timeline(run_id=1):
    filename = f"output/runs/run_{run_id}_timeline.csv"
    df = pd.read_csv(filename)
    
    agentes = sorted(df["Agente"].unique())  # Usar solo los agentes que realmente existen y ordenarlos
    
    # Crear figura con estilo limpio
    fig, ax = plt.subplots(figsize=(16, 10))
    fig.patch.set_facecolor('white')
    
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
        cmap = cm.get_cmap('tab20')
        if len(agentes) > 20:
            cmap = cm.get_cmap('hsv')
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
               linewidth=3, 
               label=f'Agente {ag}',
               alpha=0.8)
        
        # Si murió, añadir etiqueta en el punto antes de la muerte
        if punto_muerte is not None and edad_al_morir is not None:
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
    ax.set_xlabel('Iteración', fontsize=16, fontweight='600', color='#2D3748')
    ax.set_ylabel('Edad', fontsize=16, fontweight='600', color='#2D3748')
    ax.set_title(f'Timeline de Agentes — Run {run_id}', 
                fontsize=22, fontweight='300', color='#1A202C', pad=25)
    
    # Cuadrícula minimalista
    ax.grid(True, linestyle='-', alpha=0.1, color='#A0AEC0', linewidth=1)
    ax.set_facecolor('#FAFAFA')
    
    # Línea sutil en y=0
    ax.axhline(y=0, color='#E2E8F0', linewidth=2, alpha=0.8)
    
    # Personalizar ejes
    ax.tick_params(axis='both', which='major', labelsize=12, colors='#4A5568')
    
    # Bordes limpios
    for spine in ax.spines.values():
        spine.set_color('#E2E8F0')
        spine.set_linewidth(1.5)
    
    
    # Ajustar layout
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    for run_id in range(1, 11):
        plot_timeline(run_id)