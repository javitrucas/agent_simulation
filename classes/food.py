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
        x = random.randint(0, map.width - 1)
        y = random.randint(0, map.height - 1)
        return (x, y)