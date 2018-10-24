'''
Created on Oct 24, 2018

@author: ckennington
'''

from stlm import STLM
from suffixtree import SuffixTree
from sequence import Sequence

trie = SuffixTree()

class node():
    def __init__(self, s):
        self.s = s
    def __str__(self):
        return 'node({})'.format(self.s)
    def __eq__(self, other):
        return other.s == self.s
    def __hash__(self):
        return hash(self.s)

nodes = [node('c'), node('a'), node('c'), node('a'), node('o')]

for w in nodes:
    print('adding', w)
    trie.add(w)
    
print('\n')
trie.print_tree()
print('\n')
    
trie.update_all_counts()

stlm = STLM(trie)

tests = [[node('c'),node('a')]]

for test in tests:
    seq = Sequence()
    for t in test: seq.push_back(t)
    print(stlm.prob(seq))
