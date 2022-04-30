from random import choice

def main():
    vals = [[9, 1, 0, 4, 0, 0, 0, 0, 0],
            [0, 7, 4, 0, 0, 0, 8, 9, 0],
            [0, 0, 0, 0, 6, 0, 0, 0, 1],
            [0, 0, 0, 8, 2, 0, 3, 0, 9],
            [0, 0, 7, 9, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 4, 0, 6, 1, 0],
            [0, 0, 8, 6, 0, 3, 0, 0, 0],
            [3, 9, 0, 2, 0, 4, 5, 6, 8],
            [7, 2, 6, 5, 0, 1, 9, 0, 4]]

    cells = []
    entropy = 0
    for row in range(9):
        for col in range(9):
            c = cell(row, col, 3*(row//3) + (col//3), vals[row][col])
            cells.append(c)
            entropy += c.entropy

    print(entropy)

    # while not solved
    while(entropy > len(cells)):
        for c in cells:
            if c.entropy == 1:
                for s in cells:
                    if len(s.superposition) > 1 and (s.row == c.row or s.col == c.col or s.metacell == c.metacell):
                        s.reduce(c.superposition[0])
        
        cell_min_entropy = None
        for c in cells:
            if cell_min_entropy is None and c.entropy > 1:
                cell_min_entropy = c
            elif 1 < c.entropy < cell_min_entropy.entropy:
                cell_min_entropy = c
        
        if cell_min_entropy is not None:
            cell_min_entropy.collapse()
        entropy = sum([c.entropy for c in cells])
        print(entropy)

    for row in range(9):
        for col in range(9):
            if len(cells[9*row + col].superposition) == 1:
                vals[row][col] = cells[9*row + col].superposition[0]
    
    for i in range(9):
        print('-'*37)
        for j in range(9):
            print(f'| {" " if vals[i][j] == 0 else vals[i][j]} ', end='')
        print('|')
    print('-'*37)


class cell:
    def __init__(self, row, col, metacell, val=0):
        self.row = row
        self.col = col
        self.metacell = metacell
        self.superposition = []
        if val == 0:
            self.superposition.extend(range(1,10))
        else:
            self.superposition.append(val)
        self.entropy = len(self.superposition)

    def reduce(self, val):
        if (val in self.superposition):
            self.superposition.remove(val)
            self.entropy = len(self.superposition)
    
    def collapse(self):
        val = choice(self.superposition)
        self.superposition.clear()
        self.superposition.append(val)
        self.entropy = len(self.superposition)


if __name__ == '__main__':
    main()