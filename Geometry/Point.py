# coding=utf-8

###########################
# file: Rect.py
# date: 2021-7-25
# author: Sturmfy
# desc: Basic definition of Round things
# version:
#   2021-7-25 init design
###########################

import sys 
sys.path.append("..")

from .Shape import Shape
from Grid import Grid
import numpy as np

class Point(Shape):
    def __init__(self):
        super(Point, self).__init__()
        self.is_trigger = True 
    
    def PaintOnGrid(self, static_grid, dyna_grid):
        # type: (Grid, Grid)->set 
        c_pos = self.gameObject.tranform.position
        grid_size = static_grid.Size()
        if c_pos[0] < 0 or c_pos[1] < 0:
            return None 
        if c_pos[0] >= grid_size[0] or c_pos[1] >= grid_size[1]:
            return None 
        x = int(c_pos[0])
        y = int(c_pos[1])

        if self.is_static:
            static_grid.Add(x, y, self)
            return None 
        res = set()
        res.update(static_grid.Get(x, y))
        res.update(dyna_grid.Get(x, y))
        dyna_grid.Add(x, y, self)
        return res 
    
    def TestCollision(self, otherShape):
        # type: (Shape, bool)->bool
        # do not care about the needRollback
        c_pos = self.gameObject.tranform.position
        return otherShape.IsPointIn(c_pos[0], c_pos[1])

        
