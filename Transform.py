# coding=utf-8

###########################
# file: Transform.py
# date: 2021-7-25
# author: Sturmfy
# desc: the transform of the target
# version:
#   2021-7-25 init design
###########################

import numpy as np 
import math 


class Transform(object):
    def __init__(self, gameObject):
        super(Transform, self).__init__()
        self.gameObject = gameObject
        self.position = np.transpose(np.zeros(2))       # use col vector
        self.direction = np.transpose(np.array([1,0]))
        self.scale = np.transpose(np.ones(2))           
        self.rotation = np.identity(2)
        self.__mat = np.identity(3)

        # roll back support
        self.try_moved = False 
        self.try_position = np.transpose(np.zeros(2))

    def local_rotate(self, degree):
        '''
        clock wise 
        '''
        return self.local_rotate_radian(degree / 180 * math.pi)

    def local_rotate_radian(self, radian):
        '''
        clock wise
        '''
        # 1. build the rotation mat
        c = math.cos(radian)
        s = math.sin(radian)
        to_rot = np.array([
            [ c, s],
            [-s, c]
        ])
        self.rotation = to_rot.dot(self.rotation)

    def translate(self, x, y):
        self.position += (x, y)
    
    def move_to(self, x, y):
        self.position = np.transpose(np.array([x,y]))

    def look_to(self, dx, dy):
        self.direction = np.transpose(np.array([dx,dy]))
        l = np.linalg.norm(self.direction)
        if l < 0.01:    # to small
            self.direction = np.transpose(np.array([1,0]))
            return 
        self.direction /= l 

    def to_matrix(self):
        pass 

    ################ Roll Back Mech ##############

    def try_move_to(self, x, y):
        self.try_moved = True
        self.try_position = np.transpose(np.array([x,y]))
    
    def try_translate(self, x, y):
        if self.try_moved:
            self.try_position += (x, y)
        else:
            self.try_moved = True 
            self.try_position = self.position + (x, y)
    
    def apply_try(self):
        self.position = self.try_position
        self.try_moved = False 

    def trying_direction(self):
        if not self.try_moved:
            return None 
        d = self.try_position - self.position
        return d / np.linalg.norm(d)