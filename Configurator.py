# -*- coding: utf-8 -*-
"""
Created on Sun Nov 2 22:00:00 2014

@author: michar
"""
import random
import operator
import math
from Cube import *

__all__ = ['randomize', 'get_configuration_entropy']
def randomize(cube, nsteps):
    '''Apply :nsteps: random rotations on :cube:'''
    for i in xrange(nsteps):
        (f,n) = _random_rotation_params()
        cube.rotate(f,n)
        pass
    pass

def _random_rotation_params():
    f = random.randint(0,5)
    n = random.randint(1,3)
    return f,n

def product(iterable):
    return reduce(operator.mul, iterable, 1)

def get_face_entropy(face):
    '''
    >>> f = Face(1)
    >>> get_face_entropy(f)
    1
    >>> f = Face(range(9))
    >>> get_face_entropy(f)
    362880
    
    '''
    
    vals = face.get_vals()
    d = {}
    for v in vals:
        d[v] = d.get(v,0) + 1
    return math.factorial(9)/product([math.factorial(i) for i in d.values()])

def get_configuration_entropy(cube):
    '''calculate some estimator to cubes' configuration entropy
    
    >>> c = Cube()
    >>> get_configuration_entropy(c)
    0.0
    
    '''
    prod = 1
    for i in xrange(6):
        prod *= get_face_entropy(cube.get_face(i))
    return math.log(prod)

if __name__ == '__main__':
    import doctest
    doctest.testmod()    