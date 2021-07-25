# coding=utf-8

###########################
# file: Shape.py
# date: 2021-7-25
# author: Sturmfy
# desc: Basic definition of shapes
# version:
#   2021-7-25 init design
###########################

'''
    The `Shape` is basic class of every geometry defined. It
provides the basic functions and properties which are 
fundamental for the family of geometry.
    `Shape`s have to work good with Collision Detection 
Modules, so it have to have several members to implement:
    Props:
        - is_trigger:       trigger will not force two game
                            object rolling back when collides
        - is_static:        static object will save time
        - last_triggered:   The objects trigger in the last 
                            round of detection
        - gameObject:       the game object
    Methods:
        - PaintOnGrid(gird, value)->set(Shape)
            return collided object geometry
        - TestCollision(otherShape, needRollback)->(succ)
        - Rollback()


    Overall, we provide 4 simple derived specific 2D 
primitive, they are all aligned to the axis:
1. Rect
    `Rect` is short for rectangle. It defines a polygon with
4 sides and 4 angles. Each of its angles are exactly 90 deg.
or (PI/2) rad. Its center is the origin of this shape.
    Props:
        - Width, Height
        - Center

2. Circle
    `Circle` is Isosymmetrical. That means it has simple 
definition.
    Props:
        - Center, Radius

3. Point
    `Point` is abstraction for mass point.
    Props:
        - Center

4. Sector
    `Sector` is a part of a circle. 
    Props:
        - Center, Radius
        - Direction: the symmetrical line pointed from Center
        - Radian: the radian the Sector expands
'''

import sys 
sys.path.append("..")

import GameObject
from Grid import Grid
import numpy as np

class Shape(object):
    def __init__(self):
        super(Shape, self).__init__()
        self.is_trigger = False 
        self.is_static = False
        self.cur_triggered = set()  # type: set[Shape]
        self.last_triggered = set() # type: set[Shape]
        self.gameObject = None      # type: GameObject.GameObject
        self.center = np.zeros(2)
    
    def BoundingRadius(self):
        return 0

    def IsPointIn(self, x, y):
        return False

    def PaintOnGrid(self, static_grid, dyna_grid):
        # type: (Grid, Grid)->set[Shape]
        pass 

    def UnpaintOnGrid(self, grid):
        return

    def TestCollision(self, otherShape):
        return False

    def Rollback(self, x, y):
        return 
    
    