from abc import abstractmethod
from os import posix_spawn
from vector3 import *

class SceneObj:

    @abstractmethod
    def intersection(self, ray_origin, direction_vector):
        pass

    @abstractmethod
    def color_at(self, point):
        pass

    @abstractmethod
    def normal_at(self, point):
        pass

class Sphere(SceneObj):
    def __init__(self, scale, center, radius, color):
        self.scale = scale
        self.center = center
        self.radius = radius
        self.color = color

    # return format: (point of intersection, color, normal at intersection)
    def intersection(self, ray_origin, direction_vector):
        # ========== RAY PARAMETRIC ==========
        # / x = rx + x1*t
        # { y = ry + y1*t
        # \ z = rz + z1*t
        #
        # ======== SPHERE PARAMETRIC =========
        # (x-x0)^2 + (y-y0)^2 + (z-z0)^2 = r^2

        x1, y1, z1 = direction_vector
        x0, y0, z0 = self.center
        rx, ry, rz = ray_origin

        a = x1**2 + y1**2 + z1**2                                   # a term of quadratic
        b = 2*(x1*(rx-x0) + y1*(ry-y0) + z1*(rz-z0))                # b term of quadratic
        c = (x0-rx)**2 + (y0-ry)**2 + (z0-rz)**2 - self.radius**2   # c term of quadratic

        discriminant = b**2 - 4*a*c
        t = None
        if discriminant >= 0:
            t = min(((-b + (discriminant)**(1/2))/(2*a), (-b - (discriminant)**(1/2))/(2*a)))

        if t != None:
            return (x1*t, y1*t, z1*t, t)
    
    def color_at(self, point):
        return self.color

    def normal_at(self, point):
        x,y,z = point
        return norm3((x - self.center[0], y - self.center[1], z - self.center[2]))

class Plane(SceneObj):
    def __init__(self, scale, normal, p0, rotation=0, color1=None, color2=None, texture=None):
        self.scale = scale
        self.a, self.b, self.c = normal
        self.normal = normal
        self.x0, self.y0, self.z0 = p0
        self.p0 = p0
        self.color1 = color1
        self.color2 = color2
        self.texture = texture
        self.rotation = rotation
    
    # return format: (point of intersection, color, direction of reflection vector)
    def intersection(self, ray_origin, direction_vector):
        x1, y1, z1 = direction_vector
        rx, ry, rz = ray_origin
        l1 = (self.a*(self.x0-rx) + self.b*(self.y0-ry) + self.c*(self.z0-rz))
        l2 = (self.a*x1 + self.b*y1 + self.c*z1)
        t = l1 / l2 if l2 != 0 else None

        if t != None:
            x = x1*t
            y = y1*t
            z = z1*t

            return (x,y,z,t)

    def normal_at(self, point):
        return self.normal

    def color_at(self, point):
            x,y,z = point
            # some vector in the plane
            dir1 = norm3(ortho3(self.normal))
            
            # rotation of texture from original rotation
            dir1 = rotate3(self.normal, dir1, self.rotation)

            # vector orthogonal to the normal and dir1
            dir2 = norm3(crossp3(self.normal, dir1))

            # the point in the plane scaled for texture mapping
            f = [(self.x0 + x)*self.scale, (self.y0 + y)*self.scale, (self.z0 + z)*self.scale]

            # textures are first priority
            if self.texture == None:
                # check if checkerboarding is an option
                if self.color2 is not None:
                    return self.color2 if int(dotp3(f,dir1)) // int(self.scale/16) % 2 == int(dotp3(f,dir2) // int(self.scale/16) % 2) else self.color1
                else:
                    return self.color1
            else:
                # get pixel from texture at point of intersection
                return self.texture.get_at((int(dotp3(f,dir1)*50/self.scale) % (self.texture.get_width() - 1), int(dotp3(f,dir2)*50/self.scale) % (self.texture.get_height() - 1)))
            
    
    def rotate(self, angle):
        self.rotation += angle

class LightSource:
    def __init__(self, pos, color, luminosity=1):
        self.pos = pos
        self.color = color
        self.luminosity = luminosity