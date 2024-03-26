import random

class DragonPlay:
    def __init__(self, board, type="simple"):
        self.board = board
        self.type = type

    def chooseMovement(self):
        if self.type == "simple":
            return self.simpleMovement()
        else:
            return self.aiMovement()
        
    def simpleMovement(self):
        emptyPositions = []

        for i in range(0, 9):
            if self.board[i] == "E":
                emptyPositions.append(i)
                
        if len(emptyPositions) == 0:
            print("No empty position to play!")
            return -1
        
        if random.choice([True, False]):
            # Choose the fist empty position and play there
            return emptyPositions[0]
     
        else:
            # Choose a random empty position and play there
            return random.choice(emptyPositions)

    def aiMovement(self):
        print("Coming soon...")
        return -1
