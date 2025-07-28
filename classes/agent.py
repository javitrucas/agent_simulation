import random

class Agent:
    def __init__(self, pos=None, energy=20, thirst=20, history=None, hunger_threshold=10, thirst_threshold=10, 
                 age=1, map=None, sex=None, life_span=None, times_eaten=0, times_drunk=0, reproduce_threshold=5, reproduction_cooldown=0):
        # Posición Inicial
        if pos is None:
            self.pos = self.random_position(map)
        else:
            self.pos = pos
        
        # Mapa del Agente
        self.map = map
        
        # Atributos del Agente
        self.energy = energy
        self.thirst = thirst
        self.age = age
        self.sex = sex if sex else self.select_sex()
        self.life_span = life_span if life_span else self.lifespan()
        self.hunger_threshold = hunger_threshold
        self.thirst_threshold = thirst_threshold
        self.reproduce_threshold = reproduce_threshold
        self.reproduction_cooldown = reproduction_cooldown
        
        # Historial de acciones
        self.history = []
        self.just_ate = False
        self.just_drank = False
        self.times_eaten = times_eaten
        self.times_drunk = times_drunk
        
    # Movimiento y Comportamiento
    def random_move(self, map):
        if self.is_dead():
            print("El agente no puede moverse porque se ha muerto.")
            return

        movimientos = [norte, sur, este, oeste, stay]
        random.shuffle(movimientos)  # Para probar primero direcciones aleatorias

        # Crear conjunto de posiciones con agua
        water_positions = set()
        for w in map.water:
            water_positions.update(w.positions)
        
        # Crear conjunto de posiciones ocupadas por otros agentes
        occupied_positions = set()
        for agent in map.agents:
            if agent is not self and agent.pos is not None:
                occupied_positions.add(agent.pos)

        for direccion in movimientos:
            nueva_pos = direccion(self)
            x, y = nueva_pos
            if (0 <= x < map.width and
                0 <= y < map.height and
                nueva_pos not in water_positions):
                self.pos = nueva_pos
                break  # Solo se mueve a la primera posición válida sin agua

    def smart_move(self, map):
        if self.is_dead():
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
        elif not self.is_hungry() and not self.is_thirsty() and self.sex=="hombre":
            partner = self.search_for_partner(map)
            if partner is not None:
                self.move_towards(partner.pos, map)
            else:
                self.random_move(map)
        elif self.is_dead() == False:
            self.random_move(map)

    def move_towards(self, target_pos, map=None):
        if self.pos is None or target_pos is None:
            return

        x, y = self.pos
        target_x, target_y = target_pos

        new_x, new_y = x, y
        if x < target_x:
            new_x += 1
        elif x > target_x:
            new_x -= 1

        if y < target_y:
            new_y += 1
        elif y > target_y:
            new_y -= 1

        new_pos = (new_x, new_y)

        if map:
            water_positions = set()
            for w in map.water:
                water_positions.update(w.positions)
            if new_pos in water_positions:
                return  # No moverse al agua
        
        if map:
            for agent in map.agents:
                if agent is not self and agent.pos == new_pos:
                        return 


        self.pos = new_pos

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
                if pos in water.positions:
                    print(f"Agua encontrada en {pos}")
                    return pos
        return None
    
    def search_for_partner(self, map):
        visible_positions = self.view()
        for pos in visible_positions:
            for agent in map.agents:
                if agent is not self and agent.pos == pos:
                    if self.can_reproduce_with(agent):
                        print(f"Pareja compatible encontrada en {pos}")
                        return agent 
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

    # Actualización del Agente
    def update(self, map):
        self.just_ate = False
        self.just_drank = False

        # Intenta comer cualquier comida que esté en la posición actual
        if self.is_hungry(): 
            for food in map.food:
                if self.eat(food):
                    self.just_ate = True
                    food.eaten()  # Marca la comida como comida o elimínala del mapa
                    break

        # Intenta beber si tiene sed
        if self.is_thirsty():
            for water in map.water:
                if self.drink(water):
                    self.just_drank = True
                    break  # Solo bebe una vez por turno

        # Actualiza el cooldown de reproducción
        if self.reproduction_cooldown > 0:
            self.reproduction_cooldown -= 1

        # Intentar reproducirse si hay pareja cerca
        if not self.is_dead() and not self.is_hungry() and not self.is_thirsty():
            for agent in map.agents:
                if agent is not self and self.can_reproduce_with(agent):
                    self.reproduce(agent)
                    break

        # Reduce energía y sed al actualizar
        self.energy -= 1
        self.thirst -= 1

        # Verifica si el agente ha muerto
        if self.is_dead():
            print("El agente se ha quedado sin energía o agua y MUERE.")
            self.pos = None
            #self.age = -1  # Marca la edad como -1 para indicar que está muerto

        # Actualiza la edad y el historial de posiciones
        if self.is_dead() == False:
            self.age += 1
            self.history.append(self.pos)

    # Acciones del Agente
    def eat(self, food):
        if food.pos == self.pos:
            self.energy += food.energy
            self.times_eaten+=1
            return True
        return False
    
    def drink(self, water):
        x, y = self.pos
        drinkable_area = [
            (x, y),
            (x + 1, y),
            (x - 1, y),
            (x, y + 1),
            (x, y - 1)
        ]

        for pos in drinkable_area:
            if pos in water.positions:
                self.thirst += water.energy
                self.times_drunk+=1
                print(f"Agente bebe agua en {pos}")
                return True
        return False
    
    def can_reproduce_with(self, other):
        return (
            self.sex != other.sex and
            self.age >= self.reproduce_threshold and other.age >= other.reproduce_threshold and
            not self.is_hungry() and not self.is_thirsty() and
            not other.is_hungry() and not other.is_thirsty() and
            abs(self.pos[0] - other.pos[0]) <= 1 and
            abs(self.pos[1] - other.pos[1]) <= 1 and 
            self.reproduction_cooldown <= 0 and other.reproduction_cooldown <= 0
        )

    
    def reproduce(self, partner):
        if self.can_reproduce_with(partner) and self.sex == "mujer":
            child = Agent(pos=self.pos, map=self.map)
            self.map.agents.append(child)
            print(f"NACIMIENTO de un nuevo agente en {self.pos}, sexo {child.sex}")
            self.reproduction_cooldown = 3
            partner.reproduction_cooldown = 3
            return child
        return None

    # Métodos de consulta del Agente
    def is_hungry(self):
        return self.energy <= self.hunger_threshold
    
    def is_thirsty(self):
        return self.thirst <= self.thirst_threshold
    
    def is_dead(self):
        return self.energy <= 0 or self.thirst <= 0 or self.age > self.life_span
    
    # Métodos de estado del Agente
    def random_position(self, map):
        water_positions = set()
        for w in map.water:
            water_positions.update(w.positions)

        while True:
            x = random.randint(0, map.width - 1)
            y = random.randint(0, map.height - 1)
            pos = (x, y)
            if pos not in water_positions:
                return pos

    def select_sex(self):
        sexos = ["hombre", "mujer"]
        return random.choice(sexos)
    
    def lifespan(self):
        return random.randint(40, 100)
    
    def couse_death(self):
        if self.age >= self.life_span:
            return "Edad"
        elif self.energy <= 0:
            return "Energía"
        elif self.thirst <= 0:
            return "Sed"
        else:
            return "Desconocido"
                
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