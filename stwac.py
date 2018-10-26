'''
Created on Oct 24, 2018

@author: ckennington
'''


from sequence import Text
from constants import Constants
from stlm import STLM

import numpy as np

class STWAC(STLM):
   
    def __init__(self, trie):
        super(STWAC, self).__init__(trie)
        self.compose = False
        
        
    def prob(self, predictions,word, X):
        word = self.trie.get_text().get(word)
        new_predictions = self.get_prob(predictions, word, X)
        return new_predictions
        
    def get_compose(self):
        return self.compose
        
    def ground(self, predictions, child, X):
        

        p_word = self.trie.text.get_word_from_index(self.trie.text.at(self.current.get_left()))
        
        if self.offset.size() > 0:
            c_word = self.trie.text.get_word_from_index(self.trie.at(self.current.get_left())+self.offset.size())
        else:
            if child is None: return None # some of the time, there might not be a child node
            c_word = self.trie.text.get_word_from_index(self.trie.text.at(child.get_left()))
            
        if predictions is None:
            parent_target = c_word
        else:
            X = np.concatenate([predictions.reshape(-1,1), X],axis=1)
            parent_target = u'{}-{}'.format(p_word, c_word)
        
        if parent_target not in self.trie.wac: return None

        preds = self.trie.wac[parent_target].predict_proba(X)[:,1]
        
        return preds
        
        
    def get_prob(self, predictions, word, X):
        if self.offset.size() > 0:
            arc = self.current
            if arc.get_left() + self.offset.size() > arc.get_right():
                self.current = self.find_prefix_arc(self.offset.at(0))
                self.offset.clear()
                
        self.compose = False
        if self.word_is_here(word):
            if self.offset.size() == 0:
                child = self.find_prefix_arc(word)
                # usual case: word is found where we expect
                prob = self.ground(predictions, child, X)
                if child.span() > 1: self.offset.push_back(word)
                else: self.current = child
            else: 
                prob = self.ground(predictions, None, X)
                self.offset.push_back(word)
        else: # here is where we backoff
            if self.current.get_left() > -1:
                if self.offset.size() > 0:
                    self.offset.clear()
                self.current = self.current.get_link()
                prob = self.get_prob(predictions, word, X)
            else:
                if self.offset.size() > 0:
                    self.offset.cut()
                    prob = self.get_prob(predictions, word, X)
                else:
                    self.compose = True
                    prob = self.ground(None, None, X) # at this point, we've followed backoff to the root, which means no predcessor predictions
            
        return prob