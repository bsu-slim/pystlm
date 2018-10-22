#!/usr/bin/env python
""" generated source for module STLanguageModel """
# package: lm
import java.util.HashMap

import java.util.LinkedList

import model.Constants

import io.Scanner

import segment.InternalSegment

import segment.LeafSegment

import segment.Segment

import sequence.Queue

import sequence.Sequence

import sequence.Text

import smoothing.AddOneSmoothing

import smoothing.AdditiveSmoothing

import smoothing.DiscountSmoothing

import smoothing.Smoothing

import smoothing.WittenBellSmoothing

import suffixtree.SuffixTree

class STLanguageModel(object):
    """ generated source for class STLanguageModel """
    trie = SuffixTree()
    offset = Text()
    current = Segment()
    branch = Segment()
    arc = Segment()

    # this may not be necessary....try using the branch instead
    smoother = Smoothing()
    numMult = float()
    numOne = float()
    numUnk = float()
    numBO = float()
    maxDepthReached = int()

    # for incremental stuff
    incProb = 0.0
    incWord = int()

    #  private LogMath logMath;
    @overloaded
    def __init__(self):
        """ generated source for method __init__ """

    @__init__.register(object, SuffixTree)
    def __init___0(self, tree):
        """ generated source for method __init___0 """
        self.setTrie(tree)
        setSmoothing(DiscountSmoothing(getTrie()))
        self.offset = Text()
        # logMath = new LogMath();

    # 
    #      * starts things over - begin the chain rule from the root node
    #      
    def startNewUtterance(self):
        """ generated source for method startNewUtterance """
        self.smoother.resetUnk()
        self.smoother.reset()
        self.current = getTrie().getRoot()
        self.smoother.setCurrent(self.current)
        self.offset.clear()
        self.incProb = 0.0
        self.incWord = 0
        self.maxDepthReached = 0

    # 
    #      * get logProb for this prefix of the sentence
    #      
    def logProbPrefix(self, increment):
        """ generated source for method logProbPrefix """
        self.smoother.resetUnk()
        self.incWord = getTrie().getText().get(increment)
        self.smoother.incSentPosition()
        p = getProb(self.incWord)
        self.incProb += Math.log10(p)
        return self.incProb

    def prob(self, sent):
        """ generated source for method prob """
        self.startNewUtterance()
        prob = 1.0
        word = int()
        i = 0
        while i < len(sent):
            self.smoother.resetUnk()
            word = getTrie().getText().get(sent.at(i))
            self.smoother.incSentPosition()
            prob *= p
            i += 1
        return prob

    def logProb(self, sent):
        """ generated source for method logProb """
        self.startNewUtterance()
        prob = 1.0
        word = int()
        i = 0
        while i < len(sent):
            self.smoother.resetUnk()
            word = getTrie().getText().get(sent.at(i))
            self.smoother.incSentPosition()
            prob += Math.log10(p)
            if Constants.DEF_ORDER != -1:
                while self.smoother.getDepth() >= Constants.DEF_ORDER:
                    if self.current.getLeft() > -1:
                        self.current = self.current.getLink()
                        if self.current.getLeft() <= -1:
                            self.smoother.setMaxDepth(2)
                    else:
                        if len(self.offset) > 0:
                            self.offset.cut()
                    self.smoother.setMaxDepth(self.smoother.getMaxDepth() - 1)
                    self.smoother.decDepth()
            i += 1
        return prob

    def getProb(self, word):
        """ generated source for method getProb """
        if self.smoother.getDepth() > self.maxDepthReached:
            self.maxDepthReached = int(self.smoother.getDepth())
        prob = 0.0
        if len(self.offset) > 0:
            self.arc = self.current
            if self.arc.getLeft() + len(self.offset) > self.arc.getRight():
                self.current = findPrefixArc(self.offset.at(0))
                self.smoother.setCurrent(self.current)
                self.offset.clear()
        if wordIsHere(word):
            self.smoother.incDepth()
            if len(self.offset) == 0:
                prob = self.smoother.wordHereMultChild(self.current, child)
                self.numMult += 1
                if child.span() > 1:
                    self.offset.pushBack(word)
                else:
                    self.current = child
                    self.smoother.setCurrent(self.current)
            else:
                prob = self.smoother.wordHereOneChild(len(self.offset))
                self.numOne += 1
                self.offset.pushBack(word)
        else:
            self.smoother.updateUnk()
            self.numBO += 1
            if self.current.getLeft() > -1:
                if len(self.offset) > 0:
                    self.smoother.setDepth(self.smoother.getDepth() - len(self.offset) - 1)
                    self.offset.clear()
                else:
                    self.smoother.decDepth()
                self.current = self.current.getLink()
                if self.current.getLeft() == -1:
                    self.smoother.setDepth(0)
                self.smoother.setCurrent(self.current)
                prob = self.getProb(word)
            else:
                if len(self.offset) > 0:
                    self.offset.cut()
                    self.smoother.decDepth()
                    prob = self.getProb(word)
                else:
                    self.smoother.setDepth(0)
                    prob = self.smoother.getUnk(self.current)
                    self.numUnk += 1
        return prob

    def getMaxDepthReached(self):
        """ generated source for method getMaxDepthReached """
        return self.maxDepthReached

    def wordIsHere(self, word):
        """ generated source for method wordIsHere """
        if len(self.offset) == 0:
            return findPrefixArc(word) != None
        else:
            self.branch = findPrefixArc(self.offset.at(0))
            if self.branch.getLeft() + len(self.offset) <= getTrie().getText().size():
                if getTrie().getText().at(self.branch.getLeft() + len(self.offset)) == word:
                    return True
            return False

    def findPrefixArc(self, word):
        """ generated source for method findPrefixArc """
        return self.current.findBranch(word)

    def setSmoothing(self, s):
        """ generated source for method setSmoothing """
        self.smoother = s

    def computeStats(self, scan):
        """ generated source for method computeStats """
        max = 0.0
        depths = 0.0
        numSents = 0.0
        sentlens = 0.0
        while scan.moreSentences():
            numSents += 1
            sent = scan.nextSentence()
            if len(sent) == 0:
                continue 
            sent.pad()
            sentlens += len(sent)
            self.logProb(sent)
            if self.smoother.getDepth() > max:
                max = self.smoother.getDepth()
            depths += self.smoother.getDepth()
        print "Total number of nodes: " + " " + getTrie().numNodes
        print "Number of leaf nodes: " + " " + getTrie().numLeaves
        print "Number of internal nodes: " + " " + (getTrie().numNodes - getTrie().numLeaves)
        print "Percentage of leaf nodes: " + " " + (float(getTrie().numLeaves) / float(getTrie().numNodes))
        print "Percentage of internal nodes: " + " " + (((float(getTrie().numNodes) - float(getTrie().numLeaves)) / float(getTrie().numNodes)))
        print "Size of vocabulary: " + " " + getTrie().getRoot()len(.children)
        print "Number of words: " + " " + getTrie().getText()len(.items)
        print "Number of evaluation sentences: " + " " + numSents
        print "Number of evaluation words: " + " " + sentlens
        print "Average sentence length: " + " " + (sentlens / numSents)
        print "Maximum depth reached: " + " " + max
        print "Average depth reached: " + " " + (depths / numSents)
        print "Percentage of probs with multiple branches: " + " " + (self.numMult / sentlens)
        print "Percentage of probs with one branch: " + " " + (self.numOne / sentlens)
        print "Percentage of probs using UNK: " + " " + (self.numUnk / sentlens)
        print "Number of individual back off instances: " + " " + self.numBO

    def getTrie(self):
        """ generated source for method getTrie """
        return self.trie

    def setTrie(self, trie):
        """ generated source for method setTrie """
        self.trie = trie

    def printLongBranches(self):
        """ generated source for method printLongBranches """
        print "Printing long branches..."
        root = self.getTrie().getRoot()
        findLongBranches(root)
        for c in self.longSequences.keySet():
            print self.longSequences.get(c).__str__() + " " + c + "\\\\"

    longSequences = HashMap()

    def findLongBranches(self, current):
        """ generated source for method findLongBranches """
        if current.getRight() > 0 and current.getRight() - current.getLeft() > 1 and current.getCount() > 1:
            while i < current.getRight():
                sequence.add(word)
                i += 1
            if not self.longSequences.containsKey(sequence):
                self.longSequences.put(sequence, 0.0)
            self.longSequences.put(sequence, self.longSequences.get(sequence) + current.getCount())
        if isinstance(current, (InternalSegment, )):
            for child in internal.children.keySet():
                self.findLongBranches(internal.children.get(child))

