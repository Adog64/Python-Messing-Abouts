from math import e, pi
import sys
import pygame
from pygame.locals import *

pygame.init()
disp = pygame.display.set_mode((500, 500))

# colors
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)

# animation
FPS = 60
fpsclock = pygame.time.Clock()

def main():
    while True:
        # clear canvas
        disp.fill(BLACK)

        # check for termination
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        vector(disp, (10, 20), (250, 250))

        # update
        pygame.display.update()
        fpsclock.tick(FPS)

def vector(disp, ij, origin):
    tip = (origin[0] + ij[0], origin[1] + ij[1])
    pygame.draw.line(disp, WHITE, origin, tip)


if __name__ == '__main__':
    main()