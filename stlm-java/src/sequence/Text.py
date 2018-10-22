#!/usr/bin/env python
""" generated source for module Text """
# package: sequence
import java.util.HashMap

import java.util.LinkedList

import java.util.Set

class Text(object):
    """ generated source for class Text """
    # 
    # 	 * Holds the "vocabulary" for the tree
    # 	 
    items = LinkedList()
    vocab = HashMap()
    index = int()

    def __init__(self):
        """ generated source for method __init__ """
        self.vocab = HashMap()
        self.items = LinkedList()
        self.index = 0
        # vocab.put((T)Constants.ROOT, index++);

    def getVocabulary(self):
        """ generated source for method getVocabulary """
        return self.vocab.keySet()

    def pushFront(self, item):
        """ generated source for method pushFront """
        self.items.addFirst(item)

    def pushBack(self, item):
        """ generated source for method pushBack """
        self.items.add(item)

    def put(self, word, i):
        """ generated source for method put """
        self.vocab.put(word, i)
        self.index += 1

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
        if len(self) == 0:
            return 0
        if i == -1:
            i = len(self) - 1
        return self.items.get(i)

    def print_(self):
        """ generated source for method print_ """

    def offer(self, word):
        """ generated source for method offer """
        if get(word) == -1:
            self.vocab.put(word, self.index)
            return self.index += 1
        return self.vocab.get(word)

    def get(self, word):
        """ generated source for method get """
        if self.vocab.containsKey(word):
            return self.vocab.get(word)
        return -1

    def has(self, word):
        """ generated source for method has """
        if self.get(word) == -1:
            return False
        return True

    def vocabSize(self):
        """ generated source for method vocabSize """
        return len(self.vocab)

    def getWordFromVocabIndex(self, ind):
        """ generated source for method getWordFromVocabIndex """
        for word in vocab.keySet():
            if self.vocab.get(word) == ind:
                return word
        # return (T)Constants.UNK;
        return None

    def getWordFromIndex(self, ind):
        """ generated source for method getWordFromIndex """
        for word in vocab.keySet():
            if self.vocab.get(word) == self.at(ind):
                return word
        # return (T)Constants.UNK;
        return None

