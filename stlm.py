'''
Created on Oct 23, 2018

@author: ckennington
'''
from sequence import Text

class STLM:
    
    def __init__(self, trie):
        self.trie = trie
        self.offset = Text() # ??
        self.disc = 0.5
        self.start_new_utterance()
        
    def start_new_utterance(self):
        self.current = self.trie.get_root()
        self.offset.clear()
        self.inc_prob = 0.0
        self.inc_word = 0.0
        self.max_depth_reached = 0.0
    
        
    def prob(self, sent):
        prob = 1.0
        self.start_new_utterance()
        for i in range(sent.size()):
            word = self.trie.get_text().get(sent.at(i))
            p = self.get_prob(word)
            prob *= p
            
        return prob
    
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
                
                
    def find_prefix_arc(self, word):
        pa = self.current.find_branch(word)
        return pa
    
    def word_is_here(self, word):
        
        if self.offset.size() == 0:
            pa = self.find_prefix_arc(word)
            return pa is not None
        else:
            self.branch = self.find_prefix_arc(self.offset.at(0))
            if self.branch.get_left() + self.offset.size() <= self.trie.get_text().size():
                if self.trie.get_text().at(self.branch.get_left() + self.offset.size()) == word:
                    return True
        return False
            