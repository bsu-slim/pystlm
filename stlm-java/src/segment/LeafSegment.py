#!/usr/bin/env python
""" generated source for module LeafSegment """
# package: segment
import sequence.Text

class LeafSegment(Segment):
    """ generated source for class LeafSegment """
    text = Text()

    @overloaded
    def __init__(self):
        """ generated source for method __init__ """
        super(LeafSegment, self).__init__()

    @__init__.register(object, Text, int)
    def __init___0(self, t, l):
        """ generated source for method __init___0 """
        super(LeafSegment, self).__init__(l)
        self.text = t

    def getRight(self):
        """ generated source for method getRight """
        return len(self.text)

    def numChildren(self):
        """ generated source for method numChildren """
        return 0

    def findIndex(self, word):
        """ generated source for method findIndex """
        return -2

    def getCount(self):
        """ generated source for method getCount """
        return 1.0

    def findBranch(self, word):
        """ generated source for method findBranch """
        return None

