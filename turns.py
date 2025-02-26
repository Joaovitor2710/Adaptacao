import numpy as np

class turns:
    def __init__(self, paths):
        """
        paths: List of lists of moves per drone
        """
        self.paths = paths
        self.turns = []

    def __str__(self):
        return (
            '\n'
            f'Turns: {self.turns}\n'
            f'Average: {self.avg:.3f}\n'
            f'Standard Deviation: {self.std:.3f}\n')
    
    def count_turns_2(self):
        for path in self.paths:
            num_turns = -1  # O primeiro movimento não conta como curva
            last_move = None  # Nenhum movimento inicial

            for i in range(1, len(path)):  # Percorre os pontos consecutivos
                x1, y1 = path[i - 1]
                x2, y2 = path[i]

                if x1 == x2:
                    current_move = "vertical"
                elif y1 == y2:
                    current_move = "horizontal"
                else:
                    current_move = "diagonal"  # Opcional, caso queira tratar curvas diagonais

                if last_move and last_move != current_move:
                    num_turns += 1

                last_move = current_move

            self.turns.append(max(0, num_turns))  # Evita valores negativos


    def count_turns(self):
        for path in self.paths:
            num_turns = -1
            last_move = ""
            for move in path:
                if move[0] == move[2]:
                    current_move = "horizontal"
                elif move[1] == move[3]:
                    current_move = "vertical"

                if last_move != current_move:
                    num_turns += 1

                last_move = current_move
            self.turns.append(num_turns)

    def find_avg_and_std(self):
        self.avg = np.average(self.turns)
        self.std = np.std(self.turns)
