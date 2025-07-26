class Food:
    def __init__(self, pos, energy=5):
        self.pos = pos
        self.energy = energy

    def eaten(self):
        self.pos = None