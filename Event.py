# coding=utf-8

###########################
# file: Event.py
# date: 2021-7-25
# author: Sturmfy
# desc: Basic definition of Collision Event
# version:
#   2021-7-25 init design
###########################

import Geometry
import GameObject

class CollisionEvent(object):
    def __init__(self, g0, g1):
        # type: (Geometry.Shape.Shape, Geometry.Shape.Shape)->None
        super(CollisionEvent, self).__init__()
        self.geo_a = g0   #
        self.geo_b = g1 
    
    def another(self, gameObject):
        # type: (GameObject.GameObject)->None
        if gameObject.geometry is self.geo_a:
            return self.geo_b
        else:
            return self.geo_a