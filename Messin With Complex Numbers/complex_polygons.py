''' 
Using Euler's identity to draw animated n-gons in pygame

30 April, 2022 - Aidan Sharpe
'''


from math import e, pi
import sys
import pygame
from pygame.locals import *

pygame.init()
disp = pygame.display.set_mode((500, 500))

# polygon constants
VERTICIES = 5
RADIUS = 100
EDGE_THICKNESS = 2

# colors
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)

# animation
FPS = 60
fpsclock = pygame.time.Clock()
ROTATIONS_PER_SECOND = 0.1

def main():
    angle_offset = 0
    while True:
        # clear canvas
        disp.fill(BLACK)

        # check for termination
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        # calculate vertex coordinates
        points = []
        for p in range(VERTICIES):
            theta = 2*pi*(p/VERTICIES) + angle_offset
            points.append(RADIUS*e**(theta*1j))

        # draw edges connecting adjacent verticies
        for p in range(len(points)):
            pygame.draw.line(disp, WHITE,
                (250 + int(points[p-1].real), 250 - int(points[p-1].imag)),
                (250 + int(points[p].real), 250 - int(points[p].imag)),
                EDGE_THICKNESS)

        # calculate change in angle between frames
        angle_offset = 2*pi*ROTATIONS_PER_SECOND / FPS + angle_offset if angle_offset < 2*pi else 0

        # update
        pygame.display.update()
        fpsclock.tick(FPS)



if __name__ == '__main__':
    main()