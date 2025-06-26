class Snake:
    def __init__(self, initial_pos:list):
        self.positions = []
        self.positions.append(initial_pos)

    def forward(self, next_pos, grow=False):
        self.positions.append(next_pos)
        if not grow:
            return self.positions.pop(0)
        return next_pos

    def return_instance(self):
        return self
        