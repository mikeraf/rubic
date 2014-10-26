# -*- coding: utf-8 -*-
"""
Created on Sun Oct 26 20:38:26 2014

@author: michar
"""
import string

class Face(object):
    def __init__(self, val):
        assert type(val) is int
        row = [val, val, val]
        self.vals = [row[:], row[:], row[:]]
        pass
    
    def __str__(self):
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


class Cube(object):
    
    def __init__(self):
        self.faces = []
        for i in xrange(6):
            self.faces.append(Face(i))
        pass
    
    def __str__(self):
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
                              
       
       
        
###############################################        
if __name__ == '__main__':
    f = Face(1)
    print str(f)
    print 30*'='+'\n'
    c = Cube()
    print str(c)
        