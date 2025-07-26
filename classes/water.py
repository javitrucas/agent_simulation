import random

class Water:
    def __init__(self, pos=None, energy=10, map=None):
        if pos is None:
            self.pos = self.random_position(map)
        else:
            self.pos = pos
        self.energy = energy
    
    def random_position(self, map):
        x = random.randint(0, map.width - 1)
        y = random.randint(0, map.height - 1)
        return (x, y)