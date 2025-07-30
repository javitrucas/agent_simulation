import random

class Food:
    def __init__(self, map, energy=10):
        self.map = map
        self.energy = energy
        
        # Parche original con posiciones fijas de comida
        self.original_positions = self.generate_food_patch(map)
        
        # Inicialmente, la comida está disponible en esas posiciones
        self.positions = list(self.original_positions)
        
        # Control para la regeneración
        self.iterations_since_eaten = 0
        self.reset_after = random.randint(2, 4)
        
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
        patch_size = random.randint(3, 5)
        max_attempts = 200
        min_distance = min(map.width, map.height) // 4  # Ajusta para mayor dispersión

        if not hasattr(map, 'food_patch_centers'):
            map.food_patch_centers = []

        for attempt in range(max_attempts):
            start_x = random.randint(0, map.width - 1)
            start_y = random.randint(0, map.height - 1)
            center = (start_x, start_y)

            # Comprobar que el nuevo centro esté lejos de los anteriores
            too_close = False
            for c in map.food_patch_centers:
                dist = abs(center[0] - c[0]) + abs(center[1] - c[1])  # Distancia Manhattan
                if dist < min_distance:
                    too_close = True
                    break
            if too_close:
                continue

            # Si está lejos, generamos el parche
            positions = set()
            positions.add(center)

            while len(positions) < patch_size:
                x, y = random.choice(list(positions))
                directions = [(0,1), (1,0), (0,-1), (-1,0)]
                dx, dy = random.choice(directions)
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < map.width and 0 <= new_y < map.height:
                    positions.add((new_x, new_y))

            if not any(self.is_on_water(p) for p in positions):
                map.food_patch_centers.append(center)
                return list(positions)

        raise RuntimeError("No se pudo generar parche de comida sin agua y bien distribuido")

    def update(self):
        if self.is_growing:
            self.iterations_since_eaten += 1
            if self.iterations_since_eaten >= self.reset_after:
                # La comida vuelve a crecer en las posiciones originales
                self.positions = list(self.original_positions)
                self.is_growing = False
