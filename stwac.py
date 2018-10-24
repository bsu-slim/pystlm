'''
Created on Oct 24, 2018

@author: ckennington
'''
from sequence import Text
from constants import Constants
from stlm import STLM

class STWAC(STLM):
   
    def __init__(self, trie):
        super(STWAC, self).__init__(trie)
        
        
    def get_prob(self, word):
        prob = 0.0
        if self.offset.size() > 0:
            arc = self.current
            if arc.get_left() + self.offset.size() > arc.get_right():
                self.current = self.find_prefix_arc(self.offset.at(0))
                self.offset.clear()
                
        if self.word_is_here(word):
            if self.offset.size() == 0:
                child = self.find_prefix_arc(word)
                prob = (self.disc + child.get_count()) / (self.current.num_children() * self.disc + self.current.get_count())
                if child.span() > 1: self.offset.push_back(word)
                else: self.current = child
            else: 
                count = self.current.get_count()
                prob = (count - self.disc) / count # only one child, so it carries all of the mass, minus discount
                self.offset.push_back(word)
        else: # here is where we backoff
            if self.current.get_left() > -1:
                if self.offset.size() > 0:
                    self.offset.clear()
                self.current = self.current.get_link()
                prob = self.get_prob(word)
            else:
                if self.offset.size() > 0:
                    self.offset.cut()
                    prob = self.get_prob(word)
                else:
                    prob = self.disc / (self.current.num_children() * self.disc + self.current.get_count())
            
        return prob