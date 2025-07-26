import random

class Agent:
    def __init__(self, pos=None, energy=10, thirst=20, velocity=1, history=None, hunger_threshold=7, thirst_threshold=10, age=1, map=None, sex=None, life_span=None):
        if pos is None:
            self.pos = self.random_position(map)
        else:
            self.pos = pos
        self.energy = energy
        self.thirst = thirst
        self.velocity = velocity
        self.history = []
        self.hunger_threshold = hunger_threshold
        self.thirst_threshold = thirst_threshold
        self.age = age
        self.sex=self.select_sex()
        self.life_span = self.life_span()

    def random_move(self, map):
        if self.energy <= 0 or self.pos is None:
            print("El agente no puede moverse porque se ha quedado sin energía.")
            return

        movimientos = [norte, sur, este, oeste, stay]
        random.shuffle(movimientos)  # Para probar primero direcciones aleatorias

        # Crear conjunto de posiciones con agua
        water_positions = {w.pos for w in map.water if w.pos is not None}

        for direccion in movimientos:
            nueva_pos = direccion(self)
            x, y = nueva_pos
            if (0 <= x < map.width and
                0 <= y < map.height and
                nueva_pos not in water_positions):
                self.pos = nueva_pos
                break  # Solo se mueve a la primera posición válida sin agua

    def smart_move(self, map):
        if self.energy <= 0 or self.pos is None:
            return

        if self.is_hungry():
            ideal_pos = self.search_for_food(map)
            if ideal_pos is not None:
                self.move_towards(ideal_pos)
            else:
                self.random_move(map)
        elif self.is_thirsty():
            ideal_pos = self.search_for_water(map)
            if ideal_pos is not None:
                self.move_towards(ideal_pos)
            else:
                self.random_move(map)
        elif self.energy > 0 and self.thirst > 0:
            self.random_move(map)

    def update(self, map):
        # Intenta comer cualquier comida que esté en la posición actual
        if self.is_hungry(): 
            for food in map.food:
                if self.eat(food):
                    food.eaten()  # Marca la comida como comida o elimínala del mapa
                    break

        # Intenta beber si tiene sed
        if self.is_thirsty():
            for water in map.water:
                if self.drink(water):
                    break  # Solo bebe una vez por turno

        # Reduce energía y sed al actualizar
        self.energy -= 1
        self.thirst -= 1

        # Verifica si el agente ha muerto
        if self.energy <= 0 or self.thirst <= 0:
            self.energy = 0
            self.thirst = 0
            print("El agente se ha quedado sin energía o agua y MUERE.")
            self.pos = None

        # Actualiza la edad y el historial de posiciones
        if self.energy > 0 and self.pos is not None:
            self.age += 1
            self.history.append(self.pos)


    def eat(self, food):
        if food.pos == self.pos:
            self.energy += food.energy
            return True
        return False
    
    def drink(self, water):
        x, y = self.pos
        drinkable_area = [
            (x, y),            # Centro
            (x + 1, y),        # Derecha
            (x - 1, y),        # Izquierda
            (x, y + 1),        # Abajo
            (x, y - 1)         # Arriba
        ]

        if water.pos in drinkable_area:
            print(f"Agente bebe agua en {water.pos}")
            self.thirst += water.energy
            return True
        return False

    def is_hungry(self):
        return self.energy <= self.hunger_threshold
    
    def is_thirsty(self):
        return self.thirst <= self.thirst_threshold
    
    def search_for_food(self, map):
        visible_positions = self.view()
        for pos in visible_positions:
            for food in map.food:
                if food.pos == pos:
                    print(f"Comida encontrada en {pos}")
                    return pos
        return None

    def search_for_water(self, map):
        visible_positions = self.view()
        for pos in visible_positions:
            for water in map.water:
                if water.pos == pos:
                    print(f"Agua encontrada en {pos}")
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
    
    def random_position(self, map):
        x = random.randint(0, map.width - 1)
        y = random.randint(0, map.height - 1)
        return (x, y)
    
    def select_sex(self):
        sexos = ["hombre", "mujer"]
        return random.choice(sexos)
    
    def life_span(self):
        return random.randint(40, 100)

                
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