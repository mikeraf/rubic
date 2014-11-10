# -*- coding: utf-8 -*-
"""
Created on Sun Nov 2 22:00:00 2014

@author: michar
"""
from Configurator import *
from Cube import *

class EntropicSolver(object):
    def __init__(self, cube, entropy_estimator):
        self.cube = cube
        self.entropy_estimator = entropy_estimator
        
        self.cur_entropy = entropy_estimator.get_configuration_entropy(cube)
        self.moves = []   
    #---------------------------------------------------------
    def _try_reduce_entropy(self):
        cube = self.cube
        estimator = self.entropy_estimator
        cur_entropy = self.cur_entropy
        
        good_moves = {}
        for f in xrange(6):
            for n in xrange(1,4,1):
                cube.rotate(f,n)
                new_entropy = estimator.get_configuration_entropy(cube)
                # revert rotation to check for better
                cube.rotate(f,-n)       
                if new_entropy < cur_entropy:
                    good_moves[(f,n)] = new_entropy
                else:
                    continue
                pass
            pass
        if good_moves:
            best_move = min(good_moves.keys(), key=lambda k: good_moves[k])
            cube.rotate(*best_move)
            self.moves.append(best_move)
            self.cur_entropy = estimator.get_configuration_entropy(cube)
            return True
        else:
            return False           
    #---------------------------------------------------------
    def _try_backtracking(self, cur_entropy, face=-1, depth=3, recuring=0):
        cube = self.cube
        estimator = self.entropy_estimator
        
        moves = []
        should_break = False
        for f in xrange(6):
            if should_break:
                break
            for n in xrange(1,4,1): 
                if face == f:
                    continue
                cube.rotate(f,n)
                if depth > 0:
                    sub_moves = self._try_backtracking(cur_entropy, f, depth-1, 
                                                       recuring=1)
                    if sub_moves:
                        moves.append((f,n))                
                        moves.extend(sub_moves)
                else: 
                    new_entropy = estimator.get_configuration_entropy(cube)
                    if new_entropy < cur_entropy:
                        moves.append((f,n))
                cube.rotate(f,-n)
                if moves:
                    if recuring:
                        return moves
                    else:
                        should_break = True
                        break
                    pass
                pass
            pass
                
        if not recuring and moves:
            self.moves.extend(moves)
            for move in moves:
                cube.rotate(*move)
            self.cur_entropy = estimator.get_configuration_entropy(cube)
        return moves    
    #---------------------------------------------------------
    def _perform_single_step(self, max_backtracking):
        '''Try to perform single step to reduce entropy.
        return whether succeeded.
        '''
        cube = self.cube
        estimator = self.entropy_estimator        
        
        entropy = self.cur_entropy
        print 'current entropy is:', entropy
        if entropy == 0.0:
            return
        
        reduced = self._try_reduce_entropy()    
        if reduced:
            print 'succeeded to reduce!'
            return True
        else:
            for depth in range(1, max_backtracking+1):
                print 'Trying backtracking: depth=%d...'%depth
                steps = self._try_backtracking(entropy, depth=depth)
                if steps:
                    print 'Success!'
                    return True
                else:       
                    print 'Failed!' 
                    continue
                pass 
            return False
        
        
    #---------------------------------------------------------    
    def solve(self, max_steps=100, max_backtracking=3):
        success = True
        step = 0
        while success and step < max_steps:
            if self.cur_entropy == 0.0:
                break
            success = self._perform_single_step(max_backtracking)
            
        if success:
            print "Success!"
        else:
            print "Fail!"
    
def main():
    c = Cube()
    randomize(c, 3)
    print c
    solver = EntropicSolver(c, BasicEntropyEstimator())
    solver.solve()
    print c

if __name__ == '__main__':
    main()