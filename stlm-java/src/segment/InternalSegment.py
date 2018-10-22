#!/usr/bin/env python
""" generated source for module InternalSegment """
# package: segment
import java.util.HashMap

class InternalSegment(Segment):
    """ generated source for class InternalSegment """
    count = float()
    children = HashMap()

    @overloaded
    def __init__(self):
        """ generated source for method __init__ """
        super(InternalSegment, self).__init__()
        self.children = HashMap()
        setCount(0.0)

    @__init__.register(object, int)
    def __init___0(self, l):
        """ generated source for method __init___0 """
        super(InternalSegment, self).__init__(l)
        self.children = HashMap()
        setCount(0.0)

    def findBranch(self, w):
        """ generated source for method findBranch """
        if self.children.isEmpty():
            return None
        i = findIndex(w)
        if i == -2:
            return None
        return self.children.get(i)

    def findIndex(self, i):
        """ generated source for method findIndex """
        if self.children.containsKey(i):
            return i
        return -2

    def getRight(self):
        """ generated source for method getRight """
        return self.children.get(right).getLeft()

    @overloaded
    def setCount(self):
        """ generated source for method setCount """
        self.setCount(0.0)
        for s in children.keySet():
            increment(self.children.get(s).getCount())

    def getCount(self):
        """ generated source for method getCount """
        return self.count

    @setCount.register(object, float)
    def setCount_0(self, d):
        """ generated source for method setCount_0 """
        self.count = d

    @overloaded
    def increment(self, d):
        """ generated source for method increment """
        self.count += d

    @increment.register(object)
    def increment_0(self):
        """ generated source for method increment_0 """
        self.count += 1

    def numChildren(self):
        """ generated source for method numChildren """
        return len(self.children)

    def put(self, branch, w):
        """ generated source for method put """
        i = self.findIndex(w)
        if i == -2:
            if self.children.isEmpty():
                right = w
            self.children.put(w, branch)
            return None
        else:
            self.children.put(w, branch)
            return old

