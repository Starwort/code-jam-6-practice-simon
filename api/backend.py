from random import randint

class SimonSays:
    def __init__(self, *args, **kwargs):
        self.moves = []

    def validate(self, input: list, index: int):
        if input == self.moves[index]:
            return True
        else:
            return False
    
    def add_press(self):
        self.moves.append(randint(1, 4))

    