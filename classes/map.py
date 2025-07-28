import matplotlib.pyplot as plt
from classes.food import Food
from classes.agent import Agent
from classes.water import Water
import random
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.food = []  
        self.agents = [] 
        self.water = []

        # Activar modo interactivo y crear figura/ax
        plt.ion()
        self.fig, self.ax = plt.subplots()

        # Cargar imagen de fondo
        self.agent_img = mpimg.imread("images/agente.png")
        self.agent_img_fem = mpimg.imread("images/agenta.png")
        self.food_img = mpimg.imread("images/food.png")

    def add_food(self, food=None):
        if food is None:
            return
        if isinstance(food, list):
            for f in food:
                self.food.append(f)
        else:
            self.food.append(food)
 
    def add_water(self, water=None):
        if water is None:
            return
        if isinstance(water, list):
            for w in water:
                self.water.append(w)
        else:
            self.water.append(water)

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

        # Fijar límites del mapa y cuadrícula
        self.ax.set_xlim(0, self.width)
        self.ax.set_ylim(0, self.height)
        self.ax.set_xticks(range(self.width))
        self.ax.set_yticks(range(self.height))
        self.ax.grid(True)

        self.ax.set_aspect('equal', adjustable='box')
        self.fig.set_size_inches(self.width, self.height)
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

        # Dibujar agentes
        for agente in self.agents:
            if agente.pos is not None:
                x, y = agente.pos
                if agente.age < 5:
                    self.ax.plot(x + 0.5, y + 0.5, marker='o', color='pink', markersize=20, linestyle='')
                else:
                    if agente.sex == "hombre":
                        imagebox = OffsetImage(self.agent_img, zoom=0.05)
                    elif agente.sex == "mujer":
                        imagebox = OffsetImage(self.agent_img_fem, zoom=0.05)
                    else:
                        continue  # Skip if sex is not recognized
                    ab = AnnotationBbox(imagebox, (x + 0.5, y + 0.5), frameon=False)
                    self.ax.add_artist(ab)

        # Dibujar comida
        for comida in self.food:
            if comida.pos is not None:
                x, y = comida.pos
                imagebox = OffsetImage(self.food_img, zoom=0.1)
                ab = AnnotationBbox(imagebox, (x + 0.5, y + 0.5), frameon=False)
                self.ax.add_artist(ab)

        # Dibujar agua
        for water in self.water:
            for pos in water.positions:
                if pos is not None:
                    x, y = pos
                    self.ax.plot(x + 0.5, y + 0.5, marker='s', color='blue', markersize=72, linestyle='')

        # Dibujar y pausar
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        plt.pause(0.1)