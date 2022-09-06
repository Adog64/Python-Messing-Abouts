# 3D vector functions

from math import sin,cos

iHat = [1,0,0]
jHat = [0,1,0]
kHat = [0,0,1]


# similar to cross product: arbitrary vector orthogonal to v
def ortho3(v):
    w = (v[0]+1, v[1]+1, v[2]+1)
    return [(v[1]*(w[2]) - v[2]*(w[1])), 
            -(v[0]*(w[2]) - v[2]*(w[0])),
            (v[0]*(w[1]) - v[1]*(w[0]))]


# u dot v
def dotp3(u,v):
    return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]


# u cross v
def crossp3(u,v):
    return [(u[1]*(v[2]) - u[2]*(v[1])), 
            -(u[0]*(v[2]) - u[2]*(v[0])),
            (u[0]*(v[1]) - u[1]*(v[0]))]


# scale vector v by scalar x
def scalarp3(v,x):
    return [x*v[0], x*v[1], x*v[2]]


# add
def add3(u, v):
    return [u[0] + v[0], u[1] + v[1], u[2] + v[2]]


# subtract vector v from vector u
def sub3(u, v):
    return [u[0] - v[0], u[1] - v[1], u[2] - v[2]]


# length of vector v
def abs3(v):
    return (v[0]**2 + v[1]**2 + v[2]**2)**(1/2)


# normalize v
def norm3(v):
    d = abs3(v)
    return [v[0]/d, v[1]/d, v[2]/d]


# rotate v around arbitrary axis n with angle t
def rotate3(n,v,t):
    return add3(add3(scalarp3(n, dotp3(n,v)), crossp3(scalarp3(crossp3(n,v), cos(t)), n)), scalarp3(crossp3(n,v), sin(t)))


# reflect v off of surface with normal n at point of contact
def reflect3(v, n):
    return sub3(v, scalarp3(n, 2*dotp3(v,n)))


# displacement of vector list l
def sum3(l):
    u = [0,0,0]
    for v in l:
        u = add3(u,v)
    return u


# total distance along 3d path traced by vector list l
def distance3(l):
    return sum([abs3(v) for v in l])