import numpy as np
from Cube import *
class UniquelyMarkedCube(Cube):
    def __init__(self):
        Cube.__init__(self)
        for f in range(6):
            face = c.get_face(f)
            new_face_vals = [[f*9 + j*3 + 0, f*9 + j*3 + 1, f*9 + j*3 + 2] for j in range(3)]
            face.vals = new_face_vals
            pass        
class CubeMatrixRepresentation(object):
    def __init__(self):
        self._matrix = eye(54)
        self._create_rotation_matrices()
    
    def _create_rotation_matrices(self):
        '''precompute all 18 possible rotation matrices.
        The task will be done by building normal Cube for which
        every single square has unique id, then we will iterate
        through all rotations and check the effect on this cube.
        By querying the state of the cube after each rotation we
        wil construct the matrices.        
        '''
        umc = UniquelyMarkedCube()
        self._matrices
        for f in range(6):
            for nq in range(1,4):
                umc.rotate(f, nq)
                
    def rotate(self, face_ind, nquarters):
        
        pass
    pass

if __name__ == '__main__':
    from Cube import *
    c = Cube()
    for f in range(6):
        face = c.get_face(f)
        new_face_vals = [[f*9 + j*3 + 0, f*9 + j*3 + 1, f*9 + j*3 + 2] for j in range(3)]
        face.vals = new_face_vals
        pass
    print c