import sys
import pygame
from random import choice
from pygame.locals import *

pygame.init()

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)

SIZE = 600

fpsclock = pygame.time.Clock()
FPS = 10

font = pygame.font.SysFont('arial', 20)

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


def main():
    cells = []
    entropy = 0
    del_entropy = 0
    vals = []
    for i in range(81):
        n = input('Number or blank: ')
        if len(n) > 0:
            n = eval(n)
        else:
            n = 0
        while n not in range(10):
            print('bad input')
            n = input('Number or blank: ')
            if len(n) > 0:
                n = eval(n)
            else:
                n = 0
        vals.append(n)

    for row in range(9):
        for col in range(9):
            c = cell(row, col, 3*(row//3) + (col//3), vals[9*row+col])
            cells.append(c)
            entropy += c.entropy

    disp = pygame.display.set_mode((SIZE, SIZE))
    ico = pygame.image.load('SudokuSolver/icon.jpg')
    pygame.display.set_caption('Sudoku')
    pygame.display.set_icon(ico)
    

    while True:
        disp.fill(BLACK)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                print(entropy)
                for c in cells:
                    if c.entropy == 1:
                        for s in cells:
                            if len(s.superposition) > 1 and (s.row == c.row or s.col == c.col or s.metacell == c.metacell):
                                s.reduce(c.superposition[0])
                del_entropy = entropy - sum([c.entropy for c in cells])
                if del_entropy == 0:
                    min_entropy = 10
                    min_cell = None
                    for c in cells:
                        if 1 < c.entropy < min_entropy:
                            min_cell = c
                    if min_cell is not None:
                        min_cell.collapse()
                entropy = sum([c.entropy for c in cells])

        for i in range(8):
            pygame.draw.line(disp, WHITE, (0, (i+1)*SIZE // 9), (SIZE, (i+1)*SIZE // 9))
            pygame.draw.line(disp, WHITE, ((i+1)*SIZE // 9, 0), ((i+1)*SIZE // 9, SIZE))
        for i in range(81):
            x1 = int((SIZE / 9) * (i % 9))
            y1 = int((SIZE / 9) * (i // 9))
            for a in range(3):
                for b in range(3):
                    num = 3*a+(b+1)
                    if num in cells[i].superposition:
                        f_surf = font.render(f'{num}', True, WHITE)
                        f_rect = f_surf.get_rect()
                        f_rect.topleft = (x1 + b*15 + 5, y1 + a*20 + 5)
                        disp.blit(f_surf, f_rect)
        
        pygame.display.update()
        fpsclock.tick(FPS)

if __name__ == '__main__':
    main()