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
    
trie.update_all_counts()

stlm = STLM(trie)

test = 'a a a'.split()

seq = Sequence()
for t in test: seq.push_back(t)

print(stlm.prob(seq))