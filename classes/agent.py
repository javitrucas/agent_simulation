import random

class Agent:
    def __init__(self, pos, energy=10, velocity=1, history=None, hunger_threshold=10, age=1):
        self.pos = pos
        self.energy = energy
        self.velocity = velocity
        self.history = []
        self.hunger_threshold = hunger_threshold
        self.age = age

    def random_move(self, map):
        if self.energy <= 0 or self.pos is None:
            print("El agente no puede moverse porque se ha quedado sin energía.")
            return

        movimientos = [norte, sur, este, oeste, stay]
        random.shuffle(movimientos)  # Para probar primero direcciones aleatorias

        for direccion in movimientos:
            nueva_pos = direccion(self)
            x, y = nueva_pos
            if 0 <= x < map.width and 0 <= y < map.height:
                self.pos = nueva_pos
                break  # Se mueve solo a la primera posición válida

    def smart_move(self, map):
        if self.is_hungry():
            ideal_pos = self.search_for_food(map)
            if ideal_pos is not None:
                self.move_towards(ideal_pos)
            else:
                self.random_move(map)
        else:
            # Implementar lógica para moverse aleatoriamente
            self.random_move(map)

    def update(self, map):
        # Intenta comer cualquier comida que esté en la posición actual
        for food in map.food:
            if self.eat(food):
                food.eaten()  # Marca la comida como comida o elimínala del mapa
                break  # Solo come una comida por actualización

        # Reduce energía al actualizar
        self.energy -= 1
        if self.energy <= 0:
            self.energy = 0
            print("El agente se ha quedado sin energía y MUERE.")
            self.pos = None
        
        if self.energy > 0 and self.pos is not None:
            self.age+=1


        # Guarda la posición actual en el historial
        self.history.append(self.pos)

    def eat(self, food):
        if food.pos == self.pos:
            self.energy += food.energy
            return True
        return False
    
    def is_hungry(self):
        return self.energy <= self.hunger_threshold
    
    def search_for_food(self, map):
        visible_positions = self.view()
        for pos in visible_positions:
            for food in map.food:
                if food.pos == pos:
                    print(f"Comida encontrada en {pos}")
                    return pos
        return None

    def view(self):
        x, y = self.pos
        positions = []
        start_x, start_y = x - 2, y + 2
        for i in range(5):
            for j in range(5):
                pos = (start_x + i, start_y - j)
                positions.append(pos)
        return positions

    def move_towards(self, target_pos):
        if self.pos is None:
            return
        
        x, y = self.pos
        target_x, target_y = target_pos

        if x < target_x:
            x += 1
        elif x > target_x:
            x -= 1

        if y < target_y:
            y += 1
        elif y > target_y:
            y -= 1

        self.pos = (x, y)
                
                

# Fuera de la clase Agent
def stay(agente):
    return agente.pos

def norte(agente):
    pos_old = agente.pos
    pos_new = (pos_old[0], pos_old[1] + 1)
    return pos_new

def sur(agente):
    pos_old = agente.pos
    pos_new = (pos_old[0], pos_old[1] - 1)
    return pos_new

def este(agente):
    pos_old = agente.pos
    pos_new = (pos_old[0] + 1, pos_old[1])
    return pos_new

def oeste(agente):
    pos_old = agente.pos
    pos_new = (pos_old[0] - 1, pos_old[1])
    return pos_new    