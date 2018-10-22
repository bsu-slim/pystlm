#!/usr/bin/env python
""" generated source for module Sequence """
# package: sequence
import model.Constants

class Sequence(Queue, str):
    """ generated source for class Sequence """
    numPads = int()

    def __init__(self):
        """ generated source for method __init__ """
        super(Sequence, self).__init__()

    # 
    #      * Sequences sometimes need <s> and </s> "padding" the params are set in Constants
    #      
    def pad(self):
        """ generated source for method pad """
        max = Constants.NUM_PAD
        self.numPads = max
        i = 0
        while i < max:
            pushFront(Constants.START)
            pushBack(Constants.STOP)
            self.numPads += 1
            i += 1
        self.numPads *= 2

    def padBack(self):
        """ generated source for method padBack """
        max = Constants.NUM_PAD
        self.numPads = max
        i = 0
        while i < max:
            pushBack(Constants.STOP)
            i += 1

