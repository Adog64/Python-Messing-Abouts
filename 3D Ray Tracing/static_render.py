from math import pi
import sys
import pygame as pg
from pygame.locals import *
from vector3 import *
from scene_objs import *

SCALE = 250 # pixels per tile
BRIGHTNESS = 3

MAX_DEPTH = 1

# objects in scene
scene_objs = [
    Sphere(SCALE, [2,0,-2], 1, [220, 10,10]),
    Plane(SCALE, [0,1,0], [0,3,0], pi/4, texture=pg.image.load('wall.jpg')),
    Plane(SCALE, [0,1,0], [0,-3,0], pi/4, texture=pg.image.load('wall.jpg')),
    # Plane(SCALE, [1,0,0], [2, 0,0], pi/4, texture=pg.image.load('wall.jpg')),
    # Plane(SCALE, [1,0,0], [-6, 0,0], pi/4,texture=pg.image.load('wall.jpg')),
    Plane(SCALE, [0,0,1], [0,0,-3], pi/4, texture=pg.image.load('floor.jpg')),
    Plane(SCALE, [0,0,1], [0, 0,3], pi/4,[0,0,0], texture=pg.image.load('ceiling.jpg')),
]

light_sources = [
    LightSource((2,0,2.95), (255,255,255), 50),
]

camera = (-1,0,0)
pitch = 0
roll = 0
yaw = 0

def main():
    pg.init()
    WIDTH = SCALE*2
    HEIGHT = SCALE*2

    WINDOW = pg.display.set_mode((WIDTH, HEIGHT))

    # loop over pixels
    x1 = camera[0] + 0.5
    for z in range(HEIGHT):
        print(f'\rRendering... [{int(100*(z+1)/HEIGHT)}%]', end='')

        z1 = (-z + SCALE)/SCALE
        for y in range(WIDTH):
            y1 = (y - SCALE)/SCALE
            c = render_at((x1,y1,z1))
            WINDOW.set_at((y, z), c)
        pg.display.update()
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
    print('done.')

    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()

def render_at(point):
    x,y,z = point
    rc = [0,0,0]
    origin = camera
    dir = (x-camera[0], y+camera[1], z+camera[2])

    dir = rotate3(iHat, dir, roll)
    dir = rotate3(jHat, dir, pitch)
    dir = rotate3(kHat, dir, yaw)

    for i in range(MAX_DEPTH):
        points = [None]*len(scene_objs)
        pdists = []
        dists = [None]*len(scene_objs)
        for j in range(len(scene_objs)):
            intersection = scene_objs[j].intersection(origin, dir)
            if intersection is not None:
                d = dotp3(sub3(intersection,origin), dir)
                points[j] = intersection[:3]
                dists[j] = d
                if d > 0:
                    pdists.append(d)
                

        if len(pdists) > 0:
            d = min(pdists)
            obj_idx = dists.index(d)
            p = points[obj_idx]
            scene_obj = scene_objs[obj_idx]
            c = scene_obj.color_at(p)
            lcl_bright = 0
            for ls in light_sources:
                shadow = False
                r_dir = sub3(ls.pos, p)
                for obj in scene_objs:
                    if obj != scene_objs[obj_idx]:
                        intersection = obj.intersection(p, r_dir)
                        if intersection is not None and 0 < intersection[3] < 1:
                            shadow = True
                            break
                if not shadow:
                    lcl_bright += ls.luminosity / abs3(r_dir)**2 # if there is no shadow ray
            d = d**2 / ((BRIGHTNESS*lcl_bright) or 1)
            return (min(255, int(c[0]/d)),min(255, int(c[1]/d)),min(255, int(c[2]/d)))
    return [0,0,0]


if __name__ == "__main__":
    main()