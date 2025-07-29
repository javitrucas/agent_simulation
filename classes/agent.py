import random

class Agent:
    def __init__(self, pos=None, energy=20, thirst=20, history=None, hunger_threshold=8, thirst_threshold=8, 
                 age=1, map=None, sex=None, life_span=None, times_eaten=0, times_drunk=0, reproduce_threshold=5,
                reproduction_cooldown=0, n_children=0, generation=0, memory_water=None, memory_food=None):
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
        self.n_children = n_children
        self.generation=generation
        
        # Historial de acciones
        self.memory_food = memory_food if memory_food is not None else set()
        self.memory_water = memory_water if memory_water is not None else set()
        self.history = history if history is not None else []
        self.just_ate = False
        self.just_drank = False
        self.times_eaten = times_eaten
        self.times_drunk = times_drunk
        
    # Movimiento y Comportamiento
    def random_move(self, map):
        if self.is_dead():
            # print("El agente no puede moverse porque se ha muerto.")
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

        # Decisión de movimiento según necesidades
        target_pos = None

        if self.is_hungry():
            target_pos = self.search_for_food(map)
        elif self.is_thirsty():
            target_pos = self.search_for_water(map)
        elif self.sex == "hombre" and not self.is_hungry() and not self.is_thirsty():
            partner = self.search_for_partner(map)
            if partner:
                target_pos = partner.pos

        # Ejecutar movimiento
        if target_pos:
            self.move_towards(target_pos, map)
        else:
            self.explore_memory_random(map)
  
    def move_towards(self, target_pos, map=None):
        if self.is_dead() or target_pos is None:
            return

        x, y = self.pos
        target_x, target_y = target_pos

        # Movimiento preferente en dirección X, luego Y
        new_x = x + (1 if target_x > x else -1 if target_x < x else 0)
        new_y = y + (1 if target_y > y else -1 if target_y < y else 0)
        new_pos = (new_x, new_y)

        if map:
            # Evita agua
            water_positions = {p for w in map.water for p in w.positions}
            if new_pos in water_positions:
                return

            # Evita colisionar con otros agentes
            if any(agent is not self and agent.pos == new_pos for agent in map.agents):
                return

        self.pos = new_pos

    def explore_memory_random(self, map):
        # Exploración aleatoria con memoria
        movimientos = [norte, sur, este, oeste]
        random.shuffle(movimientos)  # Probar primero direcciones aleatorias

        # Posiciones con agua y ocupadas
        water_positions = {pos for w in map.water for pos in w.positions}
        occupied_positions = {agent.pos for agent in map.agents if agent is not self and agent.pos is not None}

        for direccion in movimientos:
            nueva_pos = direccion(self)
            x, y = nueva_pos

            if (
                0 <= x < map.width and
                0 <= y < map.height and
                nueva_pos not in water_positions and
                nueva_pos not in self.history and
                nueva_pos not in occupied_positions
            ):
                self.pos = nueva_pos
                self.history.append(nueva_pos)
                return

        # Si no hay ninguna nueva dirección válida, moverse aleatoriamente
        self.random_move(map)

    def explore_expansion(self, map):
        # exploracion del mapa por exploracion basada en frentes de expansion
        pass

    def explore_curiosity(self, map):
        # exploracion del mapa por curiosidad artificial/Entropia
        pass    

    def search_for_food(self, map):
        visible_positions = self.view()
        for pos in visible_positions:
            for food in map.food:
                if pos in food.positions:
                    self.memory_food.add(pos)
                    return pos
        return self.search_in_memory(self.memory_food)

    def search_for_water(self, map):
        visible_positions = self.view()
        for pos in visible_positions:
            for water in map.water:
                if pos in water.positions:
                    self.memory_water.add(pos)
                    return pos
        return self.search_in_memory(self.memory_water)
        
    def search_in_memory(self, memory_set):
        if not memory_set:
            return None

        # Devuelve la posición más cercana (Manhattan) al agente dentro de las guardadas en memoria
        return min(memory_set, key=lambda pos: abs(pos[0] - self.pos[0]) + abs(pos[1] - self.pos[1]))
    
    def search_for_partner(self, map):
        visible_positions = self.view()
        for pos in visible_positions:
            for agent in map.agents:
                if agent is not self and agent.pos == pos:
                    if self.can_reproduce_with(agent):
                        # print(f"Pareja compatible encontrada en {pos}")
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
        # Verifica si el agente ha muerto
        if self.is_dead():
            # print("El agente se ha quedado sin energía o agua y MUERE.")
            self.pos = None
            return 

        self.search_for_food(map)
        self.search_for_water(map)

        self.just_ate = False
        self.just_drank = False

        # Intenta comer cualquier comida que esté en la posición actual
        if self.is_hungry(): 
            for food in map.food:
                if self.eat(food):
                    self.just_ate = True
                    food.eaten(self.pos)  # Marca la comida como comida
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

        # Actualiza la edad y el historial de posiciones
        if self.is_dead() == False:
            self.age += 1
            self.history.append(self.pos)

    # Acciones del Agente
    def eat(self, food):
        if self.pos in food.positions:
            self.food_memory = self.pos
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
                self.water_memory = pos
                self.thirst += water.energy
                self.times_drunk+=1
                # print(f"Agente bebe agua en {pos}")
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
            # Crear un nuevo agente hijo
            if self.generation > partner.generation:
                new_generation = self.generation + 1
            else:
                new_generation = partner.generation + 1

            # "Enseñar" al hijo donde hay comida y agua
            child_memory_food = self.memory_food.union(partner.memory_food)
            child_memory_water = self.memory_water.union(partner.memory_water)

            child = Agent(pos=self.pos, map=self.map, generation=new_generation, memory_food=child_memory_food, memory_water=child_memory_water)
            self.map.agents.append(child)
            # print(f"NACIMIENTO de un nuevo agente en {self.pos}, sexo {child.sex}")
            
            # Actualizar los atributos de reproducción
            self.n_children += 1
            partner.n_children += 1
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