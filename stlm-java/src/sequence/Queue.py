#!/usr/bin/env python
""" generated source for module Queue """
# package: sequence
import java.util.LinkedList

class Queue(object):
    """ generated source for class Queue """
    # 
    # 	 * Wrapper around a linked list 
    # 	 
    items = LinkedList()

    def __init__(self):
        """ generated source for method __init__ """
        self.items = LinkedList()

    def pushFront(self, item):
        """ generated source for method pushFront """
        self.items.addFirst(item)

    def pushBack(self, item):
        """ generated source for method pushBack """
        self.items.add(item)

    def pop(self):
        """ generated source for method pop """
        return self.items.pop()

    def cut(self):
        """ generated source for method cut """
        self.items.removeFirst()

    def size(self):
        """ generated source for method size """
        return len(self.items)

    def clear(self):
        """ generated source for method clear """
        self.items.clear()

    def at(self, i):
        """ generated source for method at """
        return self.items.get(i)

    def isEmpty(self):
        """ generated source for method isEmpty """
        return self.items.isEmpty()

    def __str__(self):
        """ generated source for method toString """
        string = ""
        for item in items:
            string += item.__str__() + " "
        return string.trim()

