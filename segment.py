'''
Created on Oct 22, 2018

@author: casey
'''
class Segment(object):
    # 
    #      * Segments make up the tree. There is a base segment, then a root segment, then the tree expands into internal segments, until it gets to leaf segments. 
    #      * These segment types make it easier to traverse the tree during building and during evaluation
    #      
    
    def __init__(self, l=0):
        self.left = l
        self.right = -1
        self.link = Segment()

    @__init__.register(object, int)
    def __init___0(self, l):
        self.left = l

    def set_link(self, link):
        self.link = link

    def get_link(self):
        return self.link

    def get_left(self):
        return self.left

    def get_right(self):
        return -1

    def put(self, branch, w):
        return None

    def find_index(self, word):
        return 0

    def find_branch(self, ind):
        return None

    def set_count(self, d):
        pass

    def get_count(self):
        return 0.0

    def span(self):
        return self.get_right() - self.get_left()

    def increment(self):
        pass

    def num_children(self):
        return 0
    


class InternalSegment(Segment):
    
    def __init__(self, l):
        super(InternalSegment, self).__init__(l)
        self.children = dict()
        self.setCount(0.0)

    def findBranch(self, w):
        if len(self.children) == 0:
            return None
        i = self.find_index(w)
        if i == -2:
            return None
        return self.children[i]

    def find_index(self, i):
        if i in self.children:
            return i
        return -2

    def get_right(self):
        return self.children[self.right].get_left()

    def setCount(self):
        self.set_count(0.0)
        for s in self.children.keys():
            self.increment(self.children[s].getCount())

    def get_count(self):
        return self.count

    def set_count(self, d):
        self.count = d

    def increment(self, d):
        self.count += d

    def num_children(self):
        return len(self.children)

    def put(self, branch, w):
        i = self.find_index(w)
        if i == -2:
            if len(self.children) == 0:
                self.right = w
            self.children[w] = branch
            return None
        else:
            old = self.children[w]
            self.children.put[w] = branch
            return old


class RootSegment(InternalSegment):

    def __init__(self, text):
        super(RootSegment, self).__init__(-1)
        self.text = text


    def get_right(self):
        return 0

    def increment(self):
        pass

    def get_count(self):
        return len(self.text)
    

class BaseSegment(InternalSegment):

    def __init__(self, root):
        super(BaseSegment, self).__init__(-2)
        self.root = root

    def find_branch(self, word):
        return self.root
    
    
class LeafSegment(Segment):
    def __init__(self, text, l):
        super(LeafSegment, self).__init__(l)
        self.text = text

    def get_right(self):
        return len(self.text)

    def num_children(self):
        return 0

    def find_index(self, word):
        return -2

    def get_count(self):
        return 1.0

    def find_branch(self, word):
        return None





