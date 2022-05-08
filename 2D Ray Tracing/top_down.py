from cmath import sqrt
from numpy import intersect1d
import pygame as pg
from pygame.locals import *
import sys
from math import sin, cos, radians

from sympy import intersection


pg.init()
WIDTH = 800
HEIGHT = 800
MAX_DIST = (WIDTH**2 + HEIGHT**2)**(1/2) # maximum ray length

YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FPS = 30
fpsClock = pg.time.Clock()

def main():
    
    DISPLAYSURF = pg.display.set_mode((WIDTH, HEIGHT), 0,32)
    pg.display.set_caption("2D Raytracing")

    scene = [Circle((400, 400), 100), Circle((200, 200), 75), Circle((300, 500), 40), Square((600, 600), (100, 100))]

    while True:
        #cast rays
        origin = (pg.mouse.get_pos())
        for Θ in range(360):
            intersection = (origin[0] + MAX_DIST*cos(radians(Θ)), origin[1] + MAX_DIST*sin(radians(Θ)))
            for obj in scene:
                intersection1 = obj.intersects(origin, intersection)
                l = ((origin[0] - intersection[0])**2 + (origin[1] - intersection[1])**2)**(1/2)
                l1 = ((origin[0] - intersection1[0])**2 + (origin[1] - intersection1[1])**2)**(1/2)
                if l1 < l:
                    intersection = intersection1

            pg.draw.line(DISPLAYSURF, YELLOW, origin, intersection, 1)
        
        pg.draw.rect(DISPLAYSURF, RED, (600, 600, 100, 100), 1)
        pg.draw.circle(DISPLAYSURF, RED, (400, 400), 100, 1)
        pg.draw.circle(DISPLAYSURF, RED, (300, 500), 40, 1)
        pg.draw.circle(DISPLAYSURF, RED, (200, 200), 75, 1)

        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

        pg.display.update()
        DISPLAYSURF.fill(BLACK)
        fpsClock.tick(FPS)

class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def intersects(self, ray_start, ray_end):
        intersection = ray_end
        x0, y0 = self.center
        x1, y1 = ray_start
        x2, y2 = ray_end
        a = (x2 - x1)**2 + (y2 - y1)**2
        b = 2*(x2 - x1)*(x1 - x0) + 2*(y2 - y1)*(y1 - y0)
        c = (x1 - x0)**2 + (y1 - y0)**2 - self.radius**2
        t = None
        if (b**2 - 4*a*c) >= 0 and a != 0:
            t1 = (-b + (b**2 - 4*a*c)**(1/2)) / (2*a)
            t2 = (-b - (b**2 - 4*a*c)**(1/2)) / (2*a)
            if (0 <= t1 <= 1) and (0 <= t2 <= 1):
                t = min(t1, t2)
            elif 0 <= t1 <= 1:
                t = t1
            elif 0 <= t2 <= 1:
                t = t2
        if t != None:
            intersection = ((x2 - x1)*t + x1, (y2 - y1)*t + y1)

        return intersection
        

class Square:
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size
    
    def intersects(self, ray_start, ray_end):
        intersection = ray_end
        x1, y1 = ray_start
        x2, y2 = ray_end
        left, top = self.pos
        right = left + self.size[0]
        bottom = top + self.size[1]

        t1, t2 = 2,2
        if y2 != y1:
            t1 = ((top - y1) / (y2 - y1))
            t2 = ((bottom - y1) / (y2 - y1))
        if t1 < 0 or t1 > 1 or not (left <= (x2 - x1)*t1 + x1 <= right):
            t1 = 2
        if t2 < 0 or t2 > 1 or not (left <= (x2 - x1)*t2 + x1 <= right):
            t2 = 2

        t3, t4 = 2,2
        if x2 != x1: 
            t3 = ((left - x1) / (x2 - x1))
            t4 = ((right - x1) / (x2 - x1))
        if t3 < 0 or t3 > 1 or not (top <= (y2 - y1)*t3 + y1 <= bottom):
            t3 = 2
        if t4 < 0 or t4 > 1 or not (top <= (y2 - y1)*t4 + y1 <= bottom):
            t4 = 2

        t = min(t1, t2, t3, t4)
        if 0 <= t <= 1:
            x = (x2 - x1)*t + x1
            y = (y2 - y1)*t + y1
            intersection = (x, y)

        return intersection


if __name__ == '__main__':
    main()