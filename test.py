
import sys 
sys.path.append("..")

import GameObject
import Geometry
import Grid
import Transform
import math 
import random

def main():
    sg = Grid.Grid(10, 10)
    dg = Grid.Grid(10, 10)
    
    gl = [GameObject.GameObject() for i in xrange(5)]
    for i in gl:
        i.tranform = Transform.Transform(i)
    gl[0].geometry = Geometry.Point()
    gl[1].geometry = Geometry.Circle(2)
    gl[2].geometry = Geometry.Sector(3, (0,1), math.pi/2)
    gl[3].geometry = Geometry.MapCube()
    gl[4].geometry = Geometry.MapCube()
    for i in gl:
        i.geometry.gameObject = i 
    for i in gl:
        i.tranform.translate(random.uniform(0, 9), random.uniform(0, 9))
    for i in gl:
        i.geometry.PaintOnGrid(sg, dg)

    print "Dynamic"
    dg.Print()
    print "Static"
    sg.Print()
    return 


if __name__ == "__main__":
    main()