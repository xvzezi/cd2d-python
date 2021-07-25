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
import Point 
import Rect 
import numpy as np
import math 

class Circle(Shape):
    def __init__(self, r):
        super(Circle, self).__init__()
        self.SetRadius(r)
    
    def SetRadius(self, r):
        self.radius = r 
        self.diameter = r * 2

    
    def GetRadius(self):
        return self.radius 

    def BoundingRadius(self):
        return self.radius
    
    def IsPointIn(self, x, y):
        c_pos = self.gameObject.tranform.position
        xx = x - c_pos[0]
        yy = y - c_pos[1]
        return xx**2 + yy**2 < self.radius**2
    
    def PaintOnGrid(self, static_grid, dyna_grid):
        # type: (Grid, Grid)->set
        # 1. find all the index to paint
        c_pos = self.gameObject.tranform.position + self.center
        min_pos = (int(c_pos[0] - self.radius), int(c_pos[1] - self.radius))
        max_pos = (int(c_pos[0] + self.radius)+1, int(c_pos[1] + self.radius)+1)
        grid_size = static_grid.Size()
        min_pos = (max(min_pos[0], 0), max(min_pos[1], 0))
        max_pos = (
            min(max_pos[0], grid_size[0] - 1), 
            min(max_pos[1], grid_size[1] - 1)
        )
        print min_pos
        print max_pos
        
        # 2. if static, add to the grid and has no return
        if self.is_static:
            for y in xrange(min_pos[1], max_pos[1]):
                for x in xrange(min_pos[0], max_pos[0]):
                    static_grid.Add(x, y, self)
            return None 
        
        # 3. not static 
        res = set()
        for y in xrange(min_pos[1], max_pos[1]):
            for x in xrange(min_pos[0], max_pos[0]):
                res.update(static_grid.Get(x, y))
                res.update(dyna_grid.Get(x, y))
                dyna_grid.Add(x, y, self)

        return res 
    
    def TestCollision(self, otherShape):
        if isinstance(otherShape, Point.Point):
            return otherShape.TestCollision(self)
        
        result = False
        c_pos = self.gameObject.tranform.position
        oc_pos = otherShape.gameObject.tranform.position
        dv = oc_pos - c_pos
        d = np.linalg.norm(dv)
        dv = dv / d
        dv = dv * self.radius
        test_point = c_pos + dv 
        if isinstance(otherShape, Rect.MapCube):
            corners = otherShape.GetWorldCorners()
            for c in corners:
                if self.IsPointIn(c[0], c[1]):
                    result = True
                    break
        elif isinstance(otherShape, Circle):
            result = d < self.radius + otherShape.radius
        elif isinstance(otherShape, Sector):
            result = otherShape.IsPointIn(test_point[0], test_point[1]) 

        if result:
            if self.is_trigger or otherShape.is_trigger:
                return result 
            if self.is_static and otherShape.is_static:
                return result
            if not self.is_static and not otherShape.is_static:
                mid_p = (c_pos + oc_pos) / 2
                self.Rollback(mid_p[0], mid_p[1])
                otherShape.Rollback(mid_p[0], mid_p[1])
            staticShape = otherShape 
            dynaShape = self
            if self.is_static:
                staticShape = self 
                dynaShape = otherShape
            st_pos = staticShape.gameObject.tranform.position
            dy_pos = dynaShape.gameObject.tranform.position
            sd_vec = dy_pos - st_pos
            sd_dis = np.linalg.norm(sd_vec)
            sd_vec = sd_vec / sd_dis
            sd_vec = sd_vec * staticShape.BoundingRadius()
            rb_point = st_pos + sd_vec 
            staticShape.Rollback(rb_point[0], rb_point[1])
            
        return result
            
    
    def Rollback(self, x, y):
        # type: (float, float)->bool
        c_pos = self.gameObject.tranform.try_position
        mov_d = c_pos - (x, y)
        mov_d_len = np.linalg.norm(mov_d)
        mov_d = mov_d / mov_d_len
        if mov_d_len > self.radius:
            print "Maybe collision wrong?"
            return 
        rest = self.radius - mov_d_len
        to_mov = mov_d * rest 
        self.gameObject.tranform.try_translate(to_mov[0], to_mov[1])
        
        
