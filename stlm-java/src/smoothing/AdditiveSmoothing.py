#!/usr/bin/env python
""" generated source for module AdditiveSmoothing """
# package: smoothing
import segment.Segment

import suffixtree.SuffixTree

class AdditiveSmoothing(Smoothing, T):
    """ generated source for class AdditiveSmoothing """
    disc = 1.0

    def __init__(self, t):
        """ generated source for method __init__ """
        super(AdditiveSmoothing, self).__init__(t)

    def wordHereMultChild(self, parent, child):
        """ generated source for method wordHereMultChild """
        prob = (self.disc + child.getCount()) / (parent.numChildren() * self.disc + parent.getCount())
        return prob

    def updateUnk(self):
        """ generated source for method updateUnk """
        unk = self.disc / (current.numChildren() * self.disc + current.getCount())

