'''
Rasterize a 3d scene into an image


Clip plane is defined as the screen in front of camera.
One ray is drawn per pixel in canvas from camera, through pixel, to object intersection
'''

from audioop import cross
from math import cos, sin, pi
import sys
import pygame as pg
from pygame.locals import *

SIZE = 600
def main():
    pg.init()

    # canvas dimensions
    WIDTH = SIZE
    HEIGHT = SIZE
    
    WINDOW = pg.display.set_mode((WIDTH, HEIGHT))
    frames = []

    camera = (0,0,0)    # 3d location of camera
    x1 = int(5*SIZE/8)             # distance from camera to canvas

    scene_objs = [
        Sphere([int(9.5*SIZE/8), 0, 0], int(3*SIZE/8), [0,255,0]),
        Sphere([int(8.5*SIZE/8), int(3*SIZE/8), 0], int(SIZE/4), [0,0,255]),
        Plane([0,1,0], [0,int(-4*SIZE/8),0], 0, texture=pg.image.load('wall.jpg')),
        Plane([0,1,0], [0,int(4*SIZE/8),0], 0, texture=pg.image.load('wall.jpg')),
        Plane([0,0,1], [0,0,int(-3*SIZE/8)], pi/4, texture=pg.image.load('floor.jpg')),
        Plane([1,0,0], [int(6*SIZE/4), 0,0], pi/4,[0,0,0], texture=pg.image.load('wall.jpg')),
        Plane([0,0,1], [0, 0,int(5*SIZE/8)], pi/4,[0,0,0], texture=pg.image.load('ceiling.jpg')),
        #Circle([1,1,-1], [8*SIZE/8, SIZE/8, -SIZE/4], SIZE/4, [255,255,255]),
        ]

    frame_count = 1

    # render
    for i in range(frame_count):
        frames.append(pg.Surface((WIDTH, HEIGHT)))
        for z in range(HEIGHT):
            z1 = -z + HEIGHT/2
            for y in range(WIDTH):
                y1 = y - WIDTH/2
                
                distances = []
                colors = []
                for o in scene_objs:
                    intersection = o.intersection(camera, (x1, y1, z1))
                    if intersection != None:
                        distances.append(intersection[0])
                        colors.append(intersection[1])
                
                if len(distances) > 0:
                    d = min(distances)
                    c = colors[distances.index(d)]

                    d = (d/(5*SIZE/8))**2

                    c = (min(255, int(c[0]/d)), min(255, int(c[1]/d)), min(255, int(c[2]/d)))
                    frames[i].set_at((y, z), c)        
    print('done.')
    
    frame = 0
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
        WINDOW.blit(frames[frame%frame_count], (0,0,WIDTH,HEIGHT))
        pg.display.update()
        pg.time.Clock().tick(1)
        frame += 1

class Sphere:
    def __init__(self, center, radius, color):
        self.center = center
        self.radius = radius
        self.color = color

    def intersection(self, camera, plane_point):
        # === RAY PARAMETRIC ===
        # / x = camera[0] + x1*t
        # { y = camera[1] + y1*t
        # \ z = camera[2] + z1*t

        x1, y1, z1 = plane_point
        a = x1**2 + y1**2 + z1**2                                                           # a term of quadratic
        b = -2*(x1*self.center[0] + y1*self.center[1] + z1*self.center[2])                  # b term of quadratic
        c = self.center[0]**2 + self.center[1]**2 + self.center[2]**2 - self.radius**2      # c term of quadratic

        discriminant = b**2 - 4*a*c
        t = None
        if discriminant >= 0:
            t = min(((-b + (discriminant)**(1/2))/(2*a), (-b - (discriminant)**(1/2))/(2*a)))

        if t != None and t > 0:
            return (((x1*t)**2 + (y1*t)**2 + (z1*t)**2)**(1/2), self.color)

class Plane:
    def __init__(self, normal, p0, rotation=0, color1=None, color2=None, texture=None):
        self.a, self.b, self.c = normal
        self.normal = normal
        self.x0, self.y0, self.z0 = p0
        self.p0 = p0
        self.color1 = color1
        self.color2 = color2
        self.texture = texture
        self.rotation = rotation
    
    def intersection(self, camera, plane_point):
        x1, y1, z1 = plane_point
        l1 = (self.a*self.x0 + self.b*self.y0 + self.c*self.z0)
        l2 = (self.a*x1 + self.b*y1 + self.c*z1)
        t = l1 / l2 if l2 != 0 else None

        if t != None and t > 0:
            x = x1*t
            y = y1*t
            z = z1*t

            d = abs3((x,y,z))

            # checkerboarding
            dir1 = norm3(ortho3(self.normal))
            
            # rotate dir1 for fun
            dir1 = rotate3(self.normal, dir1, self.rotation)

            dir2 = norm3(ortho3(self.normal, dir1))

            f = [self.x0 + x, self.y0 + y, self.z0 + z]
            if self.texture == None:
                c = self.color2 if int(dotp3(f,dir1)) // int(SIZE/16) % 2 == int(dotp3(f,dir2) // int(SIZE/16) % 2) else self.color1
            else:
                # get pixel from texture at point of intersection
                c = self.texture.get_at((int(dotp3(f,dir1)) % (self.texture.get_width() - 1), int(dotp3(f,dir2) % (self.texture.get_height() - 1))))
            return (d, c)
    
    def animate(self):
        self.rotation += pi/8

class Circle:
    def __init__(self, normal, center, radius, color):
        self.normal = normal
        self.a, self.b, self.c = normal
        self.p0 = center
        self.x0, self.y0, self.z0 = center
        self.radius = radius
        self.color = color

    def intersection(self, camera, plane_point):
        x1, y1, z1 = plane_point
        l1 = (self.a*self.x0 + self.b*self.y0 + self.c*self.z0)
        l2 = (self.a*x1 + self.b*y1 + self.c*z1)
        t = l1 / l2 if l2 != 0 else None

        if t != None and t > 0:
            x = x1*t
            y = y1*t
            z = z1*t

            d = abs3((x,y,z))

            f = [self.x0 - x, self.y0 - y, self.z0 - z]

            if abs3(f) <= self.radius:
                return (d, self.color)



def ortho3(a, b=None):
    if b == None:
        b = (a[0]+1, a[1]+1, a[2]+1)
    return [(a[1]*(b[2]) - a[2]*(b[1])), 
            -(a[0]*(b[2]) - a[2]*(b[0])),
            (a[0]*(b[1]) - a[1]*(b[0]))]

def dotp3(a,b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def crossp3(a,b):
    return [(a[1]*(b[2]) - a[2]*(b[1])), 
            -(a[0]*(b[2]) - a[2]*(b[0])),
            (a[0]*(b[1]) - a[1]*(b[0]))]

def scalarp3(v,x):
    return [x*v[0], x*v[1], x*v[2]]

def add3(a, b):
    return [a[0] + b[0], a[1] + b[1], a[2] + b[2]]

def abs3(a):
    return (a[0]**2 + a[1]**2 + a[2]**2)**(1/2)

def norm3(a):
    d = abs3(a)
    return [a[0]/d, a[1]/d, a[2]/d]


def rotate3(u,x,t):
    return add3(add3(scalarp3(u, dotp3(u,x)), crossp3(scalarp3(crossp3(u,x), cos(t)), u)), scalarp3(crossp3(u,x), sin(t)))

if __name__ == '__main__':
    main()