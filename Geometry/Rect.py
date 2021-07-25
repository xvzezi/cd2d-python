# coding=utf-8

###########################
# file: Rect.py
# date: 2021-7-25
# author: Sturmfy
# desc: Basic definition of Rect
# version:
#   2021-7-25 init design
###########################

import sys 
sys.path.append("..")

from Grid import Grid
import Shape
import numpy as np
import Point
import Circle

class MapCube(Shape.Shape):
    def __init__(self, slen=1):
        # type: (int,int)->None
        super(MapCube, self).__init__()
        self.SetSize(slen)
        self.is_static = True
    
    def SetSize(self, slen):
        '''
        Clock-wise corners from left-bottom
        '''
        # type: (int, int)->None
        # 1. record init size
        self.side_len = slen
        # 2. record corners
        self.corners = []
        max_x = self.side_len / 2
        min_x = - max_x
        max_y = max_x
        min_y = - max_y
        self.corners.append(np.array([min_x, min_y]))
        self.corners.append(np.array([min_x, max_y]))
        self.corners.append(np.array([max_x, max_y]))
        self.corners.append(np.array([max_x, min_y]))
    
    def GetSize(self):
        return self.side_len
    
    def GetWorldCorners(self):
        res = []
        c_pos = self.gameObject.tranform.position
        for c in self.corners:
            res.append(c + c_pos)
        return res 
    
    def BoundingRadius(self):
        return 1.414 * self.side_len / 2

    def IsPointIn(self, x, y):
        c_pos = self.gameObject.tranform.position
        half_l = self.side_len / 2
        min_x = c_pos[0] - half_l
        max_x = c_pos[0] + half_l
        min_y = c_pos[1] - half_l
        max_y = c_pos[1] + half_l
        return min_x < x and x < max_x and min_y < y and y < max_y 
        

    def PaintOnGrid(self, static_grid, dyna_grid):
        # type: (Grid, Grid)->set
        # only paint, do not return conflicts
        c_pos = self.gameObject.tranform.position + self.center
        static_grid.Add(int(c_pos[0]), int(c_pos[1]), self)
        return None 
    
    def UnpaintOnGrid(self, grid):
        # type: (Grid)->set
        c_pos = self.gameObject.tranform.position + self.center
        grid.Remove(int(c_pos[0]), int(c_pos[1]), self)
        return None 

    def TestCollision(self, otherShape):
        if isinstance(otherShape, MapCube):
            return False
        else:
            return otherShape.TestCollision(self)
    

