import pygame
from pygame.locals import *
import sys

pygame.init()

SIZE = 600

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)

def main():
    player = pygame.mixer.Sound("cdda:///O:/")
    player.play()
    disp = pygame.display.set_mode((SIZE, SIZE))
    while True:
        disp.fill(BLACK)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    main()