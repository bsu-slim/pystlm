#!/usr/bin/env python
""" generated source for module Segment """
# package: segment
class Segment(object):
    """ generated source for class Segment """
    # 
    # 	 * Segments make up the tree. There is a base segment, then a root segment, then the tree expands into internal segments, until it gets to leaf segments. 
    # 	 * These segment types make it easier to traverse the tree during building and during evaluation
    # 	 
    left = int()
    right = int()
    link = Segment()

    @overloaded
    def __init__(self):
        """ generated source for method __init__ """
        self.left = 0

    @__init__.register(object, int)
    def __init___0(self, l):
        """ generated source for method __init___0 """
        self.left = l

    def setLink(self, link):
        """ generated source for method setLink """
        self.link = link

    def getLink(self):
        """ generated source for method getLink """
        return self.link

    def getLeft(self):
        """ generated source for method getLeft """
        return self.left

    def getRight(self):
        """ generated source for method getRight """
        return -1

    def put(self, branch, w):
        """ generated source for method put """
        return None

    def findIndex(self, word):
        """ generated source for method findIndex """
        return 0

    def findBranch(self, ind):
        """ generated source for method findBranch """
        return None

    @overloaded
    def setCount(self, d):
        """ generated source for method setCount """

    @setCount.register(object)
    def setCount_0(self):
        """ generated source for method setCount_0 """

    def getCount(self):
        """ generated source for method getCount """
        return 0.0

    def span(self):
        """ generated source for method span """
        return self.getRight() - self.getLeft()

    @overloaded
    def increment(self):
        """ generated source for method increment """

    @increment.register(object, float)
    def increment_0(self, d):
        """ generated source for method increment_0 """

    def numChildren(self):
        """ generated source for method numChildren """
        return 0