class Sector(Shape):
    def __init__(self, r, d, rad):
        super(Sector, self).__init__()
        self.Set(r, d, rad)
    
    def Set(self, r, d, rad):
        # type: (float, tuple(float,float), float)->None
        # 1. set basic info
        self.radius = r 
        self.direction = np.array(d)
        print self.direction
        print np.linalg.norm(self.direction)
        self.direction = self.direction / np.linalg.norm(self.direction)
        print self.direction
        self.radian = rad 
        self.cos_half_rad = math.cos(self.radian / 2)

        # 2. build the paint boolean buffer
        self.__d = self.radius * 2
        self.__d_floor = int(self.__d)
        self.__pbb = np.zeros([self.__d_floor + 1, self.__d_floor + 1])
        for y in xrange(self.__d_floor):
            for x in xrange(self.__d_floor):
                if self.__ispointin_sethelper(x, y):
                    self.__pbb[y,x] = 1
                    if x > 0:
                        self.__pbb[y,x-1] = 1
                    if y > 0:
                        self.__pbb[y-1,x] = 1
                    if x > 0 and y > 0:
                        self.__pbb[y-1,x-1] = 1
        # 3, check the center
        pre_c = (int(self.radius), int(self.radius))
        self.__pbb[pre_c[1], pre_c[0]] = 1
        return 
    
    def __ispointin_sethelper(self, x, y):
        xx = x - self.radius
        yy = y - self.radius
        if xx**2 + yy**2 > self.radius**2:
            # out of the circle
            return False
        
        # 2. calculate the rad
        p2c = np.array([xx, yy])
        p2cl = np.linalg.norm(p2c)
        if p2cl < 0.001:
            return True
        p2c = p2c / p2cl
        cos_a = np.dot(p2c, self.direction)
        return cos_a > self.cos_half_rad

    
    def IsPointIn(self, x, y):
        c_pos = self.gameObject.tranform.position
        xx = x - c_pos[0]
        yy = y - c_pos[1]
        if xx**2 + yy**2 > self.radius**2:
            # out of the circle
            return False
        
        # 2. calculate the rad
        p2c = np.array([xx, yy])
        p2c /= np.linalg.norm(p2c)
        cos_a = np.dot(p2c, self.direction)
        return cos_a > self.cos_half_rad
        
    def BoundingRadius(self):
        return self.radius

    def PaintOnGrid(self, static_grid, dyna_grid):
        # type: (Grid, Grid)->set 
        c_pos = self.gameObject.tranform.position
        s_pos = c_pos - (self.radius, self.radius)
        s_pos = np.array([math.floor(s_pos[0]), math.floor(s_pos[1])])
        grid_size = static_grid.Size()
        i2add = []
        # 1. add center
        for y in xrange(self.__d_floor):
            for x in xrange(self.__d_floor):
                pos = (int(s_pos[0] + x), int(s_pos[1] + y))
                if pos[0] < 0 or pos[1] < 0:
                    continue
                if pos[0] >= grid_size[0] or pos[1] >= grid_size[1]:
                    continue
                if self.__pbb[y,x] != 1:
                    continue
                i2add.append(pos)
        
        # 
        if self.is_static:
            for p in i2add:
                static_grid.Add(p[0], p[1], self)
            return None 
        res = set()
        for p in i2add:
            res.update(static_grid.Get(p[0], p[1]))
            res.update(dyna_grid.Get(p[0], p[1]))
            dyna_grid.Add(p[0], p[1], self)
        return res 

    def TestCollision(self, otherShape, needRollback):
        if isinstance(otherShape, Point.Point):
            return otherShape.TestCollision(self, needRollback)
        elif isinstance(otherShape, Rect.MapCube):
            corners = otherShape.GetWorldCorners()
            for c in corners:
                if self.IsPointIn(c[0], c[1]):
                    return True
            return False
        elif isinstance(otherShape, Circle):
            return otherShape.TestCollision(self, needRollback)
        return False

