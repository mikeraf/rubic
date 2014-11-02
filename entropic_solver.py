# -*- coding: utf-8 -*-
"""
Created on Sun Nov 2 22:00:00 2014

@author: michar
"""
from Configurator import *
from Cube import *

def try_reduce_entropy(cube, cur_entropy):
    good_moves = {}
    for f in xrange(6):
        for n in xrange(1,4,1):
            cube.rotate(f,n)
            new_entropy = get_configuration_entropy(cube)
            if new_entropy < cur_entropy:
                good_moves[(f,n)] = new_entropy
                # revert rotation to check for better
                cube.rotate(f,-n)
            else:
                continue
            pass
        pass
    if good_moves:
        best_move = min(good_moves.keys(), key=lambda k: good_moves[k])
        cube.rotate(*best_move)
        return True
    else:
        return False

def main():
    c = Cube()
    randomize(c, 100)
    print c
    for i in xrange(100):
        entropy = get_configuration_entropy(c)
        print 'current entropy is:', entropy
        if entropy == 0.0:
            return
        
        reduced = try_reduce_entropy(c, entropy)    
        if reduced:
            print 'succeeded to reduce!'
            continue
        else:
            print 'trying backtracking...'
            break
            #reduced = try_backtracking(c, entropy)
            #if reduced:
                #print 'success'
            #else:       
                #print 'Failed!'
                #break
            
            #pass
        pass
    print c

if __name__ == '__main__':
    main()