import random

class Water:
    def __init__(self, pos=None, energy=5, map=None):
        if pos is None and map is not None:
            self.positions = self.generate_water_patch(map)
        elif pos is not None:
            self.positions = [pos]
        else:
            self.positions = []
        self.energy = energy

    # Esto hecho con IA
    def generate_water_patch(self, map):
        patch_size = random.randint(5, 10)
        max_attempts = 200
        min_distance = min(map.width, map.height) // 4  # Puedes ajustar esto

        if not hasattr(map, 'water_patch_centers'):
            map.water_patch_centers = []

        for attempt in range(max_attempts):
            start_x = random.randint(0, map.width - 1)
            start_y = random.randint(0, map.height - 1)
            center = (start_x, start_y)

            # Verificar distancia mínima respecto a otros centros de agua
            too_close = False
            for c in map.water_patch_centers:
                dist = abs(center[0] - c[0]) + abs(center[1] - c[1])
                if dist < min_distance:
                    too_close = True
                    break
            if too_close:
                continue

            # Generar parche si está suficientemente lejos
            positions = set()
            positions.add(center)

            while len(positions) < patch_size:
                x, y = random.choice(list(positions))
                directions = [(0,1), (1,0), (0,-1), (-1,0)]
                dx, dy = random.choice(directions)
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < map.width and 0 <= new_y < map.height:
                    positions.add((new_x, new_y))

            map.water_patch_centers.append(center)
            return list(positions)

        raise RuntimeError("No se pudo generar parche de agua bien distribuido")
