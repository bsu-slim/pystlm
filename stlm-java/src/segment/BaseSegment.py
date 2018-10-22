#!/usr/bin/env python
""" generated source for module BaseSegment """
# package: segment
class BaseSegment(InternalSegment):
    """ generated source for class BaseSegment """
    root = Segment()

    @overloaded
    def __init__(self):
        """ generated source for method __init__ """
        super(BaseSegment, self).__init__()

    @__init__.register(object, RootSegment)
    def __init___0(self, root):
        """ generated source for method __init___0 """
        super(BaseSegment, self).__init__(-2)
        self.root = root

    def findBranch(self, word):
        """ generated source for method findBranch """
        return self.root

