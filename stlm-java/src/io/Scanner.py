#!/usr/bin/env python
""" generated source for module Scanner """
# package: io
import java.io.File

import java.io.FileNotFoundException

import sequence.Queue

import sequence.Sequence

class Scanner(object):
    """ generated source for class Scanner """
    # 
    # 	 * Scanner may not have been the best choice in names, but it does what is needed and returns the right objects.
    # 	 
    words = Queue()
    sentMode = bool()
    scanner = java.util.Scanner()

    @overloaded
    def __init__(self):
        """ generated source for method __init__ """

    @__init__.register(object, str)
    def __init___0(self, path):
        """ generated source for method __init___0 """
        openFile(path)
        self.sentMode = False

    @__init__.register(object, str, bool)
    def __init___1(self, path, s):
        """ generated source for method __init___1 """
        openFile(path)
        self.sentMode = s

    def openFile(self, path):
        """ generated source for method openFile """
        self.scanner = java.util.Scanner(File(path))

    def set(self, path, s):
        """ generated source for method set """
        self.openFile(path)
        self.sentMode = s

    def moreSentences(self):
        """ generated source for method moreSentences """
        return self.scanner.hasNext()

    # 
    #      * Reads in a line, splits it, and puts it into a STSentence object
    #      
    def nextSentence(self):
        """ generated source for method nextSentence """
        sentence = Sequence()
        line = self.scanner.nextLine().trim()
        if not line.isEmpty():
            while len(sline):
                sentence.pushBack(sline[i].trim())
                i += 1
            return sentence
        return None

    def close(self):
        """ generated source for method close """
        self.scanner.close()

