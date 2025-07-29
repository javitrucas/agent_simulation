import random

class Food:
    def __init__(self, map, energy=5):
        self.map = map
        self.energy = energy
        
        # Parche original con posiciones fijas de comida (los "árboles")
        self.original_positions = self.generate_food_patch(map)
        
        # Inicialmente, la comida está disponible en esas posiciones
        self.positions = list(self.original_positions)
        
        # Control para la regeneración
        self.iterations_since_eaten = 0
        self.reset_after = random.randint(3, 15)
        
        # Estado para saber si la comida está "creciendo"
        self.is_growing = False

    def eaten(self, pos):
        if pos in self.positions:
            self.positions.remove(pos)
            # Si ya no queda comida, empieza el crecimiento
            if len(self.positions) == 0:
                self.is_growing = True
                self.iterations_since_eaten = 0
                self.reset_after = random.randint(3, 15)

    def is_on_water(self, pos):
        water_positions = set()
        for w in self.map.water:
            water_positions.update(w.positions)
        return pos in water_positions

    def generate_food_patch(self, map):
        patch_size = random.randint(2, 4)
        attempts = 0
        while True:
            attempts += 1
            start_x = random.randint(0, map.width - 1)
            start_y = random.randint(0, map.height - 1)
            positions = set()
            positions.add((start_x, start_y))

            while len(positions) < patch_size:
                x, y = random.choice(list(positions))
                directions = [(0,1), (1,0), (0,-1), (-1,0)]
                dx, dy = random.choice(directions)
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < map.width and 0 <= new_y < map.height:
                    positions.add((new_x, new_y))

            if not any(self.is_on_water(p) for p in positions):
                return list(positions)

            if attempts > 100:
                raise RuntimeError("No se pudo generar parche de comida sin agua")

    def update(self):
        if self.is_growing:
            self.iterations_since_eaten += 1
            if self.iterations_since_eaten >= self.reset_after:
                # La comida vuelve a crecer en las posiciones originales
                self.positions = list(self.original_positions)
                self.is_growing = False
