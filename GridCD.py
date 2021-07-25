# coding=utf-8

###########################
# file: GridCD.py
# date: 2021-7-25
# author: Sturmfy
# desc: Basic definition of Grid-based collision detection
# version:
#   2021-7-25 init design
###########################

import Grid
import Event
import Geometry

class GridCD(object):
    def __init__(self, cols, rows):
        super(GridCD, self).__init__()
        self.cols = cols 
        self.rows = rows
        self.static_grid = Grid.Grid(cols, rows)
        self.dyna_grid = Grid.Grid(cols, rows)
        self.static_geo = set()     # type: set[Geometry.Shape.Shape]
        self.dyna_geo = set()       # type: set[Geometry.Shape.Shape]
        self.trigger_geo = set()    # type: set[Geometry.Shape.Shape]
    
    def Register(self, geo):
        # type: (Geometry.Shape.Shape)->None
        if geo.is_static:
            self.static_geo.add(geo)
            geo.PaintOnGrid(self.static_grid, self.dyna_grid)
        else:
            self.dyna_geo.add(geo)
        if geo.is_trigger:
            self.trigger_geo.add(geo)
    
    def Remove(self, geo):
        # type: (Geometry.Shape.Shape)->None
        if geo.is_static:
            self.static_geo.discard(geo)
            geo.UnpaintOnGrid(self.static_grid)
        else:
            self.dyna_geo.discard(geo)
        if geo.is_trigger:
            self.trigger_geo.discard(geo)
    
    def Tick(self):
        self.dyna_grid.Clear()
        # 1. paint all dyna objects
        event_list = []
        for geo in self.dyna_geo:
            conflicts = geo.PaintOnGrid(self.static_grid, self.dyna_grid)
            if conflicts is None or len(conflicts) == 0:
                continue
            for con in conflicts:
                e = Event.CollisionEvent(geo, con)
                if geo.is_trigger:
                    geo.cur_triggered.add(con)
                if con.is_trigger:
                    con.cur_triggered.add(geo)
                event_list.append(e)
        
        # 2. process trigger out event
        for geo in self.trigger_geo:
            geo.last_triggered.difference_update(geo.cur_triggered)
            for og in geo.last_triggered:
                geo.gameObject.OnTriggerOut(og)
                og.gameObject.OnTriggerOut(geo)
            geo.last_triggered = geo.cur_triggered
            geo.cur_triggered = set()

        # 3. process trigger in & collision
        for e in event_list:
            if e.geo_a.gameObject.need_destroy or e.geo_b.gameObject.need_destroy:
                continue
            if e.geo_a.is_trigger or e.geo_b.is_trigger:
                e.geo_a.gameObject.OnTriggerIn(e)
                e.geo_b.gameObject.OnTriggerIn(e)
            else:
                e.geo_a.gameObject.OnCollision(e)
                e.geo_b.gameObject.OnCollision(e)
            


        
