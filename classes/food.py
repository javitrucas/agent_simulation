import random

class Food:
    def __init__(self, pos=None, energy=5, map=None):
        if pos is None:
            self.pos = self.random_position(map)
        else:
            self.pos = pos
        self.energy = energy

    def eaten(self):
        self.pos = None

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
