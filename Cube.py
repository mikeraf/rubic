# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 20:38:26 2014

@author: michar
"""
import string
import itertools                

__all__ = ['Face','Cube']


class Face(object):
    N = 0
    E = 1
    S = 2
    W = 3
    #---------------------------------------------------------------
    def __init__(self, val):
        if type(val) is int:
            row = [val, val, val]
            self.vals = [row[:], row[:], row[:]]
        elif type(val) is list and len(val) == 9 and type(val[1]) is int:
            self.vals = [val[0:3], val[3:6], val[6:9]]
        else:
            raise TypeError('val should be either int or list of ints with length 9')                
        self.neighbors = [None for i in range(4)] # N,E,S,W
        pass
    #---------------------------------------------------------------  
    def get_vals(self):
        '''return a flat list of faces values'''
        return list(itertools.chain.from_iterable(self.vals))
    #---------------------------------------------------------------
    def copy(self):
        return Face(self.get_vals())
    #---------------------------------------------------------------    
    def set_neighbors(self, neighbors, sides):
        ''' neighbors is a list of Face objects on N,E,S,W orientations
        respectively.
        sides is the location of self relative to neighbor
        '''
        self.neighbors = [(n,o) for n,o in zip(neighbors,sides)]
        pass
    #---------------------------------------------------------------    
    def get_neighbor_edge_vals(self, side):
        '''
        get the values on the edge on the given side assuming clockwise 
        direction.
>>> f =  Face(range(9)) 
>>> print f.vals
[[0, 1, 2], [3, 4, 5], [6, 7, 8]]
>>> f.set_neighbors([f for d in range(4)], [f.S, f.W, f.N, f.E])
>>> f.get_neighbor_edge_vals(f.N)
[6, 7, 8]
>>> f.get_neighbor_edge_vals(f.E)
[0, 3, 6]
>>> f.get_neighbor_edge_vals(f.S)
[2, 1, 0]
>>> f.get_neighbor_edge_vals(f.W)
[8, 5, 2]
        '''
        if self.neighbors[side] is None:
            return None
        (neighbor, nside) = self.neighbors[side]
        if nside == self.N:
            return neighbor.vals[0][::-1]
        elif nside == self.E:
            return [neighbor.vals[i][-1] for i in reversed(range(3))]
        elif nside == self.S:
            return neighbor.vals[-1][:]
        elif nside == self.W:
            return [neighbor.vals[i][0] for i in range(3)]
    #---------------------------------------------------------------
    def set_neighbor_edge_vals(self, side, vals):
        '''
    get the values on the edge on the given side assuming clockwise 
    direction.
        >>> f =  Face(range(9)) 
        >>> f.set_neighbors([f.copy() for d in range(4)], [f.S, f.W, f.N, f.E])
        >>> n = f.get_neighbor_edge_vals(f.N)
        >>> f.set_neighbor_edge_vals(f.N,[2*i for i in n])
        >>> f.get_neighbor_edge_vals(f.N)
        [12, 14, 16]
        >>> e = f.get_neighbor_edge_vals(f.E)
        >>> f.set_neighbor_edge_vals(f.E,[2*i for i in e])
        >>> f.get_neighbor_edge_vals(f.E)
        [0, 6, 12]
        >>> s = f.get_neighbor_edge_vals(f.S)
        >>> f.set_neighbor_edge_vals(f.S,[2*i for i in s])
        >>> f.get_neighbor_edge_vals(f.S)
        [4, 2, 0]
        >>> w = f.get_neighbor_edge_vals(f.W)
        >>> f.set_neighbor_edge_vals(f.W,[2*i for i in w])
        >>> f.get_neighbor_edge_vals(f.W)
        [16, 10, 4]
        '''        
        assert(len(vals) == 3)
        if self.neighbors[side] is None:
            return
        (neighbor, nside) = self.neighbors[side]
        if nside == self.N:
            for i,j in zip(reversed(range(3)),range(3)):
                neighbor.vals[0][i] = vals[j]
        elif nside == self.E:
            for i,j in zip(reversed(range(3)),range(3)):
                neighbor.vals[i][-1] = vals[j]
        elif nside == self.S:
            neighbor.vals[-1][:] = vals
        elif nside == self.W:
            for i in range(3):
                neighbor.vals[i][0] = vals[i]
        
    #---------------------------------------------------------------        
    def __str__(self):
        '''
>>> f = Face(1)
>>> print str(f) # doctest: +NORMALIZE_WHITESPACE
_____________
|   |   |   |
| 1 | 1 | 1 |
|___|___|___|
|   |   |   |
| 1 | 1 | 1 |
|___|___|___|
|   |   |   |
| 1 | 1 | 1 |
|___|___|___|      
        '''
        ret = ''
        ret += self._get_up_separator()
        for r in range(3):            
            ret += self._get_row_str(r)
            ret += self._get_down_separator()
        return ret[:-1]
    
    def _get_up_separator(self):
        return 13*'_' + '\n'
    def _get_down_separator(self):
        return 3*'|___' + '|\n'
    def _get_row_str(self, row):
        return 3*'|   ' + '|\n' + '| %d | %d | %d |'%tuple(self.vals[row][:]) + '\n'
    pass

###########################################################################
class Cube(object):
    #--------------------------------------------------------------- 
    def __init__(self):
        faces = []
        for i in xrange(6):
            faces.append(Face(i))
        (N,E,S,W) = (Face.N, Face.E, Face.S, Face.W)
        # set face neighbors  data
        faces[0].set_neighbors([faces[3],faces[1],faces[2],faces[4]],
                               [W, W, W, E])
        faces[1].set_neighbors([faces[3],faces[5],faces[2],faces[0]],
                               [S, W, N, E])
        faces[2].set_neighbors([faces[1],faces[5],faces[4],faces[0]],
                               [S, S, S, S])
        faces[3].set_neighbors([faces[4],faces[5],faces[1],faces[0]],
                               [N, N, N, N])
        faces[4].set_neighbors([faces[3],faces[0],faces[2],faces[5]],
                               [E, W, W, W])
        faces[5].set_neighbors([faces[3],faces[4],faces[2],faces[1]],
                               [E, W, E, W])
        self.faces = faces
                                    
        pass
    #--------------------------------------------------------------- 
    def __str__(self):        
        '''
>>> c = Cube()
>>> print str(c) # doctest: +NORMALIZE_WHITESPACE
             _____________                          
             |   |   |   |                          
             | 3 | 3 | 3 |                          
             |___|___|___|                          
             |   |   |   |                          
             | 3 | 3 | 3 |                          
             |___|___|___|                          
             |   |   |   |                          
             | 3 | 3 | 3 |                          
             |___|___|___|                          
____________________________________________________
|   |   |   ||   |   |   ||   |   |   ||   |   |   |
| 0 | 0 | 0 || 1 | 1 | 1 || 5 | 5 | 5 || 4 | 4 | 4 |
|___|___|___||___|___|___||___|___|___||___|___|___|
|   |   |   ||   |   |   ||   |   |   ||   |   |   |
| 0 | 0 | 0 || 1 | 1 | 1 || 5 | 5 | 5 || 4 | 4 | 4 |
|___|___|___||___|___|___||___|___|___||___|___|___|
|   |   |   ||   |   |   ||   |   |   ||   |   |   |
| 0 | 0 | 0 || 1 | 1 | 1 || 5 | 5 | 5 || 4 | 4 | 4 |
|___|___|___||___|___|___||___|___|___||___|___|___|
             _____________                          
             |   |   |   |                          
             | 2 | 2 | 2 |                          
             |___|___|___|                          
             |   |   |   |                          
             | 2 | 2 | 2 |                          
             |___|___|___|                          
             |   |   |   |                          
             | 2 | 2 | 2 |                          
             |___|___|___| 
             
        '''
        # prepare faces string representations
        faces_strs = []
        for i in range(6):
            faces_strs.append(str(self.faces[i]))
        # calculate empty line length
        empty_line = string.find(faces_strs[0],'\n')*' '
        # join faces along \n's
        ret = ''
        for line in faces_strs[3].split('\n'):
            ret += empty_line + line + 2*empty_line+'\n'
        for a,b,c,d in zip(faces_strs[0].split('\n'),faces_strs[1].split('\n'),
                       faces_strs[5].split('\n'),faces_strs[4].split('\n')):
                           ret += a + b + c + d + '\n'
        
        for line in faces_strs[2].split('\n'):
            ret += empty_line + line + 2*empty_line+'\n'
        
        return ret
    #---------------------------------------------------------------    
    def rotate(self, face_ind, nquarters):
        '''Rotate face with index :face_ind: by :nquarters: quarter spins.
       positive :nquarters: is clockwise while negative is counter-clockwise.
       Note that :nquarters: are equal modulo 4.
       
>>> c1 = Cube()
>>> c1.rotate(1,1)
>>> print str(c1) # doctest: +NORMALIZE_WHITESPACE
             _____________                          
             |   |   |   |                          
             | 3 | 3 | 3 |                          
             |___|___|___|                          
             |   |   |   |                          
             | 3 | 3 | 3 |                          
             |___|___|___|                          
             |   |   |   |                          
             | 0 | 0 | 0 |                          
             |___|___|___|                          
____________________________________________________
|   |   |   ||   |   |   ||   |   |   ||   |   |   |
| 0 | 0 | 2 || 1 | 1 | 1 || 3 | 5 | 5 || 4 | 4 | 4 |
|___|___|___||___|___|___||___|___|___||___|___|___|
|   |   |   ||   |   |   ||   |   |   ||   |   |   |
| 0 | 0 | 2 || 1 | 1 | 1 || 3 | 5 | 5 || 4 | 4 | 4 |
|___|___|___||___|___|___||___|___|___||___|___|___|
|   |   |   ||   |   |   ||   |   |   ||   |   |   |
| 0 | 0 | 2 || 1 | 1 | 1 || 3 | 5 | 5 || 4 | 4 | 4 |
|___|___|___||___|___|___||___|___|___||___|___|___|
             _____________                          
             |   |   |   |                          
             | 5 | 5 | 5 |                          
             |___|___|___|                          
             |   |   |   |                          
             | 2 | 2 | 2 |                          
             |___|___|___|                          
             |   |   |   |                          
             | 2 | 2 | 2 |                          
             |___|___|___|        

>>> c2 = Cube()
>>> c2.rotate(1,2)
>>> print str(c2)  # doctest: +NORMALIZE_WHITESPACE
             _____________                          
             |   |   |   |                          
             | 3 | 3 | 3 |                          
             |___|___|___|                          
             |   |   |   |                          
             | 3 | 3 | 3 |                          
             |___|___|___|                          
             |   |   |   |                          
             | 2 | 2 | 2 |                          
             |___|___|___|                          
____________________________________________________
|   |   |   ||   |   |   ||   |   |   ||   |   |   |
| 0 | 0 | 5 || 1 | 1 | 1 || 0 | 5 | 5 || 4 | 4 | 4 |
|___|___|___||___|___|___||___|___|___||___|___|___|
|   |   |   ||   |   |   ||   |   |   ||   |   |   |
| 0 | 0 | 5 || 1 | 1 | 1 || 0 | 5 | 5 || 4 | 4 | 4 |
|___|___|___||___|___|___||___|___|___||___|___|___|
|   |   |   ||   |   |   ||   |   |   ||   |   |   |
| 0 | 0 | 5 || 1 | 1 | 1 || 0 | 5 | 5 || 4 | 4 | 4 |
|___|___|___||___|___|___||___|___|___||___|___|___|
             _____________                          
             |   |   |   |                          
             | 3 | 3 | 3 |                          
             |___|___|___|                          
             |   |   |   |                          
             | 2 | 2 | 2 |                          
             |___|___|___|                          
             |   |   |   |                          
             | 2 | 2 | 2 |                          
             |___|___|___| 
             
>>> c3 = Cube()
>>> c3.rotate(1,-2)
>>> str(c3) == str(c2)
True
>>> c3.rotate(1,-1)
>>> str(c3) == str(c1)
True

        '''
        def rotate(l, n):
            if n==0:
                return l
            n = -n % len(l)            
            return l[n:] + l[:n]
        
        neighbor_edges = []
        face = self.faces[face_ind]
        # get all neighbor edges
        for i in range(4):
            edge = face.get_neighbor_edge_vals(i)
            neighbor_edges.append(edge)
        
        # rotate the edges according to nquarters
        neighbor_edges = rotate(neighbor_edges, nquarters)
        
        # set back the edges
        for i in range(4):
            face.set_neighbor_edge_vals(i, neighbor_edges[i])
        pass
    #--------------------------------------------------------------- 
    def get_face(self, n):
        return self.faces[n]
    #---------------------------------------------------------------    
    def get_current_tuple_representation(self):
        ''' 
        >>> c=Cube()
        >>> c.get_current_tuple_representation()
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5)
        
        '''
        vals = []
        for f in self.faces:
            vals.extend(f.get_vals())
        return tuple(vals)
        
###############################################        
if __name__ == '__main__':
    import doctest
    doctest.testmod()

        