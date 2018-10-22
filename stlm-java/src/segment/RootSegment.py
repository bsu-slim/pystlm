#!/usr/bin/env python
""" generated source for module RootSegment """
# package: segment
import sequence.Text

class RootSegment(InternalSegment):
    """ generated source for class RootSegment """
    text = Text()

    @overloaded
    def __init__(self, text):
        """ generated source for method __init__ """
        super(RootSegment, self).__init__(-1)
        self.text = text

    @__init__.register(object)
    def __init___0(self):
        """ generated source for method __init___0 """
        super(RootSegment, self).__init__()

    def getRight(self):
        """ generated source for method getRight """
        return 0

    def increment(self):
        """ generated source for method increment """

    def getCount(self):
        """ generated source for method getCount """
        return len(self.text)

