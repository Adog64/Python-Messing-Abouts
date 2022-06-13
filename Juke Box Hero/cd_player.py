''' Juke Box Hero CD Player

By Aidan Sharpe

Audio CDs in posix operating systems are weird so imma not do this in python
'''

import os
import pygame
from pygame.locals import *
import sys
import posixpath

pygame.init()
SIZE = 600

WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)

if os.name == 'posix':
    os.
    #pygame.mixer.Sound().play()
    disp = pygame.display.set_mode((SIZE, SIZE))
    while True:
        disp.fill(BLACK)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
elif os.name == 'nt':
    pass