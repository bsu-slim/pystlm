#!/usr/bin/env python
""" generated source for module STLM """
# package: app
import io.Scanner

import java.io.FileNotFoundException

import java.util.HashMap

import sequence.Sequence

import suffixtree.SuffixTree

import lm.STLanguageModel

import model.Constants

class STLM(object):
    """ generated source for class STLM """
    @classmethod
    def main(cls, argv):
        """ generated source for method main """
        # 
        # 		 * My own way of handling command line arugments. Mostly, just use -text and -test and -perp
        # 		 
        arguments = HashMap()
        i = 0
        while len(argv):
            if argv[i] == Constants.CL_LM:
                arguments.put(argv[i], argv[i + 1])
            elif argv[i] == Constants.CL_TEXT:
                arguments.put(argv[i], argv[i + 1])
            elif argv[i] == Constants.CL_TEST:
                arguments.put(argv[i], argv[i + 1])
            elif argv[i] == Constants.CL_ORDER:
                arguments.put(argv[i], argv[i + 1])
            elif argv[i] == Constants.CL_PERP:
                arguments.put(argv[i], argv[i])
            elif argv[i] == Constants.CL_SERVER:
                arguments.put(argv[i], argv[i])
            elif argv[i] == Constants.CL_PORT:
                arguments.put(argv[i], argv[i + 1])
            elif argv[i] == Constants.CL_UNIT:
                arguments.put(argv[i], argv[i])
            elif argv[i] == Constants.CL_STATS:
                arguments.put(argv[i], argv[i])
            elif argv[i] == Constants.CL_LONG:
                arguments.put(argv[i], argv[i])
            i += 1
        trie = SuffixTree()
        if arguments.get(Constants.CL_TEXT) != None:
            try:
                print "training...",
                while scan.moreSentences():
                    if sent == None:
                        continue 
                    sent.pad()
                    while i < len(sent):
                        trie.add(sent.at(i))
                        i += 1
                trie.finish()
                print "done."
            except FileNotFoundException as e:
                e.printStackTrace()
        lm = STLanguageModel(trie)
        if arguments.get(Constants.CL_LONG) != None:
            lm.printLongBranches()
        if arguments.get(Constants.CL_TEST) != None:
            try:
                if arguments.get(Constants.CL_STATS) != None:
                    lm.computeStats(scan)
                elif arguments.get(Constants.CL_PERP) != None:
                    while scan.moreSentences():
                        cur = scan.nextSentence()
                        if cur == None or len(cur) == 0:
                            continue 
                        words += len(cur)
                        cur.padBack()
                        logprob += lm.logProb(cur)
                        cur.clear()
                        numSent += 1
                    numSent -= 1
                    print "logprob: " + logprob
                    logprob = 0 - logprob
                    print "numSent " + numSent
                    print perp
                else:
                    while scan.moreSentences():
                        if sent == None or len(sent) == 0:
                            continue 
                        sent.pad()
                        print lm.logProb(sent)
            except FileNotFoundException as e:
                e.printStackTrace()


if __name__ == '__main__':
    import sys
    STLM.main(sys.argv)

