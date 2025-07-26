import matplotlib.pyplot as plt
from classes.food import Food

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.food = []  
        self.agents = [] 

        # Activar modo interactivo y crear figura/ax
        plt.ion()
        self.fig, self.ax = plt.subplots()
    
    def add_food(self, food=None):
        if food is None:
            return
        if isinstance(food, list):
            for f in food:
                self.food.append(f)
        else:
            self.food.append(food)
 

    def add_agent(self, agent):
        if agent is None:
            return
        if isinstance(agent, list):
            for ag in agent:
                self.agents.append(ag)
        else:
            self.agents.append(agent)

    def visualizar_mapa(self):
        self.ax.clear()  # Limpiar el gráfico anterior
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)
        self.ax.set_xticks(range(self.width))
        self.ax.set_yticks(range(self.height))
        self.ax.grid(True)

        # Dibujar agentes
        for agente in self.agents:
            if agente.pos is not None:
                x, y = agente.pos
                self.ax.plot(x + 0.5, y + 0.5, 'bo')

        # Dibujar comida
        for comida in self.food:
            if comida.pos is not None:
                x, y = comida.pos
                self.ax.plot(x + 0.5, y + 0.5, 'ro')

        self.ax.set_aspect('equal', adjustable='box')
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.3)  # Pausa pequeña para que se vea el cambio