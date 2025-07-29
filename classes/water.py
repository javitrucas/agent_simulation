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
        patch_size = random.randint(3, 10)
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

        return list(positions)
