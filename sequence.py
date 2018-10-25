'''
Created on Oct 22, 2018

@author: casey
'''
from constants import Constants

class Queue(object):
    # 
    #      * Wrapper around a linked list 
    #      

    def __init__(self):
        self.items = list()

    def push_front(self, item):
        self.items.insert(0,item)

    def push_back(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def cut(self):
        self.items.pop(0)

    def size(self):
        return len(self.items)

    def clear(self):
        self.items.clear()

    def at(self, i):
        return self.items[i]

    def is_empty(self):
        return len(self.items) == 0

    def __str__(self):
        string = ""
        for item in self.items:
            string += str(item) + " "
        return string.strip()
    
    
class Sequence(Queue):

    def __init__(self):
        super(Sequence, self).__init__()
        self.numPads = 0
    #      
    def pad(self):
        max_ = Constants.NUM_PAD
        self.numPads = max_
        i = 0
        while i < max_:
            self.push_front(Constants.START)
            self.push_fack(Constants.STOP)
            self.numPads += 1
            i += 1
        self.numPads *= 2

    def pad_back(self):
        max_ = Constants.NUM_PAD
        self.numPads = max_
        i = 0
        while i < max:
            self.push_back(Constants.STOP)
            i += 1
            
            
class Text(object):
    # 
    #      * Holds the "vocabulary" for the tree
    #'
    
    def __init__(self):
        self.vocab = dict()
        self.items = list()
        self.index = 0
        # vocab.put((T)Constants.ROOT, index++);

    def get_vocabulary(self):
        return list(self.vocab.keys())

    def push_front(self, item):
        self.items.insert(0,item)

    def push_back(self, item):
        self.items.append(item)

    def put(self, word, i):
        self.vocab[word] = i
        self.index += 1

    def pop(self):
        return self.items.pop()

    def cut(self):
        self.items.pop(0)

    def size(self):
        return len(self.items)

    def clear(self):
        self.items = list() # should be self.items.clear()

    def at(self, i):
        if self.size() == 0:
            return 0
        if i == -1:
            i = self.size() - 1
        return self.items[i]

    def offer(self, word):
        if self.get(word) == -1:
            self.vocab[word] = self.index
            self.index += 1
        return self.vocab[word]

    def get(self, word):
        if word in self.vocab:
            return self.vocab[word]
        return -1

    def has(self, word):
        if self.get(word) == -1:
            return False
        return True

    def vocab_size(self):
        return len(self.vocab)

    def get_word_from_vocab_index(self, ind):
        for word in self.vocab:
            if self.vocab[word] == ind:
                return word
        # return (T)Constants.UNK;
        return None

    def get_word_from_index(self, ind):
        for word in self.vocab:
            if self.vocab[word] == ind:
                return word
        # return (T)Constants.UNK;
        return None

