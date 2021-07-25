# coding=utf-8

###########################
# file: Grid.py
# date: 2021-7-25
# author: Sturmfy
# desc: Grid-based collision detection
# version:
#   2021-7-25 init design
###########################

'''


'''

import numpy as np 

class Grid(object):
    def __init__(self, x, y):
        super(Grid, self).__init__()
        self.__data = [[set() for i in xrange(x)] for j in xrange(y)]
        self.rows = y
        self.cols = x 
    
    def Size(self):
        return (self.cols, self.rows)
    
    def Clear(self):
        for r in self.__data:
            for s in r:
                s.clear()
    
    def Add(self, x, y, tar):
        self.__data[y][x].add(tar)
    
    def Remove(self, x, y, tar):
        self.__data[y][x].remove(tar)
    
    def Get(self, x, y):
        return self.__data[y][x]

    def Print(self):
        d = np.zeros([self.rows, self.cols])
        for y in xrange(self.rows):
            for x in xrange(self.cols):
                d[y,x] = len(self.__data[y][x])
        print d 