'''
Created on Oct 23, 2018

@author: ckennington
'''
from stlm import STLM
from suffixtree import SuffixTree
from sequence import Sequence



trie = SuffixTree()


text = 'c a c a o'.split()

for w in text:
    print('adding', w)
    trie.add(w)
    
print('\n')
trie.print_tree()
print('\n')
    
trie.update_all_counts()

stlm = STLM(trie)

tests = ['c a'.split(), 'c a o'.split(), 'a o'.split(), 'o'.split(), 'c'.split()]


for test in tests:
    seq = Sequence()
    for t in test: seq.push_back(t)
    print(stlm.prob(seq))