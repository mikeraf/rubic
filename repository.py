from Cube import *
from Configurator import *
from itertools import product
import cPickle

repo_filename = 'repo.dat'

def get_repo(filename):
    try:
        f = open(filename, 'r')
    except:
        return create_repo(filename)
    
    return cPickle.load(f)

def create_repo(filename, depth=4):
    repository = {}
    depth = 5;
    basic_moves = []
    for f in xrange(6): 
        for n in xrange(1,4):
            basic_moves.append((f,n))
    for i,moves in enumerate(product(basic_moves, repeat=depth)):
        c = Cube()
        for move in moves:
            c.rotate(*move)
        t = c.get_current_tuple_representation()
        repository.setdefault(t, moves)
        print i
    
    f = open('repo.dat', 'w')
    cPickle.dump(repository, f)
    f.close()
    return repository